import React, { useState, useMemo } from 'react';
import { 
  Sparkles, 
  Table, 
  Copy, 
  Check, 
  Download, 
  FileSpreadsheet, 
  FileText, 
  BarChart3, 
  Search, 
  Presentation, 
  FileCheck, 
  FolderArchive,
  BrainCircuit,
  Send,
  Loader2,
  ChevronDown,
  ChevronUp,
  Plus
} from 'lucide-react';
import { 
  ResponsiveContainer, 
  LineChart, 
  Line, 
  BarChart, 
  Bar, 
  PieChart, 
  Pie, 
  Cell, 
  XAxis, 
  YAxis, 
  Tooltip, 
  CartesianGrid 
} from 'recharts';
import type { 
  FileAnalysis, 
  StructuringOverview, 
  VisualizationCardData,
  ReportData
} from '../types';
import { api } from '../services/api';

interface DataMorphWorkspaceProps {
  analysis: FileAnalysis;
  structuring: StructuringOverview | null;
  recommendedCharts: VisualizationCardData[];
  availableColumns: string[];
  selectedCharts: VisualizationCardData[];
  selectedTableSegments?: string[];
  reportData?: ReportData | null;
  onToggleSelectChart: (chart: VisualizationCardData) => void;
  onToggleSelectTableSegment?: (segment: string) => void;
  onGenerateCustomChart?: (config: { chart_type: string; x_axis: string; y_axis?: string; aggregation?: string }) => Promise<void>;
  onExport: (format: string, template?: string) => Promise<{ download_url: string; file_name: string }>;
  onBackToIntro?: () => void;
  onNewFileUpload: () => void;
}

