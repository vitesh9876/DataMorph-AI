import os
import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import pandas as pd
from app.database import get_db
from app.models.models import UploadedFile, DatasetArtifact, Report
from app.schemas.schemas import (
    ReportCreateRequest,
    ReportUpdateRequest,
    ReportResponse,
    ReportSection,
    VisualizationCard
)
from app.services.report.synthesizer import ReportSynthesizer
from app.services.visualization.recommender import VisualizationRecommender

router = APIRouter(prefix="/reports", tags=["Report Builder & Editor"])

@router.post("/generate", response_model=ReportResponse)
async def generate_report(request: ReportCreateRequest, db: AsyncSession = Depends(get_db)):
    """Automatically generates an AI-powered, fully editable executive report with modular sections."""
    q_file = await db.execute(
        select(UploadedFile)
        .options(selectinload(UploadedFile.dataset))
        .where(UploadedFile.id == request.file_id)
    )
    file_obj = q_file.scalar_one_or_none()
    if not file_obj or not file_obj.dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    dataset = file_obj.dataset
    cleaned_path = dataset.cleaned_data_path or dataset.raw_data_path
    df = pd.read_csv(cleaned_path)

    # Get recommended charts
    recommended_charts = VisualizationRecommender.recommend_charts(df)
    
    # Filter selected or take top 4
    if request.selected_chart_ids:
        selected_charts = [c for c in recommended_charts if c["id"] in request.selected_chart_ids]
        if not selected_charts:
            selected_charts = recommended_charts[:4]
    else:
        selected_charts = [c for c in recommended_charts if c.get("is_selected", True)][:4]
        if not selected_charts:
            selected_charts = recommended_charts[:4]

    # Generate sections
    sections = await ReportSynthesizer.generate_full_report(
        df=df,
        filename=file_obj.original_name,
        topics=file_obj.topics or [],
        quality_score_before=dataset.quality_score_initial,
        quality_score_after=dataset.quality_score_current,
        quality_breakdown=dataset.quality_breakdown or {},
        selected_charts=selected_charts,
        anomalies=dataset.anomalies_detected or [],
        template_type=request.template_type
    )

    report_id = str(uuid.uuid4())
    report_obj = Report(
        id=report_id,
        project_id=file_obj.project_id,
        file_id=file_obj.id,
        title=request.title,
        template_type=request.template_type,
        sections=sections,
        selected_visualizations=selected_charts
    )
    db.add(report_obj)
    await db.commit()

    report_sections = [ReportSection(**s) for s in sections]
    viz_cards = [VisualizationCard(**c) for c in selected_charts]

    return ReportResponse(
        id=report_obj.id,
        file_id=file_obj.id,
        title=report_obj.title,
        template_type=report_obj.template_type,
        sections=report_sections,
        selected_visualizations=viz_cards,
        created_at=report_obj.created_at,
        updated_at=report_obj.updated_at
    )

@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(report_id: str, db: AsyncSession = Depends(get_db)):
    """Retrieves an existing editable report."""
    q_rep = await db.execute(select(Report).where(Report.id == report_id))
    report_obj = q_rep.scalar_one_or_none()
    if not report_obj:
        raise HTTPException(status_code=404, detail="Report not found")

    report_sections = [ReportSection(**s) for s in (report_obj.sections or [])]
    viz_cards = [VisualizationCard(**c) for c in (report_obj.selected_visualizations or [])]

    return ReportResponse(
        id=report_obj.id,
        file_id=report_obj.file_id,
        title=report_obj.title,
        template_type=report_obj.template_type,
        sections=report_sections,
        selected_visualizations=viz_cards,
        created_at=report_obj.created_at,
        updated_at=report_obj.updated_at
    )

@router.put("/{report_id}", response_model=ReportResponse)
async def update_report(report_id: str, request: ReportUpdateRequest, db: AsyncSession = Depends(get_db)):
    """Updates report title, template type, reorders or edits individual sections."""
    q_rep = await db.execute(select(Report).where(Report.id == report_id))
    report_obj = q_rep.scalar_one_or_none()
    if not report_obj:
        raise HTTPException(status_code=404, detail="Report not found")

    if request.title is not None:
        report_obj.title = request.title
    if request.template_type is not None:
        report_obj.template_type = request.template_type
    if request.sections is not None:
        report_obj.sections = [s.model_dump() for s in request.sections]

    await db.commit()
    return await get_report(report_id, db)
