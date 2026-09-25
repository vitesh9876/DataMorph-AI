import axios from 'axios';
import type {
  FileAnalysis,
  FileProcessingStatus,
  StructuringOverview,
  VisualizationCardData,
  AskDataMessage,
  AnomalyDetectionData,
  ForecastData,
  ReportData
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || '/api/v1';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 60000,
});

export const api = {
  // Check Backend Health
  checkHealth: async (): Promise<boolean> => {
    try {
      const res = await axios.get('/health', { timeout: 3000 });
      return res.status === 200;
    } catch {
      try {
        const directRes = await axios.get('http://127.0.0.1:8000/health', { timeout: 3000 });
        return directRes.status === 200;
      } catch {
        return false;
      }
    }
  },

  // Upload File
  uploadFile: async (file: File): Promise<{ file_id: string; filename: string; original_name: string; file_type: string }> => {
    const formData = new FormData();
    formData.append('file', file);
    const res = await apiClient.post('/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
    return res.data;
  },

  // Get Processing Timeline Status
  getFileStatus: async (fileId: string): Promise<FileProcessingStatus> => {
    const res = await apiClient.get(`/upload/${fileId}/status`);
    return res.data;
  },

  // Get AI Analysis & Understanding
  getFileAnalysis: async (fileId: string): Promise<FileAnalysis> => {
    const res = await apiClient.get(`/analysis/${fileId}`);
    return res.data;
  },

  // Get Data Structuring & Recommendations
  getStructuringOverview: async (fileId: string): Promise<StructuringOverview> => {
    const res = await apiClient.get(`/structuring/${fileId}`);
    return res.data;
  },

  // Accept or Reject Cleaning Recommendation
  applyRuleAction: async (fileId: string, recommendationId: string, action: 'accept' | 'reject'): Promise<StructuringOverview> => {
    const res = await apiClient.post(`/structuring/${fileId}/rules/action`, {
      recommendation_id: recommendationId,
      action,
    });
    return res.data;
  },

  // Get Recommended Visualizations
  getVisualizations: async (fileId: string): Promise<{ file_id: string; recommended_charts: VisualizationCardData[]; available_columns: string[] }> => {
    const res = await apiClient.get(`/visualizations/${fileId}`);
    return res.data;
  },

  // Generate Custom Chart
  generateCustomChart: async (fileId: string, payload: { chart_type: string; x_axis: string; y_axis?: string; aggregation?: string }): Promise<VisualizationCardData> => {
    const res = await apiClient.post(`/visualizations/${fileId}/custom`, payload);
    return res.data;
  },

  // Ask Your Data NL Chat
  askQuestion: async (fileId: string, question: string): Promise<any> => {
    const res = await apiClient.post(`/ask-data/${fileId}`, { question });
    return res.data;
  },

  // Get Chat History
  getChatHistory: async (fileId: string): Promise<AskDataMessage[]> => {
    const res = await apiClient.get(`/ask-data/${fileId}/history`);
    return res.data;
  },

  // ML Anomaly Detection
  getAnomalies: async (fileId: string): Promise<AnomalyDetectionData> => {
    const res = await apiClient.get(`/ml/${fileId}/anomalies`);
    return res.data;
  },

  // ML Time-Series Forecasting
  generateForecast: async (fileId: string, dateCol: string, valCol: string, periods = 12): Promise<ForecastData> => {
    const res = await apiClient.post(`/ml/${fileId}/forecast`, {
      date_column: dateCol,
      value_column: valCol,
      periods,
    });
    return res.data;
  },

  // Generate AI Executive Report
  generateReport: async (fileId: string, title: string, templateType = 'professional', selectedChartIds: string[] = []): Promise<ReportData> => {
    const res = await apiClient.post('/reports/generate', {
      file_id: fileId,
      title,
      template_type: templateType,
      selected_chart_ids: selectedChartIds,
    });
    return res.data;
  },

  // Get Report
  getReport: async (reportId: string): Promise<ReportData> => {
    const res = await apiClient.get(`/reports/${reportId}`);
    return res.data;
  },

  // Update Report (reorder, edit text, change template)
  updateReport: async (reportId: string, payload: { title?: string; template_type?: string; sections?: any[] }): Promise<ReportData> => {
    const res = await apiClient.put(`/reports/${reportId}`, payload);
    return res.data;
  },

  // Export Report to PDF / DOCX / PPTX / XLSX / HTML
  exportReport: async (reportId: string, format: string, templateType = 'professional'): Promise<{ download_url: string; format: string; file_name: string; file_size: number }> => {
    const res = await apiClient.post('/export', {
      report_id: reportId,
      format,
      template_type: templateType,
    });
    return res.data;
  },

  // Export Structured Dataset Directly (CSV, XLSX, JSON, with optional segment)
  exportDatasetDirect: async (fileId: string, format: 'csv' | 'xlsx' | 'json', segment?: string): Promise<{ download_url: string; format: string; file_name: string; file_size: number }> => {
    const url = segment && segment !== 'all' 
      ? `/export/dataset/${fileId}?format=${format}&segment=${encodeURIComponent(segment)}` 
      : `/export/dataset/${fileId}?format=${format}`;
    const res = await apiClient.post(url);
    return res.data;
  },

  // Export All Segments as Separate Files (.ZIP Archive)
  exportDatasetZip: async (fileId: string, format: 'csv' | 'xlsx' | 'json' = 'csv'): Promise<{ download_url: string; format: string; file_name: string; file_size: number }> => {
    const res = await apiClient.post(`/export/dataset/${fileId}/zip-segments?format=${format}`);
    return res.data;
  },

  // Export Multi-Sheet Excel Workbook
  exportDatasetMultiSheet: async (fileId: string): Promise<{ download_url: string; format: string; file_name: string; file_size: number }> => {
    const res = await apiClient.post(`/export/dataset/${fileId}/multi-sheet-excel`);
    return res.data;
  },
};