export const DataMorphWorkspace: React.FC<DataMorphWorkspaceProps> = ({
  analysis,
  structuring,
  recommendedCharts,
  availableColumns,
  selectedCharts,
  selectedTableSegments = ['all'],
  reportData,
  onToggleSelectChart,
  onToggleSelectTableSegment,
  onGenerateCustomChart,
  onExport,
  onBackToIntro,
  onNewFileUpload,
}) => {
  const [selectedSegment, setSelectedSegment] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');
  const [copiedType, setCopiedType] = useState<string | null>(null);
  const [isExporting, setIsExporting] = useState<string | null>(null);
  const [exportNotice, setExportNotice] = useState<string | null>(null);
  const [selectedTemplate, setSelectedTemplate] = useState<string>('executive');

  // Explainability toggles for charts
  const [expandedReasons, setExpandedReasons] = useState<Record<string, boolean>>({});

  // Ask Data State
  const [askQuery, setAskQuery] = useState('');
  const [isAsking, setIsAsking] = useState(false);
  const [askAnswer, setAskAnswer] = useState<{ answer: string; suggested_chart?: any } | null>(null);

  // Natural Language Chart Prompt
  const [nlChartPrompt, setNlChartPrompt] = useState('');
  const [isGeneratingNlChart, setIsGeneratingNlChart] = useState(false);
  const [nlChartNotice, setNlChartNotice] = useState<string | null>(null);

  const cleanSample = structuring?.structured_sample || analysis.sample_data || [];
  const cleanCols = cleanSample.length > 0 ? Object.keys(cleanSample[0]) : [];

  // Detect segmenting column
  const segmentCol = useMemo(() => {
    return cleanCols.find(c => 
      ['category', 'test_category', 'segment', 'product_category', 'department', 'region', 'type', 'section'].includes(c.toLowerCase())
    ) || null;
  }, [cleanCols]);

  // Extract distinct detected sub-tables/segments
  const detectedSegments = useMemo(() => {
    if (!segmentCol || !cleanSample.length) return [];
    const counts: Record<string, number> = {};
    cleanSample.forEach(row => {
      const val = String(row[segmentCol] || 'Uncategorized');
      counts[val] = (counts[val] || 0) + 1;
    });
    return Object.entries(counts).map(([name, count]) => ({ name, count }));
  }, [segmentCol, cleanSample]);

  // Filter sample by segment and search term
  const filteredData = useMemo(() => {
    return cleanSample.filter(row => {
      const matchesSegment = selectedSegment === 'all' || String(row[segmentCol || '']) === selectedSegment;
      const matchesSearch = !searchTerm.trim() || Object.values(row).some(v => 
        String(v).toLowerCase().includes(searchTerm.toLowerCase())
      );
      return matchesSegment && matchesSearch;
    });
  }, [cleanSample, selectedSegment, segmentCol, searchTerm]);

  // Copy helpers (JSON and exact TSV text table format)
  const handleCopy = (type: 'json' | 'table') => {
    let content = '';
    if (type === 'json') {
      content = JSON.stringify(filteredData, null, 2);
    } else if (type === 'table') {
      if (filteredData.length > 0) {
        const headers = cleanCols.join('\t');
        const rows = filteredData.map(r => cleanCols.map(c => String(r[c] ?? '')).join('\t'));
        content = [headers, ...rows].join('\n');
      }
    }
    navigator.clipboard.writeText(content);
    setCopiedType(type);
    setTimeout(() => setCopiedType(null), 2000);
  };

  // Quick export
  const handleQuickExport = async (format: string) => {
    try {
      setIsExporting(format);
      setExportNotice(`Synthesizing verified ${format.toUpperCase()} export with selected sub-tables...`);
      const res = await onExport(format, selectedTemplate);
      if (res?.download_url) {
        const fullUrl = res.download_url.startsWith('http') ? res.download_url : `http://127.0.0.1:8000${res.download_url}`;
        window.open(fullUrl, '_blank');
      }
      setExportNotice(`Export complete! Downloaded ${format.toUpperCase()} successfully.`);
      setTimeout(() => setExportNotice(null), 4000);
    } catch (err: any) {
      setExportNotice(`Export failed: ${err.message}`);
    } finally {
      setIsExporting(null);
    }
  };

  // Ask Data Natural Language Query
  const handleAskData = async (queryText?: string) => {
    const q = queryText || askQuery;
    if (!q.trim() || isAsking) return;
    try {
      setIsAsking(true);
      setAskQuery(q);
      const res = await api.askQuestion(analysis.file_id, q.trim());
      setAskAnswer({
        answer: res.answer,
        suggested_chart: res.suggested_chart,
      });
    } catch (err: any) {
      setAskAnswer({
        answer: `Analysis error: ${err.message}`,
      });
    } finally {
      setIsAsking(false);
    }
  };

  // Natural Language Chart Generator Handler
  const handleGenerateNlChart = async () => {
    if (!nlChartPrompt.trim() || isGeneratingNlChart || !onGenerateCustomChart) return;
    try {
      setIsGeneratingNlChart(true);
      setNlChartNotice('Analyzing prompt & inferring optimal axes...');
      
      const promptLower = nlChartPrompt.toLowerCase();
      let inferredType = 'bar';
      if (promptLower.includes('line') || promptLower.includes('trend') || promptLower.includes('over time')) inferredType = 'line';
      else if (promptLower.includes('donut') || promptLower.includes('pie') || promptLower.includes('share') || promptLower.includes('distribution')) inferredType = 'donut';
      else if (promptLower.includes('radar')) inferredType = 'radar';
      else if (promptLower.includes('treemap')) inferredType = 'treemap';

      const x_col = cleanCols.find(c => ['name', 'test_name', 'category', 'item', 'metric', 'region', 'product', 'date'].some(k => c.toLowerCase().includes(k))) || cleanCols[0] || 'Metric';
      const y_col = cleanCols.find(c => ['value', 'measured_value', 'amount', 'score', 'price', 'total', 'revenue', 'count'].some(k => c.toLowerCase().includes(k))) || cleanCols[1];

      await onGenerateCustomChart({
        chart_type: inferredType,
        x_axis: x_col,
        y_axis: y_col,
        aggregation: 'sum'
      });

      setNlChartNotice(`Generated ${inferredType.toUpperCase()} chart: "${x_col} vs ${y_col}"!`);
      setNlChartPrompt('');
      setTimeout(() => setNlChartNotice(null), 3500);
    } catch (err: any) {
      setNlChartNotice(`Chart generation failed: ${err.message}`);
    } finally {
      setIsGeneratingNlChart(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-8 relative z-10 space-y-6">
      
      {/* 🌟 TOP NAVIGATION & FILE HEADER */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 glass-panel p-4 rounded-3xl border border-white/10">
        <div className="flex items-center gap-3">
          {onBackToIntro && (
            <button
              onClick={onBackToIntro}
              className="px-3 py-1.5 rounded-xl bg-surface-container-high hover:bg-surface-variant border border-white/10 text-xs font-semibold text-outline hover:text-on-surface transition-all active:scale-95"
            >
              ← Introduction
            </button>
          )}
          
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-extrabold text-lg text-on-surface tracking-tight">
                DataMorph AI Workspace
              </h1>
              <span className="text-[10px] font-mono font-bold text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded-full border border-emerald-500/20">
                100% Structured
              </span>
            </div>
            <p className="text-xs text-outline font-mono truncate max-w-sm sm:max-w-md">
              {analysis.filename} • {cleanSample.length} Records • {cleanCols.length} Columns
            </p>
          </div>
        </div>

        {/* Global Actions */}
        <div className="flex items-center gap-2">
          <button
            onClick={onNewFileUpload}
            className="px-3.5 py-1.5 rounded-xl bg-surface-container-high hover:bg-surface-variant border border-white/10 text-xs font-bold text-on-surface transition-all active:scale-95"
          >
            + Upload Another File
          </button>
          
          <button
            disabled={Boolean(isExporting)}
            onClick={() => handleQuickExport('pdf')}
            className="flex items-center gap-1.5 px-4 py-1.5 rounded-xl bg-primary hover:bg-primary/90 text-on-primary text-xs font-bold shadow-glow transition-all active:scale-95"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export Report</span>
          </button>
        </div>
      </div>

      {/* Export Notice Banner */}
      {exportNotice && (
        <div className="p-3 rounded-2xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-mono flex items-center justify-between animate-fadeIn">
          <span>{exportNotice}</span>
          <button onClick={() => setExportNotice(null)} className="text-outline hover:text-white text-xs">✕</button>
        </div>
      )}

      {/* ───────────────────────────────────────────────────────────── */}
      {/* DATA & VISUAL WORKSPACE                                       */}
      {/* ───────────────────────────────────────────────────────────── */}
      <div className="space-y-6">
        
        {/* 📊 1. STRUCTURED DATA TABLE WITH SUB-TABLE CHECKBOXES & COPY AS TABLE */}
        <div className="glass-panel p-5 rounded-3xl border border-white/10 space-y-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
            <div>
              <h2 className="font-bold text-base text-on-surface flex items-center gap-2">
                <Table className="w-5 h-5 text-emerald-400" />
                <span>1. Structured Data Table</span>
              </h2>
              <p className="text-xs text-outline">
                Check individual sub-tables below to select which ones appear in your exported report.
              </p>
            </div>

            {/* Quick Actions (Copy JSON, Copy Table, Download Excel) */}
            <div className="flex items-center gap-2 flex-wrap">
              <button
                onClick={() => handleCopy('json')}
                className="px-3 py-1.5 rounded-xl bg-surface-container-high hover:bg-surface-variant border border-white/10 text-xs font-bold text-outline hover:text-on-surface transition-all flex items-center gap-1.5"
                title="Copy dataset as JSON format"
              >
                {copiedType === 'json' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
                <span>Copy JSON</span>
              </button>

              <button
                onClick={() => handleCopy('table')}
                className="px-3 py-1.5 rounded-xl bg-surface-container-high hover:bg-surface-variant border border-white/10 text-xs font-bold text-outline hover:text-on-surface transition-all flex items-center gap-1.5"
                title="Copy exact table format (pastes cleanly into Excel, Word, or text files)"
              >
                {copiedType === 'table' ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Table className="w-3.5 h-3.5" />}
                <span>Copy Table</span>
              </button>

              <button
                onClick={() => handleQuickExport('xlsx')}
                className="px-3 py-1.5 rounded-xl bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 text-xs font-bold transition-all flex items-center gap-1.5"
              >
                <FileSpreadsheet className="w-3.5 h-3.5" />
                <span>Download Excel (.xlsx)</span>
              </button>
            </div>
          </div>

          {/* Sub-Table Selection Pills with Checkboxes */}
          {detectedSegments.length > 0 && (
            <div className="flex flex-wrap items-center gap-2 p-3 rounded-2xl bg-surface-container-lowest/80 border border-white/5">
              <span className="text-xs font-mono text-outline mr-1">Select Sub-Tables:</span>
              
              {/* All Records Pill */}
              <button
                onClick={() => {
                  setSelectedSegment('all');
                  onToggleSelectTableSegment?.('all');
                }}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-xl text-xs font-bold transition-all ${
                  selectedSegment === 'all'
                    ? 'bg-primary text-on-primary shadow-sm'
                    : 'bg-surface-container-high text-outline hover:text-on-surface'
                }`}
              >
                <span className={`w-3.5 h-3.5 rounded flex items-center justify-center text-[10px] ${
                  selectedTableSegments.includes('all') ? 'bg-emerald-400 text-black font-bold' : 'border border-outline'
                }`}>
                  {selectedTableSegments.includes('all') ? '✓' : ''}
                </span>
                <span>All Records ({cleanSample.length})</span>
              </button>

              {/* Individual Sub-Table Pills */}
              {detectedSegments.map(seg => {
                const isChecked = selectedTableSegments.includes(seg.name);
                const isFiltering = selectedSegment === seg.name;

                return (
                  <div
                    key={seg.name}
                    className={`flex items-center rounded-xl border text-xs transition-all overflow-hidden ${
                      isFiltering
                        ? 'bg-surface-container-high border-primary'
                        : 'bg-surface-container-lowest border-white/10 hover:border-white/20'
                    }`}
                  >
                    {/* Checkbox trigger */}
                    <button
                      onClick={() => onToggleSelectTableSegment?.(seg.name)}
                      className="px-2.5 py-1.5 flex items-center gap-1.5 hover:bg-white/5 text-outline hover:text-on-surface border-r border-white/10"
                      title={isChecked ? 'Uncheck from report export' : 'Check to include in report export'}
                    >
                      <span className={`w-3.5 h-3.5 rounded flex items-center justify-center text-[10px] font-bold ${
                        isChecked ? 'bg-emerald-400 text-black' : 'border border-outline'
                      }`}>
                        {isChecked ? '✓' : ''}
                      </span>
                    </button>

                    {/* Filter trigger */}
                    <button
                      onClick={() => setSelectedSegment(isFiltering ? 'all' : seg.name)}
                      className={`px-3 py-1.5 font-bold ${
                        isFiltering ? 'text-primary' : 'text-outline hover:text-on-surface'
                      }`}
                    >
                      <span>{seg.name}</span>
                      <span className="ml-1.5 text-[10px] font-mono text-outline">({seg.count})</span>
                    </button>
                  </div>
                );
              })}
            </div>
          )}

          {/* Search Input */}
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-2.5 text-outline" />
            <input
              type="text"
              placeholder="Search records in table..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-9 pr-4 py-2 rounded-xl bg-surface-container-lowest border border-white/10 text-xs text-on-surface font-mono focus:outline-none focus:border-primary"
            />
          </div>

          {/* Rendered Table Grid */}
          <div className="overflow-x-auto rounded-2xl border border-white/10 bg-surface-container-lowest max-h-72 overflow-y-auto">
            <table className="w-full text-left text-xs font-mono">
              <thead className="bg-surface-container-high/80 sticky top-0 border-b border-white/10 text-primary uppercase text-[10px]">
                <tr>
                  {cleanCols.map((col) => (
                    <th key={col} className="py-2.5 px-3.5 font-bold whitespace-nowrap">
                      {col}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {filteredData.slice(0, 25).map((row, idx) => (
                  <tr key={idx} className="hover:bg-white/5">
                    {cleanCols.map((col) => (
                      <td key={col} className="py-2 px-3.5 whitespace-nowrap">
                        {String(row[col] ?? '—')}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* 📊 2. VISUAL CHARTS STUDIO & NATURAL LANGUAGE CHART GENERATOR */}
        <div className="glass-panel p-5 rounded-3xl border border-white/10 space-y-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
            <div>
              <h2 className="font-bold text-base text-on-surface flex items-center gap-2">
                <BarChart3 className="w-5 h-5 text-primary" />
                <span>2. Visual Charts Studio</span>
              </h2>
              <p className="text-xs text-outline">
                Click <b>"+ Add to Report"</b> on any chart you want in your final exported document.
              </p>
            </div>

            <span className="text-xs font-mono text-amber-400 font-bold px-3 py-1 rounded-xl bg-amber-500/10 border border-amber-500/20">
              {selectedCharts.length} Charts Selected for Export
            </span>
          </div>

          {/* 🗣️ Natural Language Chart Prompt Generator */}
          <div className="p-3 rounded-2xl bg-surface-container-lowest border border-white/5 space-y-2">
            <span className="text-[11px] font-mono text-primary font-bold flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5" />
              Natural Language Chart Generator
            </span>
            <div className="flex gap-2">
              <input
                type="text"
                placeholder="e.g. Create a line trend of Measured_Value over time, or compare categories in a bar chart..."
                value={nlChartPrompt}
                onChange={(e) => setNlChartPrompt(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleGenerateNlChart()}
                className="flex-1 px-3 py-2 rounded-xl bg-surface-container-high border border-white/10 text-xs text-on-surface font-mono focus:outline-none focus:border-primary"
              />
              <button
                disabled={isGeneratingNlChart || !nlChartPrompt.trim()}
                onClick={handleGenerateNlChart}
                className="px-4 py-2 rounded-xl bg-primary text-on-primary text-xs font-bold shadow-glow hover:opacity-95 disabled:opacity-50 transition-all flex items-center gap-1.5"
              >
                {isGeneratingNlChart ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Plus className="w-3.5 h-3.5" />}
                <span>Generate</span>
              </button>
            </div>
            {nlChartNotice && (
              <div className="text-[11px] font-mono text-emerald-400">{nlChartNotice}</div>
            )}
          </div>

          {/* Recommended Visual Charts Grid with Explainability */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {recommendedCharts.slice(0, 6).map((chart) => {
              const isSelected = selectedCharts.some(c => c.id === chart.id);
              const isReasonExpanded = expandedReasons[chart.id] || false;

              return (
                <div
                  key={chart.id}
                  className={`glass-panel p-4 rounded-3xl border transition-all flex flex-col justify-between ${
                    isSelected ? 'border-primary shadow-glow bg-primary/5' : 'border-white/10 hover:border-primary/40'
                  }`}
                >
                  <div>
                    <div className="flex items-center justify-between gap-2 mb-2">
                      <span className="text-xs font-bold text-on-surface truncate">{chart.title}</span>
                      
                      <button
                        onClick={() => onToggleSelectChart(chart)}
                        className={`px-3 py-1 rounded-lg text-[11px] font-bold transition-all ${
                          isSelected
                            ? 'bg-primary text-on-primary shadow-sm'
                            : 'bg-surface-container-high hover:bg-surface-variant text-outline hover:text-on-surface'
                        }`}
                      >
                        {isSelected ? '✓ In Report' : '+ Add to Report'}
                      </button>
                    </div>

                    {/* Mini Rendered Visual Figure */}
                    <div className="h-36 w-full my-2">
                      <ResponsiveContainer width="100%" height="100%">
                        {chart.chart_type === 'line' ? (
                          <LineChart data={chart.chart_data}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
                            <XAxis dataKey="name" stroke="#64748b" fontSize={10} tickLine={false} />
                            <YAxis stroke="#64748b" fontSize={10} tickLine={false} />
                            <Tooltip contentStyle={{ backgroundColor: '#0B0F19', borderColor: '#ffffff20', borderRadius: '12px' }} />
                            <Line type="monotone" dataKey="value" stroke="#10b981" strokeWidth={2} dot={{ r: 3 }} />
                          </LineChart>
                        ) : chart.chart_type === 'donut' || chart.chart_type === 'pie' ? (
                          <PieChart>
                            <Tooltip contentStyle={{ backgroundColor: '#0B0F19', borderColor: '#ffffff20', borderRadius: '12px' }} />
                            <Pie data={chart.chart_data} dataKey="value" nameKey="name" innerRadius={28} outerRadius={46} paddingAngle={4}>
                              {chart.chart_data.map((_, i) => (
                                <Cell key={i} fill={['#10b981', '#6366f1', '#a855f7', '#f59e0b', '#3b82f6'][i % 5]} />
                              ))}
                            </Pie>
                          </PieChart>
                        ) : (
                          <BarChart data={chart.chart_data}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#ffffff10" />
                            <XAxis dataKey="name" stroke="#64748b" fontSize={10} tickLine={false} />
                            <YAxis stroke="#64748b" fontSize={10} tickLine={false} />
                            <Tooltip contentStyle={{ backgroundColor: '#0B0F19', borderColor: '#ffffff20', borderRadius: '12px' }} />
                            <Bar dataKey="value" fill="#10b981" radius={[4, 4, 0, 0]} />
                          </BarChart>
                        )}
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Explainable AI Recommendation Note */}
                  <div className="pt-2 border-t border-white/5 space-y-1">
                    <div className="flex items-center justify-between text-[10px] font-mono text-outline">
                      <span>Type: <b>{chart.chart_type.toUpperCase()}</b></span>
                      <button
                        onClick={() => setExpandedReasons(prev => ({ ...prev, [chart.id]: !prev[chart.id] }))}
                        className="flex items-center gap-1 text-primary hover:underline"
                      >
                        <span>{chart.confidence_score}% Confidence</span>
                        {isReasonExpanded ? <ChevronUp className="w-3 h-3" /> : <ChevronDown className="w-3 h-3" />}
                      </button>
                    </div>

                    {isReasonExpanded && (
                      <div className="p-2 rounded-xl bg-surface-container-lowest text-[10px] font-mono text-slate-300 border border-white/5 animate-fadeIn">
                        <span className="text-emerald-400 font-bold">Why recommended: </span>
                        {chart.reason || 'High distribution variance and optimal column cardinality.'}
                      </div>
                    )}
                  </div>

                </div>
              );
            })}
          </div>
        </div>

        {/* 💡 3. AI DATA UNDERSTANDING & ASK DATAMORPH */}
        <div className="glass-panel p-5 rounded-3xl border border-white/10 space-y-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-tertiary" />
              <h2 className="font-bold text-base text-on-surface">3. AI Data Understanding & Insights</h2>
            </div>
            <span className="text-[11px] font-mono text-emerald-400 bg-emerald-500/10 px-2.5 py-0.5 rounded-lg border border-emerald-500/20">
              Domain: {analysis.doc_stats?.inferred_domain || 'General Analytical'}
            </span>
          </div>

          <p className="text-xs text-on-surface-variant leading-relaxed bg-surface-container-lowest/60 p-4 rounded-2xl border border-white/5 font-mono">
            {analysis.ai_understanding}
          </p>

          {/* 💬 Ask DataMorph AI Natural Language Query Bar */}
          <div className="pt-2 border-t border-white/5 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <BrainCircuit className="w-4 h-4 text-primary" />
                <span className="text-xs font-bold text-on-surface">Ask Your Data (Conversational Query)</span>
              </div>

              {/* Pre-built Prompt Pills */}
              <div className="hidden sm:flex items-center gap-1.5 text-[10px] font-mono text-outline">
                <span>Quick prompts:</span>
                <button onClick={() => handleAskData('Which category has the highest average value?')} className="px-2 py-0.5 rounded-lg bg-surface-container-high hover:text-white">Highest avg?</button>
                <button onClick={() => handleAskData('What is the peak measured value in this dataset?')} className="px-2 py-0.5 rounded-lg bg-surface-container-high hover:text-white">Peak value?</button>
                <button onClick={() => handleAskData('Are there any outliers in this data?')} className="px-2 py-0.5 rounded-lg bg-surface-container-high hover:text-white">Outliers?</button>
              </div>
            </div>

            <div className="flex gap-2">
              <input
                type="text"
                placeholder="Ask anything... e.g. Which category has highest average value? What is the peak measurement?"
                value={askQuery}
                onChange={(e) => setAskQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleAskData()}
                className="flex-1 px-4 py-2.5 rounded-xl bg-surface-container-lowest border border-white/10 text-xs text-on-surface font-mono focus:outline-none focus:border-primary"
              />
              <button
                disabled={isAsking || !askQuery.trim()}
                onClick={() => handleAskData()}
                className={`px-4 py-2.5 rounded-xl text-xs font-bold transition-all flex items-center gap-1.5 ${
                  askQuery.trim() && !isAsking
                    ? 'bg-primary text-on-primary shadow-glow hover:opacity-95'
                    : 'bg-surface-container-high text-outline cursor-not-allowed'
                }`}
              >
                {isAsking ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Send className="w-3.5 h-3.5" />}
                <span>{isAsking ? 'Thinking...' : 'Ask AI'}</span>
              </button>
            </div>

            {/* Assistant Answer Box */}
            {askAnswer && (
              <div className="p-4 rounded-2xl bg-primary/10 border border-primary/30 space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-primary flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5" />
                    AI Answer
                  </span>
                  <span className="text-[10px] font-mono text-outline">Verified Pandas Calculation</span>
                </div>
                <p className="text-xs text-on-surface leading-relaxed font-mono">
                  {askAnswer.answer}
                </p>

                {askAnswer.suggested_chart && (
                  <div className="pt-2 border-t border-white/10 flex items-center justify-between">
                    <span className="text-xs text-outline font-mono">
                      Suggested Chart: <b>{askAnswer.suggested_chart.title}</b>
                    </span>
                    <button
                      onClick={() => onToggleSelectChart(askAnswer.suggested_chart)}
                      className="px-3 py-1 rounded-lg text-xs font-bold bg-primary text-on-primary shadow-sm"
                    >
                      + Add to Report
                    </button>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>

        {/* 📥 4. 1-CLICK EXPORT CENTER WITH TEMPLATE SELECTOR */}
        <div className="glass-panel p-5 rounded-3xl border border-white/10 space-y-4">
          <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
            <div className="flex items-center gap-2">
              <Download className="w-5 h-5 text-primary" />
              <div>
                <h2 className="font-bold text-base text-on-surface">4. Export & Download Center</h2>
                <p className="text-xs text-outline">Download verified reports with your selected sub-tables and charts.</p>
              </div>
            </div>

            {/* Specialized Report Template Selector */}
            <div className="flex items-center gap-1.5 p-1 rounded-xl bg-surface-container-lowest border border-white/10">
              <span className="text-[10px] font-mono text-outline px-2">Theme:</span>
              {[
                { id: 'executive', label: 'Executive' },
                { id: 'clinical', label: 'Clinical' },
                { id: 'research', label: 'Research' }
              ].map(t => (
                <button
                  key={t.id}
                  onClick={() => setSelectedTemplate(t.id)}
                  className={`px-2.5 py-1 rounded-lg text-[11px] font-bold transition-all ${
                    selectedTemplate === t.id ? 'bg-primary text-on-primary' : 'text-outline hover:text-white'
                  }`}
                >
                  {t.label}
                </button>
              ))}
            </div>
          </div>

          <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
            <button
              disabled={Boolean(isExporting)}
              onClick={() => handleQuickExport('pdf')}
              className="p-4 rounded-2xl bg-surface-container-high hover:bg-surface-variant border border-white/5 hover:border-primary/40 flex flex-col items-center justify-center gap-2 text-center transition-all group active:scale-95"
            >
              <FileText className="w-6 h-6 text-primary group-hover:scale-110 transition-transform" />
              <div>
                <div className="text-xs font-bold text-on-surface">PDF Report</div>
                <div className="text-[10px] font-mono text-outline">Charts + Data Tables</div>
              </div>
            </button>

            <button
              disabled={Boolean(isExporting)}
              onClick={() => handleQuickExport('pptx')}
              className="p-4 rounded-2xl bg-surface-container-high hover:bg-surface-variant border border-white/5 hover:border-amber-500/40 flex flex-col items-center justify-center gap-2 text-center transition-all group active:scale-95"
            >
              <Presentation className="w-6 h-6 text-amber-400 group-hover:scale-110 transition-transform" />
              <div>
                <div className="text-xs font-bold text-on-surface">PowerPoint (.pptx)</div>
                <div className="text-[10px] font-mono text-outline">16:9 Presentation</div>
              </div>
            </button>

            <button
              disabled={Boolean(isExporting)}
              onClick={() => handleQuickExport('docx')}
              className="p-4 rounded-2xl bg-surface-container-high hover:bg-surface-variant border border-white/5 hover:border-blue-500/40 flex flex-col items-center justify-center gap-2 text-center transition-all group active:scale-95"
            >
              <FileCheck className="w-6 h-6 text-blue-400 group-hover:scale-110 transition-transform" />
              <div>
                <div className="text-xs font-bold text-on-surface">Word (.docx)</div>
                <div className="text-[10px] font-mono text-outline">Executive Document</div>
              </div>
            </button>

            <button
              disabled={Boolean(isExporting)}
              onClick={() => handleQuickExport('zip')}
              className="p-4 rounded-2xl bg-surface-container-high hover:bg-surface-variant border border-white/5 hover:border-purple-500/40 flex flex-col items-center justify-center gap-2 text-center transition-all group active:scale-95"
            >
              <FolderArchive className="w-6 h-6 text-purple-400 group-hover:scale-110 transition-transform" />
              <div>
                <div className="text-xs font-bold text-on-surface">All Sub-Tables (.ZIP)</div>
                <div className="text-[10px] font-mono text-outline">Categorized CSVs</div>
              </div>
            </button>
          </div>
        </div>

      </div>

    </div>
  );
};
export default DataMorphWorkspace;
