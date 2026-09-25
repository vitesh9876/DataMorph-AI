import os
import uuid
import shutil
import logging
from datetime import datetime
from typing import List
from fastapi import APIRouter, UploadFile, File, BackgroundTasks, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.config import settings
from app.database import get_db
from app.models.models import UploadedFile, DatasetArtifact
from app.schemas.schemas import FileUploadResponse, FileStatusResponse, TimelineStep
from app.services.extractors.pipeline import ExtractionPipeline
from app.services.structuring.quality import QualityAnalyzer
from app.services.structuring.cleaner import DataCleaner
from app.services.ml.anomaly import AnomalyDetector
from app.services.ml.clustering import CorrelationEngine

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/upload", tags=["Upload & Processing"])

# Progress timeline definitions
TIMELINE_STEPS = [
    {"step_id": "detecting_structure", "label": "Detecting file structure"},
    {"step_id": "extracting_text_tables", "label": "Extracting text and tables"},
    {"step_id": "identifying_entities", "label": "Identifying data entities"},
    {"step_id": "detecting_relationships", "label": "Detecting columns and relationships"},
    {"step_id": "checking_quality", "label": "Checking data quality"},
    {"step_id": "preparing_visualizations", "label": "Preparing visualization possibilities"}
]

# In-memory progress tracking for realtime UI timeline animations
FILE_PROGRESS_TRACKER = {}

async def process_file_pipeline(file_id: str, file_path: str, original_filename: str):
    """Background pipeline executing all automated analysis stages."""
    from app.database import AsyncSessionLocal
    
    async with AsyncSessionLocal() as db:
        try:
            # Step 1: Detecting structure
            FILE_PROGRESS_TRACKER[file_id] = {"step": "detecting_structure", "progress": 15, "status": "processing"}
            
            # Step 2: Extracting text & tables
            FILE_PROGRESS_TRACKER[file_id] = {"step": "extracting_text_tables", "progress": 35, "status": "processing"}
            extraction_result = await ExtractionPipeline.extract_file(file_path, original_filename)
            df = extraction_result.dataframe

            # Step 3: Identifying entities & topics
            FILE_PROGRESS_TRACKER[file_id] = {"step": "identifying_entities", "progress": 55, "status": "processing"}
            
            # Step 4: Detecting relationships & columns
            FILE_PROGRESS_TRACKER[file_id] = {"step": "detecting_relationships", "progress": 70, "status": "processing"}
            
            # Step 5: Checking quality & generating recommendations
            FILE_PROGRESS_TRACKER[file_id] = {"step": "checking_quality", "progress": 85, "status": "processing"}
            quality_eval = QualityAnalyzer.evaluate_quality(df) if df is not None and not df.empty else {
                "completeness": 100.0, "consistency": 100.0, "uniqueness": 100.0, "validity": 100.0, "overall_score": 90.0, "columns_analysis": []
            }

            # Step 6: Preparing ML & recommendations
            FILE_PROGRESS_TRACKER[file_id] = {"step": "preparing_visualizations", "progress": 95, "status": "processing"}
            raw_sample = df.head(10).to_dict(orient="records") if df is not None and not df.empty else []
            
            # Save raw dataset to disk for persistence
            raw_csv_path = os.path.join(settings.CACHE_DIR, f"{file_id}_raw.csv")
            cleaned_csv_path = os.path.join(settings.CACHE_DIR, f"{file_id}_cleaned.csv")
            if df is not None and not df.empty:
                df.to_csv(raw_csv_path, index=False)
                df.to_csv(cleaned_csv_path, index=False)

            # Generate initial recommendations
            cleaning_recommendations = DataCleaner.generate_recommendations(df) if df is not None and not df.empty else []

            # ML Anomaly & Correlation detection
            anomaly_data = AnomalyDetector.detect_anomalies(df) if df is not None and not df.empty else {"anomalies": []}
            correlations_data = CorrelationEngine.analyze_correlations(df) if df is not None and not df.empty else {}

            # Update DB UploadedFile
            q_file = await db.execute(
                select(UploadedFile)
                .options(selectinload(UploadedFile.dataset))
                .where(UploadedFile.id == file_id)
            )
            file_obj = q_file.scalar_one_or_none()
            if file_obj:
                file_obj.status = "ready"
                file_obj.processing_step = "completed"
                file_obj.raw_text = extraction_result.raw_text
                file_obj.summary_text = extraction_result.summary
                file_obj.topics = extraction_result.topics
                file_obj.entities = extraction_result.entities
                file_obj.doc_stats = extraction_result.doc_stats
                file_obj.data_type = extraction_result.data_type

                from app.models.models import CleaningRecommendation
                
                # Check if dataset already exists for this file
                if file_obj.dataset:
                    dataset_artifact = file_obj.dataset
                    dataset_artifact.num_rows = extraction_result.doc_stats.get("rows", 0)
                    dataset_artifact.num_columns = extraction_result.doc_stats.get("columns", 0)
                    dataset_artifact.columns_meta = quality_eval.get("columns_analysis", [])
                    dataset_artifact.raw_sample = raw_sample
                    dataset_artifact.current_sample = raw_sample
                    dataset_artifact.raw_data_path = raw_csv_path
                    dataset_artifact.cleaned_data_path = cleaned_csv_path
                    dataset_artifact.quality_score_initial = quality_eval.get("overall_score", 75.0)
                    dataset_artifact.quality_score_current = quality_eval.get("overall_score", 75.0)
                    dataset_artifact.quality_breakdown = quality_eval
                    dataset_artifact.anomalies_detected = anomaly_data.get("anomalies", [])
                    dataset_artifact.correlations = correlations_data
                else:
                    dataset_artifact = DatasetArtifact(
                        file_id=file_id,
                        num_rows=extraction_result.doc_stats.get("rows", 0),
                        num_columns=extraction_result.doc_stats.get("columns", 0),
                        columns_meta=quality_eval.get("columns_analysis", []),
                        raw_sample=raw_sample,
                        current_sample=raw_sample,
                        raw_data_path=raw_csv_path,
                        cleaned_data_path=cleaned_csv_path,
                        quality_score_initial=quality_eval.get("overall_score", 75.0),
                        quality_score_current=quality_eval.get("overall_score", 75.0),
                        quality_breakdown=quality_eval,
                        anomalies_detected=anomaly_data.get("anomalies", []) if isinstance(anomaly_data, dict) else [],
                        correlations=correlations_data
                    )
                    db.add(dataset_artifact)
                    await db.flush()

                # Add recommendations
                for rec in cleaning_recommendations:
                    rec_obj = CleaningRecommendation(
                        id=rec["id"],
                        dataset_id=dataset_artifact.id,
                        rule_type=rec["rule_type"],
                        title=rec["title"],
                        description=rec["description"],
                        target_column=rec.get("target_column"),
                        suggested_action=rec["suggested_action"],
                        parameters=rec.get("parameters", {}),
                        status="pending",
                        impact_score_gain=rec.get("impact_score_gain", 5.0),
                        before_preview=rec.get("before_preview", []),
                        after_preview=rec.get("after_preview", [])
                    )
                    db.add(rec_obj)

                await db.commit()

            FILE_PROGRESS_TRACKER[file_id] = {"step": "completed", "progress": 100, "status": "ready"}
            logger.info(f"File pipeline completed successfully for {file_id}")
        except Exception as e:
            logger.error(f"Error processing pipeline for {file_id}: {e}", exc_info=True)
            FILE_PROGRESS_TRACKER[file_id] = {"step": "error", "progress": 100, "status": "error", "error": str(e)}
            
            q_file = await db.execute(select(UploadedFile).where(UploadedFile.id == file_id))
            file_obj = q_file.scalar_one_or_none()
            if file_obj:
                file_obj.status = "error"
                file_obj.error_message = str(e)
                await db.commit()

