import React, { useState } from 'react';
import { 
  BrainCircuit, 
  Layers, 
  Table, 
  BarChart3, 
  LineChart as LineChartIcon,
  PieChart as PieChartIcon,
  Sparkles, 
  ArrowRight, 
  CheckCircle2, 
  Database,
  Tag,
  Cpu,
  Download,
  MessageSquareCode,
  FileSpreadsheet,
  FileText,
  TrendingUp,
  AlertTriangle,
  Search,
  Filter
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
  AreaChart, 
  Area, 
  ScatterChart, 
  Scatter, 
  XAxis, 
  YAxis, 
  Tooltip, 
  CartesianGrid 
} from 'recharts';
import { motion } from 'framer-motion';
import type { FileAnalysis, StructuringOverview, VisualizationCardData } from '../types';

interface AIAnalysisViewProps {
  analysis: FileAnalysis;
  structuring: StructuringOverview | null;
  recommendedCharts: VisualizationCardData[];
  onProceedToMorphing: () => void;
  onProceedToVisualizations: () => void;
  onProceedToChat: () => void;
  onProceedToReport: () => void;
  onExportCleanData?: () => void;
}

export const AIAnalysisView: React.FC<AIAnalysisViewProps> = ({
  analysis,
  structuring,
  recommendedCharts,
  onProceedToMorphing,
  onProceedToVisualizations,
  onProceedToChat,
  onProceedToReport,
}) => {
  const [dataTab, setDataTab] = useState<'structured' | 'raw' | 'narrative'>('structured');
  const [searchTerm, setSearchTerm] = useState('');

  const statCards = [
    { label: 'Total Rows', value: analysis.doc_stats.rows.toLocaleString(), icon: Database, color: 'text-indigo-400 bg-indigo-500/10 border-indigo-500/20' },
    { label: 'Dimensions', value: analysis.doc_stats.columns, icon: Cpu, color: 'text-rose-400 bg-rose-500/10 border-rose-500/20' },
    { label: 'Extracted Tables', value: analysis.doc_stats.tables, icon: Table, color: 'text-purple-400 bg-purple-500/10 border-purple-500/20' },
    { label: 'Quality Score', value: `${Math.round(analysis.quality_score)}%`, icon: CheckCircle2, color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20' },
    { label: 'AI Charts', value: recommendedCharts.length, icon: BarChart3, color: 'text-amber-400 bg-amber-500/10 border-amber-500/20' },
    { label: 'Topics Found', value: analysis.topics.length, icon: Tag, color: 'text-blue-400 bg-blue-500/10 border-blue-500/20' },
  ];

  const chartColors = ['#2e5bff', '#943fe2', '#b8c3ff', '#4ade80', '#fbbf24', '#f87171', '#38bdf8'];

  const cleanSample = structuring?.structured_sample || analysis.sample_data || [];
  const rawSample = structuring?.raw_sample || analysis.sample_data || [];
  const cleanCols = cleanSample.length > 0 ? Object.keys(cleanSample[0]) : [];
  const rawCols = rawSample.length > 0 ? Object.keys(rawSample[0]) : [];

  const filteredCleanSample = cleanSample.filter(row => 
    Object.values(row).some(v => String(v).toLowerCase().includes(searchTerm.toLowerCase()))
  );

  const renderDashboardChart = (card: VisualizationCardData) => {
    const data = card.chart_data || [];
    if (!data.length) return <div className="h-44 flex items-center justify-center text-xs text-outline">No preview data</div>;

    const xKey = card.chart_config.x_axis || 'name';
    const yKey = card.chart_config.y_axis || 'value';

    switch (card.chart_type) {
      case 'line':
        return (
          <ResponsiveContainer width="100%" height={200}>
            <LineChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey={xKey} stroke="#8e90a2" fontSize={10} tickLine={false} />
              <YAxis stroke="#8e90a2" fontSize={10} tickLine={false} />
              <Tooltip contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '11px' }} />
              <Line type="monotone" dataKey={yKey} stroke="#2e5bff" strokeWidth={2.5} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        );

      case 'bar':
      case 'horizontal_bar':
        return (
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey={xKey} stroke="#8e90a2" fontSize={10} tickLine={false} />
              <YAxis stroke="#8e90a2" fontSize={10} tickLine={false} />
              <Tooltip contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '11px' }} />
              <Bar dataKey={yKey} fill="#4ade80" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'pie':
      case 'donut':
        return (
          <ResponsiveContainer width="100%" height={200}>
            <PieChart>
              <Tooltip contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '11px' }} />
              <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={card.chart_type === 'donut' ? 40 : 0} outerRadius={65}>
                {data.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={chartColors[index % chartColors.length]} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        );

      case 'area':
        return (
          <ResponsiveContainer width="100%" height={200}>
            <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey={xKey} stroke="#8e90a2" fontSize={10} tickLine={false} />
              <YAxis stroke="#8e90a2" fontSize={10} tickLine={false} />
              <Tooltip contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '11px' }} />
              <Area type="monotone" dataKey={yKey} stroke="#943fe2" fill="#943fe2" fillOpacity={0.3} />
            </AreaChart>
          </ResponsiveContainer>
        );

      case 'scatter':
        return (
          <ResponsiveContainer width="100%" height={200}>
            <ScatterChart margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis type="number" dataKey="x" stroke="#8e90a2" fontSize={10} />
              <YAxis type="number" dataKey="y" stroke="#8e90a2" fontSize={10} />
              <Tooltip contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '11px' }} />
              <Scatter data={data} fill="#f43f5e" />
            </ScatterChart>
          </ResponsiveContainer>
        );

      default:
        return (
          <ResponsiveContainer width="100%" height={200}>
            <BarChart data={data}>
              <XAxis dataKey="name" stroke="#8e90a2" fontSize={10} />
              <YAxis stroke="#8e90a2" fontSize={10} />
              <Tooltip />
              <Bar dataKey="value" fill="#b8c3ff" />
            </BarChart>
          </ResponsiveContainer>
        );
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-8 relative z-10 space-y-8">
      {/* Top Banner: Complete Automated Pipeline Flow */}
      <div className="glass-panel p-4 sm:p-6 rounded-3xl border border-white/10 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
              Raw Data → Cleaned & Structured
            </span>
            <span className="text-xs text-outline font-mono font-semibold">{analysis.filename}</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-on-surface tracking-tight">
            Data Intelligence & Visual Insights Hub
          </h1>
        </div>

        {/* Quick Hub Navigation Actions */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            onClick={onProceedToChat}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold bg-surface-container-high hover:bg-surface-variant text-on-surface border border-white/10 transition-all active:scale-95"
          >
            <MessageSquareCode className="w-3.5 h-3.5 text-primary" />
            <span>Ask AI</span>
          </button>
          <button
            onClick={onProceedToVisualizations}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold bg-surface-container-high hover:bg-surface-variant text-on-surface border border-white/10 transition-all active:scale-95"
          >
            <BarChart3 className="w-3.5 h-3.5 text-tertiary" />
            <span>Visual Studio</span>
          </button>
          <button
            onClick={onProceedToReport}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold bg-gradient-to-r from-primary-container to-tertiary-container hover:from-primary hover:to-secondary text-white shadow-glow transition-all active:scale-95"
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Report & Export Hub</span>
            <ArrowRight className="w-3.5 h-3.5 ml-1" />
          </button>
        </div>
      </div>

      {/* Top 6 KPI Metric Pills */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-6 gap-3">
        {statCards.map((stat, idx) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.04 }}
              className="glass-card p-3.5 rounded-2xl border border-white/5 flex flex-col justify-between"
            >
              <div className="flex items-center justify-between">
                <span className="text-[11px] text-outline font-medium">{stat.label}</span>
                <div className={`p-1 rounded-lg ${stat.color}`}>
                  <Icon className="w-3.5 h-3.5" />
                </div>
              </div>
              <div className="text-xl font-bold font-mono text-on-surface mt-2">
                {stat.value}
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* AI Understanding & Key Insights Summary */}
      <div className="glass-panel p-6 rounded-3xl border border-white/10 relative overflow-hidden space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-xl bg-gradient-to-tr from-primary-container to-tertiary-container text-white shadow-glow">
              <BrainCircuit className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-bold text-base text-on-surface">Key AI Insights & Executive Assessment</h3>
              <span className="text-xs text-outline font-mono">Automated patterns, structure detection & data hygiene</span>
            </div>
          </div>

          <div className="hidden sm:flex items-center gap-2">
            {analysis.topics.map((t) => (
              <span key={t} className="px-2.5 py-0.5 rounded-md text-[11px] font-mono bg-surface-container-high text-primary border border-white/5">
                #{t}
              </span>
            ))}
          </div>
        </div>

        <p className="text-sm text-on-surface-variant leading-relaxed bg-surface-container-lowest/60 p-4 rounded-2xl border border-white/5">
          {analysis.ai_understanding}
        </p>
      </div>

      {/* 📊 Interactive Visualizations Grid */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-primary" />
            <h3 className="font-bold text-lg text-on-surface">
              Auto-Generated Visualizations ({recommendedCharts.length})
            </h3>
          </div>
          <button
            onClick={onProceedToVisualizations}
            className="text-xs font-semibold text-primary hover:underline flex items-center gap-1"
          >
            <span>Open in Full Visual Studio</span>
            <ArrowRight className="w-3 h-3" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {recommendedCharts.slice(0, 6).map((chart) => (
            <motion.div
              key={chart.id}
              initial={{ opacity: 0, scale: 0.98 }}
              animate={{ opacity: 1, scale: 1 }}
              className="glass-panel p-4 sm:p-5 rounded-3xl border border-white/10 hover:border-primary/40 transition-all flex flex-col justify-between"
            >
              <div>
                <div className="flex items-center justify-between gap-2 mb-2">
                  <span className="px-2 py-0.5 rounded-md text-[10px] font-mono font-bold bg-primary-container/20 text-primary border border-primary/30">
                    {chart.confidence_score}% confidence
                  </span>
                  <span className="text-[10px] font-mono uppercase text-outline">
                    {chart.chart_type.replace('_', ' ')}
                  </span>
                </div>
                <h4 className="font-bold text-sm text-on-surface mb-1">{chart.title}</h4>
                <p className="text-[11px] text-on-surface-variant line-clamp-2 mb-3">{chart.reason}</p>

                {/* Render chart */}
                <div className="py-1">{renderDashboardChart(chart)}</div>
              </div>

              <div className="pt-2 border-t border-white/5 flex items-center justify-between text-[10px] font-mono text-outline">
                <span>X: {chart.chart_config.x_axis || 'Dim'}</span>
                <span>Y: {chart.chart_config.y_axis || 'Metric'}</span>
              </div>
            </motion.div>
          ))}
        </div>
      </div>

      {/* 🔄 Structured Dataset & Raw vs Clean Morphing */}
      <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <Table className="w-5 h-5 text-emerald-400" />
            <h3 className="font-bold text-base text-on-surface">
              {dataTab === 'structured' ? 'Clean Structured Dataset' : dataTab === 'raw' ? 'Raw Extracted Input' : 'Preserved Narrative Text'}
            </h3>
          </div>

          {/* Toggle Tabs & Search */}
          <div className="flex flex-wrap items-center gap-2">
            <div className="relative">
              <Search className="w-3.5 h-3.5 absolute left-3 top-2.5 text-outline" />
              <input
                type="text"
                placeholder="Search rows..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="pl-8 pr-3 py-1.5 rounded-xl bg-surface-container-high border border-white/10 text-xs text-on-surface focus:outline-none focus:border-primary w-36 sm:w-48 font-mono"
              />
            </div>

            <div className="flex items-center bg-surface-container-lowest p-1 rounded-xl border border-white/5">
              <button
                onClick={() => setDataTab('structured')}
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                  dataTab === 'structured' ? 'bg-primary text-on-primary shadow-sm' : 'text-outline hover:text-on-surface'
                }`}
              >
                Clean Structured ({cleanSample.length})
              </button>
              <button
                onClick={() => setDataTab('raw')}
                className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                  dataTab === 'raw' ? 'bg-primary text-on-primary shadow-sm' : 'text-outline hover:text-on-surface'
                }`}
              >
                Raw Input ({rawSample.length})
              </button>
              {analysis.raw_text && (
                <button
                  onClick={() => setDataTab('narrative')}
                  className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                    dataTab === 'narrative' ? 'bg-primary text-on-primary shadow-sm' : 'text-outline hover:text-on-surface'
                  }`}
                >
                  Raw Text
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Display Data */}
        {dataTab === 'structured' && (
          <div className="overflow-x-auto max-h-80 border border-emerald-500/20 rounded-2xl bg-emerald-950/10">
            <table className="w-full text-left text-xs font-mono">
              <thead className="sticky top-0 bg-surface-container-high text-emerald-300">
                <tr className="border-b border-white/10">
                  {cleanCols.map((col) => (
                    <th key={col} className="py-2.5 px-3 whitespace-nowrap">{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-on-surface">
                {filteredCleanSample.slice(0, 15).map((row, idx) => (
                  <tr key={idx} className="hover:bg-emerald-500/10">
                    {cleanCols.map((col) => (
                      <td key={col} className="py-2 px-3 whitespace-nowrap font-medium">
                        {String(row[col] ?? '—')}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {dataTab === 'raw' && (
          <div className="overflow-x-auto max-h-80 border border-white/10 rounded-2xl bg-surface-container-lowest/60">
            <table className="w-full text-left text-xs font-mono">
              <thead className="sticky top-0 bg-surface-container-high text-outline">
                <tr className="border-b border-white/10">
                  {rawCols.map((col) => (
                    <th key={col} className="py-2.5 px-3 whitespace-nowrap">{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-on-surface-variant">
                {rawSample.slice(0, 15).map((row, idx) => (
                  <tr key={idx} className="hover:bg-white/5">
                    {rawCols.map((col) => (
                      <td key={col} className="py-2 px-3 whitespace-nowrap">
                        {String(row[col] ?? '—')}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {dataTab === 'narrative' && (
          <div className="p-4 rounded-2xl bg-surface-container-lowest border border-white/5 max-h-80 overflow-y-auto font-mono text-xs text-on-surface-variant whitespace-pre-line leading-relaxed">
            {analysis.raw_text}
          </div>
        )}

        {/* Bottom Bar: Action to review rules or proceed */}
        <div className="pt-2 flex items-center justify-between text-xs text-outline font-mono">
          <span>Displaying sample extracted rows • Quality Rating: {Math.round(analysis.quality_score)}%</span>
          <button
            onClick={onProceedToMorphing}
            className="text-emerald-400 font-semibold hover:underline flex items-center gap-1"
          >
            <span>Review Cleaning Rules & Diffs</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>
      </div>
    </div>
  );
};
