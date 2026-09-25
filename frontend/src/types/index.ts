export interface DocStats {
  pages: number;
  tables: number;
  charts: number;
  sections: number;
  rows: number;
  columns: number;
  inferred_domain?: string;
}

export interface ColumnMeta {
  name: string;
  dtype: string;
  sample_values: any[];
  null_count: number;
  null_percentage: number;
  unique_count: number;
  is_numeric: boolean;
  is_datetime: boolean;
  is_categorical: boolean;
}

export interface FileAnalysis {
  file_id: string;
  filename: string;
  file_type: string;
  file_size: number;
  data_type: string;
  raw_text?: string;
  doc_stats: DocStats;
  topics: string[];
  entities: { column: string; type: string; unique_values_count: number }[];
  ai_understanding: string;
  quality_score: number;
  columns_meta: ColumnMeta[];
  sample_data: Record<string, any>[];
}

export interface TimelineStep {
  step_id: string;
  label: string;
  status: 'waiting' | 'active' | 'completed' | 'error';
  timestamp?: string;
  detail?: string;
}

export interface FileProcessingStatus {
  file_id: string;
  status: 'uploaded' | 'processing' | 'ready' | 'error';
  current_step: string;
  progress: number;
  timeline: TimelineStep[];
  error?: string;
}

export interface CleaningRecommendation {
  id: string;
  rule_type: string;
  title: string;
  description: string;
  target_column?: string | null;
  suggested_action: string;
  status: 'pending' | 'accepted' | 'rejected';
  impact_score_gain: number;
  before_preview: any[];
  after_preview: any[];
}

export interface QualityBreakdown {
  completeness: number;
  consistency: number;
  uniqueness: number;
  validity: number;
  overall_score: number;
}

export interface StructuringOverview {
  file_id: string;
  dataset_id: string;
  total_rows_raw: number;
  total_rows_clean: number;
  total_columns: number;
  raw_sample: Record<string, any>[];
  structured_sample: Record<string, any>[];
  quality_score_before: number;
  quality_score_after: number;
  quality_breakdown: QualityBreakdown;
  recommendations: CleaningRecommendation[];
}

export interface ChartConfig {
  chart_type: string;
  title: string;
  x_axis?: string | null;
  y_axis?: string | null;
  group_by?: string | null;
  aggregation?: string;
  color_palette?: string;
}

export interface VisualizationCardData {
  id: string;
  title: string;
  chart_type: 'line' | 'bar' | 'horizontal_bar' | 'pie' | 'donut' | 'scatter' | 'area' | 'radar' | 'composed' | 'treemap';
  confidence_score: number;
  reason: string;
  chart_config: ChartConfig;
  chart_data: Record<string, any>[];
  is_selected?: boolean;
}

export interface AskDataMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  structured_data?: Record<string, any>[] | null;
  suggested_chart?: VisualizationCardData | null;
  citations?: string[];
  timestamp: string;
}

export interface AnomalyItem {
  row_index: number;
  anomaly_score: number;
  severity: 'high' | 'medium' | 'low';
  reasons: string[];
  row_data: Record<string, any>;
}

export interface AnomalyDetectionData {
  file_id: string;
  total_anomalies: number;
  anomaly_percentage: number;
  algorithm: string;
  anomalies: AnomalyItem[];
}

export interface ForecastPoint {
  date: string;
  actual?: number | null;
  predicted?: number | null;
  lower_bound?: number | null;
  upper_bound?: number | null;
}

export interface ForecastData {
  date_column: string;
  value_column: string;
  model_name: string;
  forecast_data: ForecastPoint[];
  summary_insight: string;
}

export interface ReportSection {
  id: string;
  section_type: string;
  title: string;
  content: string;
  charts?: ChartConfig[];
  chart_data?: Record<string, any>[];
  chart_type?: string;
  table_data?: Record<string, any>[];
  table_columns?: string[];
  segment_name?: string;
  order: number;
  is_visible: boolean;
}

export interface ReportData {
  id: string;
  file_id: string;
  title: string;
  template_type: string;
  sections: ReportSection[];
  selected_visualizations: VisualizationCardData[];
  created_at: string;
  updated_at: string;
}