@router.post("", response_model=FileUploadResponse)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    """Uploads a file (PDF, PPT/PPTX, CSV, XLSX, XLS, TXT, XML, JSON, DOCX) and triggers the AI pipeline."""
    file_id = str(uuid.uuid4())
    ext = os.path.splitext(file.filename)[1].lower()
    stored_filename = f"{file_id}{ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, stored_filename)

    # Save to storage
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = os.path.getsize(file_path)

    # Save file record in DB
    uploaded_file = UploadedFile(
        id=file_id,
        filename=stored_filename,
        original_name=file.filename,
        file_type=ext.replace(".", ""),
        file_size=file_size,
        file_path=file_path,
        status="processing",
        processing_step="detecting_structure"
    )
    db.add(uploaded_file)
    await db.commit()

    # Launch processing pipeline in background
    background_tasks.add_task(process_file_pipeline, file_id, file_path, file.filename)

    return FileUploadResponse(
        file_id=file_id,
        filename=stored_filename,
        original_name=file.filename,
        file_type=ext.replace(".", ""),
        file_size=file_size,
        status="processing",
        message="File uploaded successfully. AI processing pipeline initiated."
    )

@router.get("/{file_id}/status", response_model=FileStatusResponse)
async def get_file_status(file_id: str, db: AsyncSession = Depends(get_db)):
    """Returns the live AI processing timeline progress for animated UI representation."""
    tracker = FILE_PROGRESS_TRACKER.get(file_id)

    # Fallback to DB if not in memory
    if not tracker:
        q = await db.execute(select(UploadedFile).where(UploadedFile.id == file_id))
        f = q.scalar_one_or_none()
        if not f:
            raise HTTPException(status_code=404, detail="File not found")
        tracker = {
            "step": f.processing_step,
            "progress": 100 if f.status == "ready" else (0 if f.status == "uploaded" else 50),
            "status": f.status,
            "error": f.error_message
        }

    current_step = tracker.get("step", "detecting_structure")
    status = tracker.get("status", "processing")
    progress = tracker.get("progress", 10)
    error = tracker.get("error")

    # Build timeline array
    timeline = []
    step_reached = False
    for item in TIMELINE_STEPS:
        if item["step_id"] == current_step:
            step_status = "error" if status == "error" else ("completed" if status == "ready" else "active")
            step_reached = True
        elif not step_reached:
            step_status = "completed"
        else:
            step_status = "waiting"

        timeline.append(TimelineStep(
            step_id=item["step_id"],
            label=item["label"],
            status=step_status,
            timestamp=datetime.utcnow().strftime("%H:%M:%S") if step_status == "completed" else None
        ))

    return FileStatusResponse(
        file_id=file_id,
        status=status,
        current_step=current_step,
        progress=progress,
        timeline=timeline,
        error=error
    )
