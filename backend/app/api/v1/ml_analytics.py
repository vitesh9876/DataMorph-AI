import os
from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import pandas as pd
from app.database import get_db
from app.models.models import UploadedFile, DatasetArtifact
from app.schemas.schemas import (
    AnomalyDetectionResponse,
    AnomalyItem,
    ForecastRequest,
    ForecastResponse,
    ForecastPoint,
    CorrelationMatrixResponse
)
from app.services.ml.anomaly import AnomalyDetector
from app.services.ml.forecasting import TimeSeriesForecaster
from app.services.ml.clustering import CorrelationEngine

router = APIRouter(prefix="/ml", tags=["Machine Learning Analytics"])

@router.get("/{file_id}/anomalies", response_model=AnomalyDetectionResponse)
async def get_anomalies(file_id: str, contamination: float = 0.05, db: AsyncSession = Depends(get_db)):
    """Runs Isolation Forest anomaly detection over the dataset."""
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

    result = AnomalyDetector.detect_anomalies(df, contamination=contamination)
    
    anomalies_list = [AnomalyItem(**a) for a in result.get("anomalies", [])]

    return AnomalyDetectionResponse(
        file_id=file_id,
        total_anomalies=result.get("total_anomalies", 0),
        anomaly_percentage=result.get("anomaly_percentage", 0.0),
        algorithm=result.get("algorithm", "Isolation Forest"),
        anomalies=anomalies_list
    )

@router.post("/{file_id}/forecast", response_model=ForecastResponse)
async def generate_forecast(file_id: str, request: ForecastRequest, db: AsyncSession = Depends(get_db)):
    """Generates future time-series forecasts with 95% confidence intervals."""
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

    try:
        forecast_res = TimeSeriesForecaster.generate_forecast(
            df=df,
            date_column=request.date_column,
            value_column=request.value_column,
            periods=request.periods,
            frequency=request.frequency
        )

        points = [ForecastPoint(**p) for p in forecast_res["forecast_data"]]

        return ForecastResponse(
            date_column=request.date_column,
            value_column=request.value_column,
            model_name=forecast_res["model_name"],
            forecast_data=points,
            summary_insight=forecast_res["summary_insight"]
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Forecasting error: {str(e)}")

@router.get("/{file_id}/correlations", response_model=CorrelationMatrixResponse)
async def get_correlations(file_id: str, db: AsyncSession = Depends(get_db)):
    """Calculates Pearson correlation matrix across numeric dimensions."""
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

    corr_res = CorrelationEngine.analyze_correlations(df)
    return CorrelationMatrixResponse(
        columns=corr_res.get("columns", []),
        matrix=corr_res.get("matrix", []),
        strong_correlations=corr_res.get("strong_correlations", [])
    )
