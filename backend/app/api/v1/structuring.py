import os
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import pandas as pd
from app.database import get_db
from app.models.models import UploadedFile, DatasetArtifact, CleaningRecommendation
from app.schemas.schemas import (
    StructuringOverviewResponse,
    CleaningRecommendationItem,
    QualityBreakdown,
    RuleActionRequest,
    BatchRuleActionRequest
)
from app.services.structuring.cleaner import DataCleaner
from app.services.structuring.quality import QualityAnalyzer

router = APIRouter(prefix="/structuring", tags=["Data Structuring Workspace"])

@router.get("/{file_id}", response_model=StructuringOverviewResponse)
async def get_structuring_overview(file_id: str, db: AsyncSession = Depends(get_db)):
    """Returns the side-by-side Raw vs AI-Structured data view and list of cleaning recommendations."""
    q_file = await db.execute(
        select(UploadedFile)
        .options(
            selectinload(UploadedFile.dataset).selectinload(DatasetArtifact.recommendations)
        )
        .where(UploadedFile.id == file_id)
    )
    file_obj = q_file.scalar_one_or_none()
    if not file_obj or not file_obj.dataset:
        raise HTTPException(status_code=404, detail="Dataset structuring data not found")

    dataset = file_obj.dataset
    recommendations = []
    for r in (dataset.recommendations or []):
        recommendations.append(CleaningRecommendationItem(
            id=r.id,
            rule_type=r.rule_type,
            title=r.title,
            description=r.description,
            target_column=r.target_column,
            suggested_action=r.suggested_action,
            status=r.status,
            impact_score_gain=r.impact_score_gain,
            before_preview=r.before_preview or [],
            after_preview=r.after_preview or []
        ))

    breakdown_dict = dataset.quality_breakdown or {}
    quality_breakdown = QualityBreakdown(
        completeness=breakdown_dict.get("completeness", 90.0),
        consistency=breakdown_dict.get("consistency", 90.0),
        uniqueness=breakdown_dict.get("uniqueness", 90.0),
        validity=breakdown_dict.get("validity", 90.0),
        overall_score=dataset.quality_score_current
    )

    return StructuringOverviewResponse(
        file_id=file_obj.id,
        dataset_id=dataset.id,
        total_rows_raw=dataset.num_rows,
        total_rows_clean=len(dataset.current_sample) if dataset.current_sample else dataset.num_rows,
        total_columns=dataset.num_columns,
        raw_sample=dataset.raw_sample or [],
        structured_sample=dataset.current_sample or [],
        quality_score_before=round(dataset.quality_score_initial, 1),
        quality_score_after=round(dataset.quality_score_current, 1),
        quality_breakdown=quality_breakdown,
        recommendations=recommendations
    )

@router.post("/{file_id}/rules/action", response_model=StructuringOverviewResponse)
async def apply_rule_action(file_id: str, request: RuleActionRequest, db: AsyncSession = Depends(get_db)):
    """Accepts or rejects an individual data cleaning rule and updates the active dataset and quality score."""
    q_file = await db.execute(
        select(UploadedFile)
        .options(
            selectinload(UploadedFile.dataset).selectinload(DatasetArtifact.recommendations)
        )
        .where(UploadedFile.id == file_id)
    )
    file_obj = q_file.scalar_one_or_none()
    if not file_obj or not file_obj.dataset:
        raise HTTPException(status_code=404, detail="Dataset not found")

    dataset = file_obj.dataset
    target_rule = next((r for r in (dataset.recommendations or []) if r.id == request.recommendation_id), None)
    if not target_rule:
        raise HTTPException(status_code=404, detail="Cleaning recommendation not found")

    target_rule.status = "accepted" if request.action == "accept" else "rejected"

    # Re-apply all accepted rules sequentially from raw data
    if dataset.raw_data_path and os.path.exists(dataset.raw_data_path):
        df = pd.read_csv(dataset.raw_data_path)
        accepted_rules = [r for r in (dataset.recommendations or []) if r.status == "accepted"]

        for rule in accepted_rules:
            df = DataCleaner.apply_rule(
                df=df,
                rule_type=rule.rule_type,
                target_column=rule.target_column,
                suggested_action=rule.suggested_action,
                parameters=rule.parameters or {}
            )

        # Save updated cleaned dataset
        df.to_csv(dataset.cleaned_data_path, index=False)
        dataset.current_sample = df.head(10).to_dict(orient="records")
        dataset.num_rows = len(df)
        dataset.num_columns = len(df.columns)

        # Recalculate Quality Score
        quality_eval = QualityAnalyzer.evaluate_quality(df)
        dataset.quality_score_current = quality_eval.get("overall_score", 90.0)
        dataset.quality_breakdown = quality_eval
        dataset.columns_meta = quality_eval.get("columns_analysis", [])

    await db.commit()
    return await get_structuring_overview(file_id, db)

@router.post("/{file_id}/rules/batch", response_model=StructuringOverviewResponse)
async def apply_batch_rules(file_id: str, request: BatchRuleActionRequest, db: AsyncSession = Depends(get_db)):
    """Applies a batch of accept/reject decisions."""
    for action_req in request.actions:
        await apply_rule_action(file_id, action_req, db)
    return await get_structuring_overview(file_id, db)
