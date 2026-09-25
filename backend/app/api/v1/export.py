import os
import uuid
import json
import zipfile
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import pandas as pd
from app.config import settings
from app.database import get_db
from app.models.models import Report, UploadedFile, DatasetArtifact
from app.schemas.schemas import ExportRequest, ExportResponse
from app.services.export.pdf_exporter import PDFExporter
from app.services.export.docx_exporter import DOCXExporter
from app.services.export.pptx_exporter import PPTXExporter
from app.services.export.xlsx_exporter import XLSXExporter
from app.services.export.html_exporter import HTMLExporter

router = APIRouter(prefix="/export", tags=["Multi-Format Export Engine"])

@router.post("", response_model=ExportResponse)
async def export_report(request: ExportRequest, db: AsyncSession = Depends(get_db)):
    """Exports an intelligence report into PDF, DOCX, PPTX, XLSX, or HTML format."""
    q_rep = await db.execute(
        select(Report)
        .options(selectinload(Report.file).selectinload(UploadedFile.dataset))
        .where(Report.id == request.report_id)
    )
    report_obj = q_rep.scalar_one_or_none()
    if not report_obj:
        raise HTTPException(status_code=404, detail="Report not found")

    fmt = request.format.lower()
    export_id = str(uuid.uuid4())[:8]
    clean_title = "".join(c for c in report_obj.title if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
    
    filename = f"{clean_title}_{export_id}.{fmt}"
    output_path = os.path.join(settings.EXPORT_DIR, filename)

    sections = list(report_obj.sections or [])
    template_type = request.template_type or report_obj.template_type

    # Ensure chart_data is fully populated for every visualization section
    if report_obj.file and report_obj.file.dataset:
        cleaned_path = report_obj.file.dataset.cleaned_data_path or report_obj.file.dataset.raw_data_path
        if cleaned_path and os.path.exists(cleaned_path):
            try:
                from app.services.visualization.recommender import VisualizationRecommender
                df = pd.read_csv(cleaned_path)
                rec_charts = VisualizationRecommender.recommend_charts(df)
                chart_map = {c["title"].lower().strip(): c for c in rec_charts}
                
                chart_idx = 0
                for s in sections:
                    sec_type = s.get("section_type")
                    if sec_type == "visualizations" and not s.get("chart_data"):
                        sec_title = s.get("title", "").lower().strip()
                        matched = chart_map.get(sec_title)
                        if not matched and chart_idx < len(rec_charts):
                            matched = rec_charts[chart_idx]
                            chart_idx += 1
                        if matched:
                            s["chart_data"] = matched.get("chart_data", [])
                            s["chart_type"] = matched.get("chart_type", "bar")
                    elif sec_type == "structured_table":
                        seg_name = s.get("segment_name") or ""
                        df_target = df
                        if seg_name and seg_name.lower() != "all":
                            seg_col = next((c for c in df.columns if c.lower() in [
                                'category', 'test_category', 'segment', 'product_category', 'department', 'region', 'type', 'section'
                            ]), None)
                            if seg_col:
                                df_target = df[df[seg_col].astype(str).str.lower() == seg_name.lower()]
                        s["table_data"] = df_target.head(30).to_dict(orient="records")
                        s["table_columns"] = list(df.columns)
            except Exception as e:
                pass

    if fmt == "pdf":
        PDFExporter.export_to_pdf(
            output_path=output_path,
            report_title=report_obj.title,
            template_type=template_type,
            sections=sections
        )
    elif fmt == "docx":
        DOCXExporter.export_to_docx(
            output_path=output_path,
            report_title=report_obj.title,
            template_type=template_type,
            sections=sections
        )
    elif fmt == "pptx":
        PPTXExporter.export_to_pptx(
            output_path=output_path,
            report_title=report_obj.title,
            template_type=template_type,
            sections=sections
        )
    elif fmt == "html":
        HTMLExporter.export_to_html(
            output_path=output_path,
            report_title=report_obj.title,
            sections=sections
        )
    elif fmt == "xlsx":
        df = pd.DataFrame()
        quality_score = 90.0
        recommendations = []
        if report_obj.file and report_obj.file.dataset:
            dataset = report_obj.file.dataset
            cleaned_path = dataset.cleaned_data_path or dataset.raw_data_path
            if cleaned_path and os.path.exists(cleaned_path):
                df = pd.read_csv(cleaned_path)
            quality_score = dataset.quality_score_current
        
        XLSXExporter.export_to_xlsx(
            output_path=output_path,
            df=df,
            quality_score=quality_score,
            recommendations=recommendations,
            anomalies=[]
        )
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported export format: {fmt}. Supported: pdf, docx, pptx, html, xlsx.")

    file_size = os.path.getsize(output_path)
    download_url = f"/api/v1/export/download/{filename}"

    return ExportResponse(
        download_url=download_url,
        format=fmt,
        file_name=filename,
        file_size=file_size
    )

@router.post("/dataset/{file_id}", response_model=ExportResponse)
async def export_dataset_direct(
    file_id: str, 
    format: str = "csv", 
    segment: Optional[str] = Query(None, description="Optional segment or category name to filter"),
    db: AsyncSession = Depends(get_db)
):
    """Exports structured data directly as a single file (CSV, XLSX, or JSON), optionally filtered to a single detected segment."""
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
        raise HTTPException(status_code=404, detail="Structured data file not found")

    df = pd.read_csv(cleaned_path)

    # Filter to specific segment/category if requested
    segment_suffix = ""
    if segment and segment.lower() != "all":
        # Look for category column
        cat_cols = [c for c in df.columns if any(k in c.lower() for k in ["category", "type", "segment", "department", "region", "section"])]
        if cat_cols:
            df = df[df[cat_cols[0]].astype(str).str.lower() == segment.lower()]
            segment_suffix = f"_{segment.replace(' ', '_')}"

    fmt = format.lower()
    export_id = str(uuid.uuid4())[:8]
    base_name = os.path.splitext(file_obj.original_name)[0]
    clean_title = "".join(c for c in base_name if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
    
    filename = f"{clean_title}{segment_suffix}_structured_{export_id}.{fmt}"
    output_path = os.path.join(settings.EXPORT_DIR, filename)

    if fmt == "csv":
        df.to_csv(output_path, index=False)
    elif fmt == "xlsx":
        df.to_excel(output_path, index=False)
    elif fmt == "json":
        df.to_json(output_path, orient="records", indent=2)
    else:
        raise HTTPException(status_code=400, detail=f"Unsupported format {fmt}. Use csv, xlsx, or json.")

    file_size = os.path.getsize(output_path)
    download_url = f"/api/v1/export/download/{filename}"

    return ExportResponse(
        download_url=download_url,
        format=fmt,
        file_name=filename,
        file_size=file_size
    )

@router.post("/dataset/{file_id}/zip-segments", response_model=ExportResponse)
async def export_dataset_separate_zip(
    file_id: str, 
    format: str = "csv", 
    db: AsyncSession = Depends(get_db)
):
    """
    Exports all distinct detected sub-tables/segments/categories as SEPARATE individual files
    packaged together in a single downloadable ZIP archive.
    """
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
        raise HTTPException(status_code=404, detail="Structured data file not found")

    df = pd.read_csv(cleaned_path)
    fmt = format.lower()
    if fmt not in ["csv", "xlsx", "json"]:
        fmt = "csv"

    export_id = str(uuid.uuid4())[:8]
    base_name = os.path.splitext(file_obj.original_name)[0]
    clean_title = "".join(c for c in base_name if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
    zip_filename = f"{clean_title}_Separate_Data_Files_{export_id}.zip"
    zip_path = os.path.join(settings.EXPORT_DIR, zip_filename)

    # Find segmenting column
    cat_cols = [c for c in df.columns if any(k in c.lower() for k in ["category", "test_category", "segment", "department", "region", "section", "table", "type"])]

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        if cat_cols:
            cat_col = cat_cols[0]
            groups = df.groupby(cat_col)
            for group_name, group_df in groups:
                clean_grp = "".join(c for c in str(group_name) if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
                file_in_zip = f"{clean_title}_{clean_grp}.{fmt}"
                temp_path = os.path.join(settings.EXPORT_DIR, f"temp_{export_id}_{file_in_zip}")

                if fmt == "csv":
                    group_df.to_csv(temp_path, index=False)
                elif fmt == "xlsx":
                    group_df.to_excel(temp_path, index=False)
                elif fmt == "json":
                    group_df.to_json(temp_path, orient="records", indent=2)

                zip_file.write(temp_path, arcname=file_in_zip)
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        else:
            # If no category column, chunk into logical subsets
            file_in_zip = f"{clean_title}_full_data.{fmt}"
            temp_path = os.path.join(settings.EXPORT_DIR, f"temp_{export_id}_{file_in_zip}")
            if fmt == "csv":
                df.to_csv(temp_path, index=False)
            elif fmt == "xlsx":
                df.to_excel(temp_path, index=False)
            elif fmt == "json":
                df.to_json(temp_path, orient="records", indent=2)
            zip_file.write(temp_path, arcname=file_in_zip)
            if os.path.exists(temp_path):
                os.remove(temp_path)

    file_size = os.path.getsize(zip_path)
    download_url = f"/api/v1/export/download/{zip_filename}"

    return ExportResponse(
        download_url=download_url,
        format="zip",
        file_name=zip_filename,
        file_size=file_size
    )

@router.post("/dataset/{file_id}/multi-sheet-excel", response_model=ExportResponse)
async def export_dataset_multisheet(file_id: str, db: AsyncSession = Depends(get_db)):
    """Exports structured data as a single Excel workbook with separate sheets for each detected category/segment."""
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
        raise HTTPException(status_code=404, detail="Structured data file not found")

    df = pd.read_csv(cleaned_path)
    export_id = str(uuid.uuid4())[:8]
    base_name = os.path.splitext(file_obj.original_name)[0]
    clean_title = "".join(c for c in base_name if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
    
    filename = f"{clean_title}_MultiSheet_Workbook_{export_id}.xlsx"
    output_path = os.path.join(settings.EXPORT_DIR, filename)

    cat_cols = [c for c in df.columns if any(k in c.lower() for k in ["category", "test_category", "segment", "department", "region", "section", "type"])]

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        # Sheet 1: All Combined Data
        df.to_excel(writer, sheet_name="All Combined Data", index=False)

        if cat_cols:
            cat_col = cat_cols[0]
            for group_name, group_df in df.groupby(cat_col):
                sheet_name = str(group_name)[:30].replace(":", "").replace("/", "_").replace("\\", "_")
                group_df.to_excel(writer, sheet_name=sheet_name, index=False)

    file_size = os.path.getsize(output_path)
    download_url = f"/api/v1/export/download/{filename}"

    return ExportResponse(
        download_url=download_url,
        format="xlsx",
        file_name=filename,
        file_size=file_size
    )

@router.get("/download/{filename}")
async def download_file(filename: str):
    """Direct binary download endpoint for exported artifacts."""
    file_path = os.path.join(settings.EXPORT_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Exported file not found or expired")

    ext = os.path.splitext(filename)[1].lower()
    media_types = {
        ".pdf": "application/pdf",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".csv": "text/csv",
        ".json": "application/json",
        ".zip": "application/zip",
        ".html": "text/html"
    }

    return FileResponse(
        path=file_path,
        media_type=media_types.get(ext, "application/octet-stream"),
        filename=filename
    )
