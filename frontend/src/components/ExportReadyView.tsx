import React, { useState } from 'react';
import { 
  Download, 
  FileText, 
  FileSpreadsheet, 
  Presentation, 
  FileType, 
  Code2, 
  CheckCircle2, 
  Loader2, 
  ExternalLink,
  Sparkles,
  ShieldCheck,
  Eye
} from 'lucide-react';
import { motion } from 'framer-motion';
import confetti from 'canvas-confetti';
import { ReportData } from '../types';

interface ExportReadyViewProps {
  report: ReportData;
  onExport: (format: string) => Promise<{ download_url: string; file_name: string }>;
}

export const ExportReadyView: React.FC<ExportReadyViewProps> = ({ report, onExport }) => {
  const [exportingFormat, setExportingFormat] = useState<string | null>(null);
  const [downloadSuccess, setDownloadSuccess] = useState<string | null>(null);
  const [previewFormat, setPreviewFormat] = useState('pdf');

  const exportFormats = [
    {
      id: 'pdf',
      title: 'Adobe PDF Document',
      ext: '.pdf',
      icon: FileText,
      desc: 'Executive formatted print document with crisp typography and header rules.',
      color: 'text-red-400 bg-red-500/10 border-red-500/30'
    },
    {
      id: 'docx',
      title: 'Microsoft Word Document',
      ext: '.docx',
      icon: FileType,
      desc: 'Fully editable DOCX with native Word headings, tables, and callouts.',
      color: 'text-blue-400 bg-blue-500/10 border-blue-500/30'
    },
    {
      id: 'pptx',
      title: 'PowerPoint Slide Deck',
      ext: '.pptx',
      icon: Presentation,
      desc: '16:9 widescreen slide presentation ready for executive boardroom briefings.',
      color: 'text-amber-400 bg-amber-500/10 border-amber-500/30'
    },
    {
      id: 'xlsx',
      title: 'Excel Multi-Sheet Workbook',
      ext: '.xlsx',
      icon: FileSpreadsheet,
      desc: 'Structured clean dataset, Data Quality audit log, and metrics tabs.',
      color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/30'
    },
    {
      id: 'html',
      title: 'Standalone Web Report',
      ext: '.html',
      icon: Code2,
      desc: 'Responsive standalone HTML report with custom CSS themes.',
      color: 'text-purple-400 bg-purple-500/10 border-purple-500/30'
    }
  ];

  const handleTriggerExport = async (format: string) => {
    setExportingFormat(format);
    setDownloadSuccess(null);
    try {
      const result = await onExport(format);
      setDownloadSuccess(result.file_name);
      
      // Trigger festive celebration confetti
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });

      // Direct browser download
      const fullUrl = `http://127.0.0.1:8000${result.download_url}`;
      window.open(fullUrl, '_blank');
    } finally {
      setExportingFormat(null);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-10 relative z-10 space-y-8">
      {/* Header */}
      <div className="text-center max-w-2xl mx-auto">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-xs font-mono mb-3">
          <CheckCircle2 className="w-3.5 h-3.5" />
          <span>Intelligence Pipeline Complete</span>
        </div>
        <h1 className="text-3xl sm:text-4xl font-extrabold text-on-surface tracking-tight">
          Export & Deliver Your Report
        </h1>
        <p className="mt-2 text-on-surface-variant text-sm sm:text-base">
          Choose from 5 industry-standard export formats. All files are dynamically compiled from your structured dataset and selected visualizations.
        </p>
      </div>

      {/* Export Formats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
        {exportFormats.map((fmt) => {
          const Icon = fmt.icon;
          const isExporting = exportingFormat === fmt.id;

          return (
            <motion.div
              key={fmt.id}
              whileHover={{ y: -3 }}
              className="glass-panel p-6 rounded-3xl border border-white/10 flex flex-col justify-between hover:border-primary/40 hover:shadow-glow transition-all"
            >
              <div>
                <div className="flex items-center justify-between gap-3 mb-4">
                  <div className={`p-3 rounded-2xl ${fmt.color}`}>
                    <Icon className="w-6 h-6" />
                  </div>
                  <span className="font-mono text-xs font-bold px-2 py-1 rounded-lg bg-surface-container-high text-primary">
                    {fmt.ext}
                  </span>
                </div>

                <h3 className="font-bold text-base text-on-surface mb-1.5">{fmt.title}</h3>
                <p className="text-xs text-on-surface-variant leading-relaxed mb-6">{fmt.desc}</p>
              </div>

              <button
                disabled={isExporting}
                onClick={() => handleTriggerExport(fmt.id)}
                className="w-full py-3 rounded-xl text-xs font-bold bg-primary text-on-primary hover:bg-white transition-all shadow-sm flex items-center justify-center gap-2 active:scale-95 disabled:opacity-50"
              >
                {isExporting ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Compiling {fmt.ext}...</span>
                  </>
                ) : (
                  <>
                    <Download className="w-4 h-4" />
                    <span>Download {fmt.ext}</span>
                  </>
                )}
              </button>
            </motion.div>
          );
        })}
      </div>

      {/* Success Notification Banner */}
      {downloadSuccess && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          className="p-4 rounded-2xl bg-emerald-950/40 border border-emerald-500/30 flex items-center justify-between gap-4 text-xs font-mono"
        >
          <div className="flex items-center gap-2 text-emerald-300">
            <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
            <span>Generated and delivered: <strong>{downloadSuccess}</strong></span>
          </div>
          <span className="text-emerald-400 font-semibold">100% Ready</span>
        </motion.div>
      )}

      {/* Live Document Preview Card */}
      <div className="glass-panel p-8 rounded-3xl border border-white/10 space-y-6">
        <div className="flex items-center justify-between pb-4 border-b border-white/10">
          <div className="flex items-center gap-2.5">
            <Eye className="w-5 h-5 text-primary" />
            <h3 className="font-bold text-base text-on-surface">Executive Document Preview</h3>
          </div>
          <span className="text-xs font-mono text-outline">Theme: {report.template_type.toUpperCase()}</span>
        </div>

        <div className="bg-surface-container-lowest/80 p-8 rounded-2xl border border-white/5 space-y-6 font-sans">
          <div className="border-b border-white/10 pb-4">
            <span className="text-[11px] font-mono uppercase text-primary tracking-widest font-semibold block mb-1">
              DataMorph AI Executive Brief
            </span>
            <h2 className="text-2xl font-bold text-on-surface">{report.title}</h2>
          </div>

          <div className="space-y-6 text-xs text-on-surface-variant">
            {report.sections.filter(s => s.is_visible).slice(0, 4).map((s) => (
              <div key={s.id} className="space-y-1.5">
                <h4 className="font-bold text-sm text-primary">{s.title}</h4>
                <p className="whitespace-pre-line leading-relaxed">{s.content}</p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
