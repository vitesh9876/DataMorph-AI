from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.database import get_db
from app.models.models import UploadedFile, DatasetArtifact
from app.schemas.schemas import FileAnalysisResponse, DocStats, ColumnMeta

router = APIRouter(prefix="/analysis", tags=["AI File Analysis"])

@router.get("/{file_id}", response_model=FileAnalysisResponse)
async def get_file_analysis(file_id: str, db: AsyncSession = Depends(get_db)):
    """Returns the comprehensive AI analysis screen data including understanding card and document stats."""
    q_file = await db.execute(
        select(UploadedFile)
        .options(selectinload(UploadedFile.dataset))
        .where(UploadedFile.id == file_id)
    )
    file_obj = q_file.scalar_one_or_none()
    if not file_obj:
        raise HTTPException(status_code=404, detail="File analysis not found")

    dataset = file_obj.dataset
    doc_stats_dict = file_obj.doc_stats or {}
    
    doc_stats = DocStats(
        pages=doc_stats_dict.get("pages", 1),
        tables=doc_stats_dict.get("tables", 0),
        charts=doc_stats_dict.get("charts", 0),
        sections=doc_stats_dict.get("sections", 1),
        rows=doc_stats_dict.get("rows", dataset.num_rows if dataset else 0),
        columns=doc_stats_dict.get("columns", dataset.num_columns if dataset else 0)
    )

    columns_meta = []
    if dataset and dataset.columns_meta:
        for c in dataset.columns_meta:
            columns_meta.append(ColumnMeta(**c))

    quality_score = dataset.quality_score_current if dataset else 75.0
    sample_data = dataset.current_sample if dataset else []

    return FileAnalysisResponse(
        file_id=file_obj.id,
        filename=file_obj.original_name,
        file_type=file_obj.file_type,
        file_size=file_obj.file_size,
        data_type=file_obj.data_type or "tabular",
        raw_text=file_obj.raw_text or "",
        doc_stats=doc_stats,
        topics=file_obj.topics or ["Operational Data"],
        entities=file_obj.entities or [],
        ai_understanding=file_obj.summary_text or "Analysis completed successfully.",
        quality_score=round(quality_score, 1),
        columns_meta=columns_meta,
        sample_data=sample_data
    )
