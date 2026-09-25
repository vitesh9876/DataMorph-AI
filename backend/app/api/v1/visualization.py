import os
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import pandas as pd
from app.database import get_db
from app.models.models import UploadedFile, DatasetArtifact
from app.schemas.schemas import (
    VisualizationListResponse,
    VisualizationCard,
    CustomChartGenerateRequest,
    ChartConfig
)
from app.services.visualization.recommender import VisualizationRecommender
from app.services.visualization.aggregator import ChartAggregator

router = APIRouter(prefix="/visualizations", tags=["Visualization Recommendation Engine"])

@router.get("/{file_id}", response_model=VisualizationListResponse)
async def get_visualizations(file_id: str, db: AsyncSession = Depends(get_db)):
    """Returns AI-recommended charts with confidence scores, explanations, and preview data."""
    q_file = await db.execute(
        select(UploadedFile)
        .options(selectinload(UploadedFile.dataset))
        .where(UploadedFile.id == file_id)
    )
    file_obj = q_file.scalar_one_or_none()
    if not file_obj or not file_obj.dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    dataset = file_obj.dataset
    cleaned_path = dataset.cleaned_data_path or dataset.raw_data_path

    if not cleaned_path or not os.path.exists(cleaned_path):
        raise HTTPException(status_code=400, detail="Data file not available for visualization")

    df = pd.read_csv(cleaned_path)
    recommended_list = VisualizationRecommender.recommend_charts(df)

    cards = []
    for item in recommended_list:
        cfg = item["chart_config"]
        cards.append(VisualizationCard(
            id=item["id"],
            title=item["title"],
            chart_type=item["chart_type"],
            confidence_score=item["confidence_score"],
            reason=item["reason"],
            chart_config=ChartConfig(
                chart_type=cfg.get("chart_type", "bar"),
                title=cfg.get("title", ""),
                x_axis=cfg.get("x_axis"),
                y_axis=cfg.get("y_axis"),
                aggregation=cfg.get("aggregation", "sum"),
                color_palette=cfg.get("color_palette", "default")
            ),
            chart_data=item["chart_data"],
            is_selected=item.get("is_selected", False)
        ))

    return VisualizationListResponse(
        file_id=file_id,
        recommended_charts=cards,
        available_columns=list(df.columns)
    )

@router.post("/{file_id}/custom", response_model=VisualizationCard)
async def generate_custom_chart(file_id: str, request: CustomChartGenerateRequest, db: AsyncSession = Depends(get_db)):
    """Generates a custom chart based on user-selected X/Y axes and chart type."""
    q_file = await db.execute(
        select(UploadedFile)
        .options(selectinload(UploadedFile.dataset))
        .where(UploadedFile.id == file_id)
    )
    file_obj = q_file.scalar_one_or_none()
    if not file_obj or not file_obj.dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    dataset = file_obj.dataset
    cleaned_path = dataset.cleaned_data_path or dataset.raw_data_path
    df = pd.read_csv(cleaned_path)

    chart_data = ChartAggregator.aggregate_for_chart(
        df=df,
        x_col=request.x_axis,
        y_col=request.y_axis,
        chart_type=request.chart_type,
        aggregation=request.aggregation or "sum",
        group_by=request.group_by
    )

    title = request.title or (f"{request.y_axis} by {request.x_axis}" if request.y_axis else f"{request.x_axis} Distribution")

    return VisualizationCard(
        id=str(uuid.uuid4()),
        title=title,
        chart_type=request.chart_type,
        confidence_score=90,
        reason=f"Custom chart built for '{request.x_axis}' and '{request.y_axis}'.",
        chart_config=ChartConfig(
            chart_type=request.chart_type,
            title=title,
            x_axis=request.x_axis,
            y_axis=request.y_axis,
            aggregation=request.aggregation or "sum",
            group_by=request.group_by
        ),
        chart_data=chart_data,
        is_selected=True
    )
