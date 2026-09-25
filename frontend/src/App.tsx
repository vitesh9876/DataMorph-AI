import React, { useState, useEffect } from 'react';
import { Navbar } from './components/Navbar';
import { NeuralBackground } from './components/NeuralBackground';
import { IntroductionView } from './components/IntroductionView';
import { UploadWorkspace } from './components/UploadWorkspace';
import { DataMorphWorkspace } from './components/DataMorphWorkspace';
import { api } from './services/api';
import type {
  FileAnalysis,
  FileProcessingStatus,
  StructuringOverview,
  VisualizationCardData,
  ReportData,
  ReportSection,
} from './types';

export function App() {
  const [activeTab, setActiveTab] = useState<string>('intro');
  const [isBackendConnected, setIsBackendConnected] = useState<boolean>(false);
  const [activeFileId, setActiveFileId] = useState<string | null>(null);
  const [processingStatus, setProcessingStatus] = useState<FileProcessingStatus | null>(null);
  const [fileAnalysis, setFileAnalysis] = useState<FileAnalysis | null>(null);
  const [structuringData, setStructuringData] = useState<StructuringOverview | null>(null);
  const [recommendedCharts, setRecommendedCharts] = useState<VisualizationCardData[]>([]);
  const [availableColumns, setAvailableColumns] = useState<string[]>([]);
  const [selectedCharts, setSelectedCharts] = useState<VisualizationCardData[]>([]);
  const [selectedTableSegments, setSelectedTableSegments] = useState<string[]>(['all']);
  const [reportData, setReportData] = useState<ReportData | null>(null);
  const [uploadError, setUploadError] = useState<string | null>(null);

  // Check Backend Connection Health
  useEffect(() => {
    const checkConnection = async () => {
      const healthy = await api.checkHealth();
      setIsBackendConnected(healthy);
    };
    checkConnection();
    const interval = setInterval(checkConnection, 8000);
    return () => clearInterval(interval);
  }, []);

  // Poll File Processing Status when processing
  useEffect(() => {
    if (!activeFileId || processingStatus?.status !== 'processing') return;

    const interval = setInterval(async () => {
      try {
        const status = await api.getFileStatus(activeFileId);
        setProcessingStatus(status);

        if (status.status === 'ready') {
          clearInterval(interval);
          await loadAllFileData(activeFileId);
          setTimeout(() => {
            setActiveTab('workspace');
          }, 400);
        } else if (status.status === 'error') {
          clearInterval(interval);
          setUploadError(status.error || 'Pipeline encountered an error while analyzing this file.');
        }
      } catch (err: any) {
        console.error('Status poll error:', err);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [activeFileId, processingStatus?.status]);

  // Load all artifacts for a file
  const loadAllFileData = async (fileId: string) => {
    try {
      const [analysis, structuring, viz] = await Promise.all([
        api.getFileAnalysis(fileId),
        api.getStructuringOverview(fileId),
        api.getVisualizations(fileId),
      ]);

      setFileAnalysis(analysis);
      setStructuringData(structuring);
      setRecommendedCharts(viz.recommended_charts || []);
      setAvailableColumns(viz.available_columns || []);

      // Pre-select top high confidence charts
      const topSelected = (viz.recommended_charts || []).filter((c) => c.is_selected).slice(0, 4);
      setSelectedCharts(topSelected);

      // Generate Report with error boundary
      try {
        const rep = await api.generateReport(
          fileId, 
          `${analysis.filename} Visual Report`, 
          'professional', 
          topSelected.map(c => c.id)
        );
        setReportData(rep);
      } catch (repErr) {
        console.warn('Report generation fallback initialized:', repErr);
        setReportData({
          id: 'report_' + fileId,
          file_id: fileId,
          title: `${analysis.filename} Visual Report`,
          template_type: 'professional',
          sections: [
            {
              id: 'sec_title',
              section_type: 'title_page',
              title: `${analysis.filename} Visual Report`,
              content: `Automated analysis for ${analysis.filename}`,
              charts: [],
              order: 0,
              is_visible: true,
            },
            {
              id: 'sec_summary',
              section_type: 'executive_summary',
              title: 'Data Summary & Key Insights',
              content: analysis.ai_understanding,
              charts: [],
              order: 1,
              is_visible: true,
            },
            {
              id: 'sec_table_all',
              section_type: 'structured_table',
              title: 'Structured Dataset: All Combined Records',
              content: 'Verified structured tabular data records and measurements.',
              charts: [],
              order: 50,
              is_visible: true,
            }
          ],
          selected_visualizations: topSelected,
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
        });
      }
    } catch (err: any) {
      console.error('Error loading file data:', err);
      setUploadError('Failed to load structured file data. Please re-upload or try again.');
    }
  };

  // Upload Handler
  const handleFileUpload = async (file: File) => {
    try {
      setUploadError(null);
      const res = await api.uploadFile(file);
      setActiveFileId(res.file_id);
      setProcessingStatus({
        file_id: res.file_id,
        status: 'processing',
        current_step: 'detecting_structure',
        progress: 15,
        timeline: [
          { step_id: '1', label: 'File Upload & Format Validation', status: 'completed' },
          { step_id: '2', label: 'Document & Unstructured Data Scanning', status: 'active' },
          { step_id: '3', label: 'Extracting Metrics & Building Table Schema', status: 'waiting' },
          { step_id: '4', label: 'Data Cleaning & Normalization', status: 'waiting' },
          { step_id: '5', label: 'Generating AI Insights & Visualizations', status: 'waiting' },
        ],
      });
      setActiveTab('workspace');
    } catch (err: any) {
      setUploadError(err?.response?.data?.detail || err.message || 'File upload failed');
    }
  };

  // Sample data quick loader from Introduction Page
  const handleLoadSample = (sampleType: 'business' | 'clinical') => {
    let content = '';
    let filename = '';
    if (sampleType === 'clinical') {
      filename = 'raw_lab_test_results.txt';
      content = `PATIENT CLINICAL EVALUATION REPORT - UNSTRUCTURED NOTES
Patient ID: PT-90482 | Date of Evaluation: 2026-08-14
Fasting blood glucose was recorded at 98 mg/dL, showing optimal glycemic control.
Total serum cholesterol reached 215 mg/dL (slightly elevated baseline).
HDL cholesterol measured at 54 mg/dL with LDL cholesterol around 132 mg/dL.
Hemoglobin count stood at 14.8 g/dL and platelet count was 245 K/uL.
Systolic Blood Pressure measured 122 mmHg, diastolic measured 78 mmHg.
Body Mass Index calculated at 24.2 kg/m2 with resting pulse 68 bpm.`;
    } else {
      filename = 'unstructured_business_notes.txt';
      content = `QUARTERLY BUSINESS PERFORMANCE & REGIONAL METRICS
Q3 Executive Summary Notes:
Europe West enterprise region delivered €620,000 in gross recurring revenue.
Latin America branch generated $195,000 with strong customer retention.
Our overall operating expenses stood at $420,000, representing healthy cost control.
Research and Development investments accounted for $210,000 USD.
Hardware shipments totaled 14,200 units across regional hubs.`;
    }

    const blob = new Blob([content], { type: 'text/plain' });
    const file = new File([blob], filename, { type: 'text/plain' });
    handleFileUpload(file);
  };

  // Toggle chart selection for reports
  const handleToggleSelectChart = (chart: VisualizationCardData) => {
    setSelectedCharts((prev) => {
      const exists = prev.some((c) => c.id === chart.id);
      const updated = exists ? prev.filter((c) => c.id !== chart.id) : [...prev, chart];
      
      // Sync into report
      if (activeFileId) {
        api.generateReport(
          activeFileId,
          reportData?.title || 'Visual Report',
          reportData?.template_type || 'professional',
          updated.map(c => c.id)
        ).then(setReportData).catch(() => {});
      }
      return updated;
    });
  };

  // Toggle Table Category / Sub-Table selection for reports
  const handleToggleSelectTableSegment = (segment: string) => {
    setSelectedTableSegments((prev) => {
      const exists = prev.includes(segment);
      const next = exists ? prev.filter((s) => s !== segment) : [...prev, segment];

      // Automatically sync table sections into reportData
      if (reportData && structuringData) {
        const sample = structuringData.structured_sample || fileAnalysis?.sample_data || [];
        const cleanCols = sample.length ? Object.keys(sample[0]) : [];
        const segmentCol = cleanCols.find((c) =>
          ['category', 'test_category', 'segment', 'product_category', 'department', 'region', 'type', 'section'].includes(c.toLowerCase())
        ) || null;

        const nonTableSections = reportData.sections.filter((s) => s.section_type !== 'structured_table');

        const tableSections: ReportSection[] = next.map((seg, idx) => {
          const segData = (seg === 'all' || !segmentCol)
            ? sample
            : sample.filter((r) => String(r[segmentCol]).toLowerCase() === seg.toLowerCase());

          return {
            id: `sec_table_${seg.replace(/[^a-zA-Z0-9]/g, '_')}`,
            section_type: 'structured_table',
            title: seg === 'all' ? 'Structured Dataset: All Combined Records' : `Structured Sub-Table: ${seg}`,
            content: `Verified structured records for ${seg} (${segData.length} records).`,
            segment_name: seg,
            table_data: segData,
            table_columns: cleanCols,
            charts: [],
            order: 50 + idx,
            is_visible: true,
          };
        });

        const updatedSections = [...nonTableSections, ...tableSections];
        setReportData({
          ...reportData,
          sections: updatedSections,
        });

        api.updateReport(reportData.id, { sections: updatedSections }).catch(() => {});
      }

      return next;
    });
  };

  // Generate Custom Chart
  const handleGenerateCustomChart = async (config: {
    chart_type: string;
    x_axis: string;
    y_axis?: string;
    aggregation?: string;
  }) => {
    if (!activeFileId) return;
    try {
      const newChart = await api.generateCustomChart(activeFileId, config);
      setRecommendedCharts((prev) => [newChart, ...prev]);
      setSelectedCharts((prev) => [newChart, ...prev]);
    } catch (err: any) {
      alert('Could not generate chart: ' + err.message);
    }
  };

  // Export Report
  const handleExport = async (format: string) => {
    if (!reportData) throw new Error('No active report generated');
    return await api.exportReport(reportData.id, format, reportData.template_type);
  };

  // Reset workspace for a new file
  const handleReset = () => {
    setActiveFileId(null);
    setProcessingStatus(null);
    setFileAnalysis(null);
    setStructuringData(null);
    setRecommendedCharts([]);
    setSelectedCharts([]);
    setSelectedTableSegments(['all']);
    setReportData(null);
    setUploadError(null);
    setActiveTab('workspace');
  };

  return (
    <div className="min-h-screen bg-background text-on-surface flex flex-col selection:bg-primary/20">
      <NeuralBackground />

      {uploadError && (
        <div className="max-w-4xl mx-auto mt-4 px-4 w-full">
          <div className="p-4 rounded-2xl bg-red-950/40 border border-red-500/30 text-red-300 text-xs font-mono flex items-center justify-between shadow-sm">
            <span>Error: {uploadError}</span>
            <button onClick={() => setUploadError(null)} className="underline ml-2">Dismiss</button>
          </div>
        </div>
      )}

      <main className="flex-1">
        {/* View 1: Standalone Animated Introduction Page */}
        {activeTab === 'intro' && (
          <IntroductionView
            onGetStarted={() => setActiveTab('workspace')}
          />
        )}

        {/* View 2: Standalone DataMorph AI Workspace */}
        {activeTab === 'workspace' && (
          (!activeFileId || !fileAnalysis) ? (
            <UploadWorkspace
              onFileUpload={handleFileUpload}
              processingStatus={processingStatus}
              onProceedToAnalysis={() => setActiveTab('workspace')}
              onBackToIntro={() => setActiveTab('intro')}
              activeFileName={fileAnalysis?.filename}
            />
          ) : (
            <DataMorphWorkspace
              analysis={fileAnalysis}
              structuring={structuringData}
              recommendedCharts={recommendedCharts}
              availableColumns={availableColumns}
              selectedCharts={selectedCharts}
              selectedTableSegments={selectedTableSegments}
              reportData={reportData}
              onToggleSelectChart={handleToggleSelectChart}
              onToggleSelectTableSegment={handleToggleSelectTableSegment}
              onGenerateCustomChart={handleGenerateCustomChart}
              onExport={handleExport}
              onBackToIntro={() => setActiveTab('intro')}
              onNewFileUpload={handleReset}
            />
          )
        )}
      </main>

      {/* Modern Status Footer */}
      <footer className="border-t border-white/5 bg-surface-container-lowest/60 py-5 px-4 text-center text-xs text-outline font-mono">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row items-center justify-between gap-3">
          <span>DataMorph AI • Autonomous Data Structuring & Visual Intelligence</span>
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5">
              <span className={`w-2 h-2 rounded-full ${isBackendConnected ? 'bg-emerald-400' : 'bg-amber-400'}`} />
              {isBackendConnected ? 'FastAPI Backend Online' : 'Connecting to API...'}
            </span>
          </div>
        </div>
      </footer>
    </div>
  );
}
export default App;
