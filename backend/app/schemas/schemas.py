from datetime import datetime
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

# --- Project Schemas ---
class ProjectCreate(BaseModel):
    name: str = "Untitled Workspace"
    description: Optional[str] = None

class ProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- File & Upload Schemas ---
class FileUploadResponse(BaseModel):
    file_id: str
    filename: str
    original_name: str
    file_type: str
    file_size: int
    status: str
    message: str

class TimelineStep(BaseModel):
    step_id: str
    label: str
    status: str # waiting, active, completed, error
    timestamp: Optional[str] = None
    detail: Optional[str] = None

class FileStatusResponse(BaseModel):
    file_id: str
    status: str
    current_step: str
    progress: int
    timeline: List[TimelineStep]
    error: Optional[str] = None

# --- Analysis & Understanding Schemas ---
class DocStats(BaseModel):
    pages: int = 0
    tables: int = 0
    charts: int = 0
    sections: int = 0
    rows: int = 0
    columns: int = 0

class ColumnMeta(BaseModel):
    name: str
    dtype: str
    sample_values: List[Any] = []
    null_count: int = 0
    null_percentage: float = 0.0
    unique_count: int = 0
    is_numeric: bool = False
    is_datetime: bool = False
    is_categorical: bool = False

class FileAnalysisResponse(BaseModel):
    file_id: str
    filename: str
    file_type: str
    file_size: int
    data_type: str # tabular, unstructured, semi-structured
    raw_text: Optional[str] = ""
    doc_stats: DocStats
    topics: List[str] = []
    entities: List[Dict[str, Any]] = []
    ai_understanding: str
    quality_score: float
    columns_meta: List[ColumnMeta] = []
    sample_data: List[Dict[str, Any]] = []

# --- Data Structuring & Cleaning Schemas ---
class CleaningRecommendationItem(BaseModel):
    id: str
    rule_type: str
    title: str
    description: str
    target_column: Optional[str] = None
    suggested_action: str
    status: str # pending, accepted, rejected
    impact_score_gain: float
    before_preview: List[Any] = []
    after_preview: List[Any] = []

class QualityBreakdown(BaseModel):
    completeness: float
    consistency: float
    uniqueness: float
    validity: float
    overall_score: float

class StructuringOverviewResponse(BaseModel):
    file_id: str
    dataset_id: str
    total_rows_raw: int
    total_rows_clean: int
    total_columns: int
    raw_sample: List[Dict[str, Any]]
    structured_sample: List[Dict[str, Any]]
    quality_score_before: float
    quality_score_after: float
    quality_breakdown: QualityBreakdown
    recommendations: List[CleaningRecommendationItem]

class RuleActionRequest(BaseModel):
    recommendation_id: str
    action: str # "accept" or "reject"

class BatchRuleActionRequest(BaseModel):
    actions: List[RuleActionRequest]

# --- Visualization Recommendations Schemas ---
class ChartConfig(BaseModel):
    chart_type: str # line, bar, pie, scatter, area, histogram, radar, boxplot
    title: str
    x_axis: Optional[str] = None
    y_axis: Optional[str] = None
    group_by: Optional[str] = None
    aggregation: Optional[str] = "sum" # sum, avg, count, min, max, none
    color_palette: Optional[str] = "default"

class VisualizationCard(BaseModel):
    id: str
    title: str
    chart_type: str
    confidence_score: int # e.g. 96
    reason: str
    chart_config: ChartConfig
    chart_data: List[Dict[str, Any]]
    is_selected: bool = False

class VisualizationListResponse(BaseModel):
    file_id: str
    recommended_charts: List[VisualizationCard]
    available_columns: List[str]

class CustomChartGenerateRequest(BaseModel):
    chart_type: str
    x_axis: str
    y_axis: Optional[str] = None
    aggregation: Optional[str] = "sum"
    group_by: Optional[str] = None
    title: Optional[str] = None

# --- Ask Your Data Schemas ---
class AskQuestionRequest(BaseModel):
    question: str
    history: Optional[List[Dict[str, str]]] = []

class AskQuestionResponse(BaseModel):
    question: str
    answer: str
    supporting_data: Optional[List[Dict[str, Any]]] = None
    suggested_visualization: Optional[VisualizationCard] = None
    sql_or_code: Optional[str] = None
    citations: List[str] = []

# --- Machine Learning & Analytics Schemas ---
class AnomalyItem(BaseModel):
    row_index: int
    anomaly_score: float
    severity: str # high, medium, low
    reasons: List[str]
    row_data: Dict[str, Any]

class AnomalyDetectionResponse(BaseModel):
    file_id: str
    total_anomalies: int
    anomaly_percentage: float
    algorithm: str # Isolation Forest
    anomalies: List[AnomalyItem]

class ForecastRequest(BaseModel):
    date_column: str
    value_column: str
    periods: int = 12
    frequency: str = "M" # D, W, M, Y

class ForecastPoint(BaseModel):
    date: str
    actual: Optional[float] = None
    predicted: Optional[float] = None
    lower_bound: Optional[float] = None
    upper_bound: Optional[float] = None

class ForecastResponse(BaseModel):
    date_column: str
    value_column: str
    model_name: str
    r2_score: Optional[float] = None
    forecast_data: List[ForecastPoint]
    summary_insight: str

class CorrelationMatrixResponse(BaseModel):
    columns: List[str]
    matrix: List[List[float]]
    strong_correlations: List[Dict[str, Any]]

# --- Report & Builder Schemas ---
class ReportSection(BaseModel):
    id: str
    section_type: str # title_page, executive_summary, dataset_overview, data_quality, key_insights, visualizations, anomalies, conclusion, custom
    title: str
    content: str
    charts: List[ChartConfig] = []
    order: int = 0
    is_visible: bool = True

class ReportCreateRequest(BaseModel):
    file_id: str
    title: str = "DataMorph AI Intelligence Report"
    template_type: str = "professional" # professional, minimal, modern, corporate, research
    selected_chart_ids: List[str] = []

class ReportUpdateRequest(BaseModel):
    title: Optional[str] = None
    template_type: Optional[str] = None
    sections: Optional[List[ReportSection]] = None

class ReportResponse(BaseModel):
    id: str
    file_id: str
    title: str
    template_type: str
    sections: List[ReportSection]
    selected_visualizations: List[VisualizationCard]
    created_at: datetime
    updated_at: datetime

# --- Export Schemas ---
class ExportRequest(BaseModel):
    report_id: str
    format: str # pdf, docx, pptx, html, xlsx
    template_type: Optional[str] = "professional"

class ExportResponse(BaseModel):
    download_url: str
    format: str
    file_name: str
    file_size: int
