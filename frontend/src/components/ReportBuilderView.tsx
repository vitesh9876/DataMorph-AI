import React, { useState } from 'react';
import { 
  FileText, 
  Sparkles, 
  Download, 
  CheckCircle2, 
  Edit3, 
  Trash2, 
  Plus, 
  Eye, 
  EyeOff, 
  Check, 
  ArrowRight,
  BarChart3,
  Layers,
  FileSpreadsheet,
  FileCode,
  SlidersHorizontal,
  Table as TableIcon,
  Database
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
  XAxis, 
  YAxis, 
  Tooltip, 
  CartesianGrid 
} from 'recharts';
import { motion } from 'framer-motion';
import type { ReportData, ReportSection, VisualizationCardData } from '../types';
import { api } from '../services/api';

interface ReportBuilderViewProps {
  report: ReportData;
  allCharts?: VisualizationCardData[];
  structuringSample?: any[];
  onUpdateReport: (payload: { title?: string; template_type?: string; sections?: ReportSection[] }) => Promise<void>;
  onProceedToExport: () => void;
}

export const ReportBuilderView: React.FC<ReportBuilderViewProps> = ({
  report,
  allCharts = [],
  structuringSample = [],
  onUpdateReport,
  onProceedToExport,
}) => {
  const [title, setTitle] = useState(report.title);
  const [sections, setSections] = useState<ReportSection[]>(report.sections || []);
  const [editingSectionId, setEditingSectionId] = useState<string | null>(null);
  const [editContent, setEditContent] = useState('');
  const [isExporting, setIsExporting] = useState<string | null>(null);
  const [exportNotice, setExportNotice] = useState<string | null>(null);

  const chartColors = ['#2e5bff', '#943fe2', '#b8c3ff', '#4ade80', '#fbbf24', '#f87171', '#38bdf8', '#f43f5e'];

  const syncReport = async (partial: { title?: string; sections?: ReportSection[] }) => {
    try {
      await onUpdateReport({
        title: partial.title || title,
        template_type: report.template_type,
        sections: partial.sections || sections,
      });
    } catch (err: any) {
      console.warn('Sync notice:', err);
    }
  };

  // Toggle AI Summary Section Visibility
  const isSummaryVisible = sections.find(s => s.section_type === 'executive_summary')?.is_visible ?? true;
  
  const handleToggleSummary = async () => {
    const updated = sections.map(s => {
      if (s.section_type === 'executive_summary') {
        return { ...s, is_visible: !s.is_visible };
      }
      return s;
    });
    setSections(updated);
    await syncReport({ sections: updated });
  };

  // Toggle Structured Table Section Visibility
  const isTableVisible = sections.find(s => s.section_type === 'structured_table')?.is_visible ?? true;

  const handleToggleTable = async () => {
    const tableSection = sections.find(s => s.section_type === 'structured_table');
    let updated = sections;

    if (tableSection) {
      updated = sections.map(s => {
        if (s.section_type === 'structured_table') {
          return { ...s, is_visible: !s.is_visible };
        }
        return s;
      });
    } else {
      // Add structured table section
      const newSec: ReportSection = {
        id: 'sec_table_' + Date.now(),
        section_type: 'structured_table',
        title: 'Structured Dataset Record Table',
        content: 'Verified structured tabular data records and measurements.',
        charts: [],
        order: 50,
        is_visible: true,
      };
      updated = [...sections, newSec];
    }

    setSections(updated);
    await syncReport({ sections: updated });
  };

  const handleToggleSectionVisibility = async (secId: string) => {
    const updated = sections.map(s => s.id === secId ? { ...s, is_visible: !s.is_visible } : s);
    setSections(updated);
    await syncReport({ sections: updated });
  };

  const handleDeleteSection = async (secId: string) => {
    const updated = sections.filter(s => s.id !== secId);
    setSections(updated);
    await syncReport({ sections: updated });
  };

  const handleStartEdit = (sec: ReportSection) => {
    setEditingSectionId(sec.id);
    setEditContent(sec.content);
  };

  const handleSaveEdit = async (secId: string) => {
    const updated = sections.map(s => s.id === secId ? { ...s, content: editContent } : s);
    setSections(updated);
    setEditingSectionId(null);
    await syncReport({ sections: updated });
  };

  // Direct 1-Click Export
  const handleDirectExport = async (format: string) => {
    try {
      setIsExporting(format);
      await syncReport({ title, sections });
      const res = await api.exportReport(report.id, format, report.template_type);
      const link = document.createElement('a');
      link.href = res.download_url;
      link.download = res.file_name;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      setExportNotice(`Exported ${res.file_name} successfully!`);
      setTimeout(() => setExportNotice(null), 4000);
    } catch (e: any) {
      setExportNotice(`Export error: ${e.message}`);
    } finally {
      setIsExporting(null);
    }
  };

  const chartSections = sections.filter(s => s.section_type === 'visualizations');

  // Render chart graphic for section
  const renderSectionChart = (section: any) => {
    let data = section.chart_data || (section.charts && section.charts[0]?.chart_data) || [];
    let type = section.chart_type || (section.charts && section.charts[0]?.chart_type) || 'bar';

    if (!data || !data.length) {
      const candidates = [...(allCharts || []), ...(report.selected_visualizations || [])];
      const match = candidates.find(c => 
        c.title?.toLowerCase().trim() === section.title?.toLowerCase().trim() ||
        section.title?.toLowerCase().includes(c.title?.toLowerCase()) ||
        c.title?.toLowerCase().includes(section.title?.toLowerCase())
      );
      if (match && match.chart_data && match.chart_data.length > 0) {
        data = match.chart_data;
        type = match.chart_type || 'bar';
      }
    }

    if (!data || !data.length) {
      return (
        <div className="h-32 flex items-center justify-center text-xs text-outline font-mono bg-surface-container-lowest/40 rounded-xl border border-white/5">
          Visual Chart Preview
        </div>
      );
    }

    switch (type) {
      case 'pie':
      case 'donut':
        return (
          <ResponsiveContainer width="100%" height={160}>
            <PieChart>
              <Tooltip contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '10px' }} />
              <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={type === 'donut' ? 30 : 0} outerRadius={55}>
                {data.map((_: any, index: number) => (
                  <Cell key={`cell-${index}`} fill={chartColors[index % chartColors.length]} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        );

      case 'line':
        return (
          <ResponsiveContainer width="100%" height={160}>
            <LineChart data={data} margin={{ top: 5, right: 10, left: -25, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="name" stroke="#8e90a2" fontSize={8} tickLine={false} />
              <YAxis stroke="#8e90a2" fontSize={8} tickLine={false} />
              <Tooltip contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '10px' }} />
              <Line type="monotone" dataKey="value" stroke="#2e5bff" strokeWidth={2.5} dot={{ r: 3 }} />
            </LineChart>
          </ResponsiveContainer>
        );

      case 'area':
        return (
          <ResponsiveContainer width="100%" height={160}>
            <AreaChart data={data} margin={{ top: 5, right: 10, left: -25, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="name" stroke="#8e90a2" fontSize={8} tickLine={false} />
              <YAxis stroke="#8e90a2" fontSize={8} tickLine={false} />
              <Tooltip contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '10px' }} />
              <Area type="monotone" dataKey="value" stroke="#943fe2" fill="#943fe2" fillOpacity={0.25} />
            </AreaChart>
          </ResponsiveContainer>
        );

      default:
        return (
          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={data} margin={{ top: 5, right: 10, left: -25, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey="name" stroke="#8e90a2" fontSize={8} tickLine={false} />
              <YAxis stroke="#8e90a2" fontSize={8} tickLine={false} />
              <Tooltip contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '10px' }} />
              <Bar dataKey="value" fill="#4ade80" radius={[3, 3, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        );
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-8 relative z-10 space-y-6">
      {/* Header with DataMorph AI Branding */}
      <div className="glass-panel p-6 rounded-3xl border border-white/10 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-full text-[10px] font-mono font-bold bg-primary-container/20 text-primary border border-primary/30">
              ✨ DATAMORPH AI BRANDED REPORT
            </span>
          </div>
          <h2 className="text-2xl sm:text-3xl font-extrabold text-on-surface tracking-tight">
            Visual Intelligence Report Exporter
          </h2>
          <p className="text-xs text-outline mt-0.5">
            Strictly exports your selected visual charts and structured dataset with DataMorph AI header branding.
          </p>
        </div>

        {/* 1-Click Export Actions */}
        <div className="flex flex-wrap items-center gap-2">
          <button
            disabled={Boolean(isExporting)}
            onClick={() => handleDirectExport('pdf')}
            className="flex items-center gap-1.5 px-4 py-2 rounded-xl text-xs font-bold bg-gradient-to-r from-primary-container to-primary hover:from-primary hover:to-secondary text-white shadow-glow transition-all active:scale-95"
          >
            <Download className="w-3.5 h-3.5" />
            <span>{isExporting === 'pdf' ? 'Generating PDF...' : 'Download PDF'}</span>
          </button>

          <button
            disabled={Boolean(isExporting)}
            onClick={() => handleDirectExport('docx')}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold bg-surface-container-high hover:bg-surface-variant border border-white/10 text-on-surface transition-all active:scale-95"
          >
            <FileText className="w-3.5 h-3.5 text-primary" />
            <span>Word (.docx)</span>
          </button>

          <button
            disabled={Boolean(isExporting)}
            onClick={() => handleDirectExport('pptx')}
            className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold bg-surface-container-high hover:bg-surface-variant border border-white/10 text-on-surface transition-all active:scale-95"
          >
            <FileSpreadsheet className="w-3.5 h-3.5 text-amber-400" />
            <span>PowerPoint (.pptx)</span>
          </button>
        </div>
      </div>

      {exportNotice && (
        <div className="p-3 rounded-xl bg-emerald-950/60 border border-emerald-500/40 text-emerald-300 text-xs font-mono flex items-center justify-between shadow-sm">
          <span className="flex items-center gap-2">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            {exportNotice}
          </span>
          <button onClick={() => setExportNotice(null)} className="underline ml-2">Dismiss</button>
        </div>
      )}

      {/* User Controls: Customization Cards */}
      <div className="glass-panel p-5 rounded-3xl border border-white/10 space-y-4">
        <h3 className="font-bold text-base text-on-surface flex items-center gap-2">
          <Sparkles className="w-4 h-4 text-primary" />
          <span>Report Content Customization</span>
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
          {/* 1. Optional Summarized Text Toggle */}
          <div 
            onClick={handleToggleSummary}
            className={`p-4 rounded-2xl border cursor-pointer transition-all flex items-center justify-between ${
              isSummaryVisible 
                ? 'bg-primary/10 border-primary/40 text-on-surface' 
                : 'bg-surface-container-lowest/60 border-white/5 text-outline'
            }`}
          >
            <div className="flex items-center gap-3">
              <div className={`p-2 rounded-xl ${isSummaryVisible ? 'bg-primary text-on-primary' : 'bg-surface-container text-outline'}`}>
                <FileText className="w-4 h-4" />
              </div>
              <div>
                <span className="font-bold text-xs sm:text-sm block">Include AI Summary</span>
                <span className="text-[10px] text-outline">Executive data findings</span>
              </div>
            </div>
            <div className={`w-5 h-5 rounded-md flex items-center justify-center border ${
              isSummaryVisible ? 'bg-primary border-primary text-on-primary' : 'border-white/20'
            }`}>
              {isSummaryVisible && <Check className="w-3.5 h-3.5" />}
            </div>
          </div>

          {/* 2. Structured Dataset Table Toggle */}
          <div 
            onClick={handleToggleTable}
            className={`p-4 rounded-2xl border cursor-pointer transition-all flex items-center justify-between ${
              isTableVisible 
                ? 'bg-emerald-500/10 border-emerald-500/40 text-on-surface' 
                : 'bg-surface-container-lowest/60 border-white/5 text-outline'
            }`}
          >
            <div className="flex items-center gap-3">
              <div className={`p-2 rounded-xl ${isTableVisible ? 'bg-emerald-600 text-white' : 'bg-surface-container text-outline'}`}>
                <Database className="w-4 h-4" />
              </div>
              <div>
                <span className="font-bold text-xs sm:text-sm block">Structured Dataset</span>
                <span className="text-[10px] text-outline">Include data records table</span>
              </div>
            </div>
            <div className={`w-5 h-5 rounded-md flex items-center justify-center border ${
              isTableVisible ? 'bg-emerald-600 border-emerald-600 text-white' : 'border-white/20'
            }`}>
              {isTableVisible && <Check className="w-3.5 h-3.5" />}
            </div>
          </div>

          {/* 3. Selected Charts Counter Card */}
          <div className="p-4 rounded-2xl border border-white/5 bg-surface-container-lowest/60 flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-400">
                <BarChart3 className="w-4 h-4" />
              </div>
              <div>
                <span className="font-bold text-xs sm:text-sm text-on-surface block">Visual Charts</span>
                <span className="text-[10px] text-outline">Selected charts exported</span>
              </div>
            </div>
            <span className="text-xl font-bold font-mono text-amber-400">{chartSections.length}</span>
          </div>
        </div>
      </div>

      {/* Sections List */}
      <div className="space-y-4">
        <h4 className="font-bold text-sm text-on-surface px-1">
          Export Sections ({sections.filter(s => s.is_visible).length} included)
        </h4>

        {sections.map((section) => {
          if (section.section_type === 'title_page') return null;
          const isVisible = section.is_visible;
          const isEditing = editingSectionId === section.id;

          return (
            <motion.div
              key={section.id}
              initial={{ opacity: 0, y: 8 }}
              animate={{ opacity: 1, y: 0 }}
              className={`glass-panel p-5 rounded-3xl border transition-all ${
                isVisible ? 'border-white/10 bg-surface-container/40' : 'border-white/5 bg-surface-container-lowest/30 opacity-50'
              }`}
            >
              <div className="flex items-center justify-between gap-3 mb-3">
                <div className="flex items-center gap-2">
                  <span className={`text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-md border ${
                    section.section_type === 'visualizations' 
                      ? 'bg-primary-container/20 text-primary border-primary/20' 
                      : section.section_type === 'structured_table'
                      ? 'bg-emerald-500/20 text-emerald-400 border-emerald-500/20'
                      : 'bg-indigo-500/20 text-indigo-300 border-indigo-500/20'
                  }`}>
                    {section.section_type === 'visualizations' 
                      ? '📊 Visual Chart' 
                      : section.section_type === 'structured_table'
                      ? '📋 Structured Table'
                      : '📝 Executive Summary'}
                  </span>
                  <h5 className="font-bold text-base text-on-surface">{section.title}</h5>
                </div>

                <div className="flex items-center gap-1">
                  <button
                    onClick={() => handleToggleSectionVisibility(section.id)}
                    className="p-1.5 rounded-lg hover:bg-white/10 text-outline hover:text-on-surface text-xs"
                    title={isVisible ? 'Hide from Export' : 'Show in Export'}
                  >
                    {isVisible ? <Eye className="w-4 h-4 text-emerald-400" /> : <EyeOff className="w-4 h-4 text-outline" />}
                  </button>

                  <button
                    onClick={() => handleStartEdit(section)}
                    className="p-1.5 rounded-lg hover:bg-white/10 text-outline hover:text-on-surface text-xs"
                    title="Edit Text"
                  >
                    <Edit3 className="w-4 h-4 text-primary" />
                  </button>

                  {section.section_type === 'visualizations' && (
                    <button
                      onClick={() => handleDeleteSection(section.id)}
                      className="p-1.5 rounded-lg hover:bg-red-500/20 text-outline hover:text-red-400 text-xs"
                      title="Remove from Report"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>
              </div>

              {isEditing ? (
                <div className="space-y-2 mt-2">
                  <textarea
                    value={editContent}
                    onChange={(e) => setEditContent(e.target.value)}
                    rows={4}
                    className="w-full p-3 rounded-xl bg-surface-container-high border border-primary/40 text-xs text-on-surface focus:outline-none font-mono"
                  />
                  <div className="flex justify-end gap-2">
                    <button
                      onClick={() => setEditingSectionId(null)}
                      className="px-3 py-1 text-xs text-outline hover:text-on-surface"
                    >
                      Cancel
                    </button>
                    <button
                      onClick={() => handleSaveEdit(section.id)}
                      className="px-3 py-1 text-xs font-bold bg-primary text-on-primary rounded-lg"
                    >
                      Save
                    </button>
                  </div>
                </div>
              ) : (
                <div className="space-y-3">
                  {section.section_type === 'executive_summary' && (
                    <div className="p-4 rounded-2xl bg-surface-container-lowest/70 border border-white/5 text-xs text-on-surface-variant font-mono leading-relaxed">
                      {section.content}
                    </div>
                  )}

                  {section.section_type === 'structured_table' && (() => {
                    const tableRows = (section.table_data && section.table_data.length > 0)
                      ? section.table_data
                      : structuringSample;
                    const tableCols = (section.table_columns && section.table_columns.length > 0)
                      ? section.table_columns
                      : (tableRows.length > 0 ? Object.keys(tableRows[0]) : []);

                    return (
                      <div className="space-y-2.5">
                        <p className="text-xs text-outline font-mono">{section.content}</p>

                        {tableRows.length > 0 ? (
                          <div className="overflow-x-auto max-h-64 border border-emerald-500/30 rounded-2xl bg-emerald-950/20 shadow-inner">
                            <table className="w-full text-left text-xs font-mono">
                              <thead className="sticky top-0 bg-surface-container-high text-emerald-300 shadow-sm border-b border-white/10">
                                <tr>
                                  {tableCols.slice(0, 7).map((col: string) => (
                                    <th key={col} className="py-2.5 px-3 whitespace-nowrap">{col}</th>
                                  ))}
                                </tr>
                              </thead>
                              <tbody className="divide-y divide-white/5 text-on-surface">
                                {tableRows.slice(0, 15).map((row: any, idx: number) => (
                                  <tr key={idx} className="hover:bg-emerald-500/10 transition-colors">
                                    {tableCols.slice(0, 7).map((col: string) => (
                                      <td key={col} className="py-2 px-3 whitespace-nowrap">
                                        {String(row[col] ?? '—')}
                                      </td>
                                    ))}
                                  </tr>
                                ))}
                              </tbody>
                            </table>
                          </div>
                        ) : (
                          <div className="p-4 rounded-xl bg-surface-container-lowest border border-white/5 text-xs text-outline font-mono text-center">
                            No table records available.
                          </div>
                        )}
                      </div>
                    );
                  })()}

                  {section.section_type === 'visualizations' && (
                    <div className="space-y-3">
                      {/* Visual Chart Graphic Representation */}
                      <div className="p-3 rounded-2xl bg-surface-container-lowest/80 border border-white/5">
                        {renderSectionChart(section)}
                      </div>

                      {/* Brief Analytical Insight */}
                      <div className="text-xs text-on-surface-variant font-mono bg-surface-container-high/40 p-3 rounded-xl border border-white/5">
                        {section.content.split('**Data Breakdown:**')[0].replace(/\*\*/g, '')}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </motion.div>
          );
        })}
      </div>
    </div>
  );
};
