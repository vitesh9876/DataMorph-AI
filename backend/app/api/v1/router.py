from fastapi import APIRouter
from app.api.v1.upload import router as upload_router
from app.api.v1.analysis import router as analysis_router
from app.api.v1.structuring import router as structuring_router
from app.api.v1.visualization import router as visualization_router
from app.api.v1.ask_data import router as ask_data_router
from app.api.v1.ml_analytics import router as ml_router
from app.api.v1.reports import router as reports_router
from app.api.v1.export import router as export_router

api_v1_router = APIRouter(prefix="/api/v1")

api_v1_router.include_router(upload_router)
api_v1_router.include_router(analysis_router)
api_v1_router.include_router(structuring_router)
api_v1_router.include_router(visualization_router)
api_v1_router.include_router(ask_data_router)
api_v1_router.include_router(ml_router)
api_v1_router.include_router(reports_router)
api_v1_router.include_router(export_router)
