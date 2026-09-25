import React, { useRef } from 'react';
import { 
  Sparkles, 
  ArrowRight, 
  FileText, 
  Cpu, 
  Layers, 
  CheckCircle2, 
  FileSpreadsheet, 
  Presentation, 
  FileType, 
  Code2, 
  FileCode, 
  TrendingUp, 
  Brain,
  UploadCloud,
  FolderOpen
} from 'lucide-react';
import { motion } from 'framer-motion';

interface LandingViewProps {
  onStartUpload: (file?: File) => void;
}

export const LandingView: React.FC<LandingViewProps> = ({ onStartUpload }) => {
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const fileFormats = [
    { ext: 'PDF', label: 'Documents', icon: FileText, color: 'text-red-400 bg-red-500/10 border-red-500/20' },
    { ext: 'CSV', label: 'Tabular', icon: FileSpreadsheet, color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20' },
    { ext: 'XLSX', label: 'Workbooks', icon: FileSpreadsheet, color: 'text-green-400 bg-green-500/10 border-green-500/20' },
    { ext: 'PPTX', label: 'Slides', icon: Presentation, color: 'text-amber-400 bg-amber-500/10 border-amber-500/20' },
    { ext: 'DOCX', label: 'Word Docs', icon: FileType, color: 'text-blue-400 bg-blue-500/10 border-blue-500/20' },
    { ext: 'JSON', label: 'Structured', icon: Code2, color: 'text-yellow-400 bg-yellow-500/10 border-yellow-500/20' },
    { ext: 'XML', label: 'Hierarchical', icon: FileCode, color: 'text-purple-400 bg-purple-500/10 border-purple-500/20' },
    { ext: 'TXT', label: 'Raw Logs', icon: FileText, color: 'text-slate-400 bg-slate-500/10 border-slate-500/20' },
  ];

  const features = [
    {
      icon: Cpu,
      title: 'Hybrid Multi-Format Extraction',
      description: 'PyMuPDF, pdfplumber, openpyxl, and python-pptx ingest complex documents, nested tables, and text hierarchies seamlessly.'
    },
    {
      icon: Layers,
      title: 'Interactive Data Structuring',
      description: 'Intelligent deduplication, currency and date normalization, and category unification with real-time Quality Score gains.'
    },
    {
      icon: TrendingUp,
      title: 'ML Anomaly & Trend Forecasting',
      description: 'Isolation Forest anomaly detection flags multivariate risks; polynomial trend models project future intervals with 95% confidence.'
    },
    {
      icon: Brain,
      title: 'Conversational "Ask Your Data"',
      description: 'Query your data in plain English. Get back factual answers, verified data slices, and auto-generated chart recommendations.'
    }
  ];

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      onStartUpload(file);
    }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      onStartUpload(file);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  return (
    <div 
      onDrop={handleDrop}
      onDragOver={handleDragOver}
      className="relative z-10 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 lg:py-20 flex flex-col items-center"
    >
      <input
        ref={fileInputRef}
        type="file"
        onChange={handleFileChange}
        accept=".pdf,.csv,.xlsx,.xls,.pptx,.ppt,.docx,.doc,.txt,.json,.xml,.log"
        className="hidden"
      />

      {/* Top Badge */}
      <motion.div
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-surface-container-high border border-primary/30 text-primary text-xs font-semibold shadow-glow mb-6"
      >
        <Sparkles className="w-3.5 h-3.5" />
        <span>Next-Generation AI Intelligence Workspace</span>
      </motion.div>

      {/* Hero Header */}
      <motion.h1
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.1 }}
        className="text-4xl sm:text-6xl lg:text-7xl font-extrabold text-center tracking-tight max-w-5xl leading-[1.15]"
      >
        Transform Any Raw File into{' '}
        <span className="text-gradient">Structured Data</span>,{' '}
        <span className="text-gradient-purple">Visual Insights</span> & Reports.
      </motion.h1>

      <motion.p
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.2 }}
        className="mt-6 text-lg sm:text-xl text-on-surface-variant text-center max-w-3xl leading-relaxed"
      >
        Upload PDF, PPTX, Excel, CSV, Word, XML or JSON files. DataMorph AI automatically extracts, structures, runs Machine Learning analytics, and produces professional editable reports exported in multiple formats.
      </motion.p>

      {/* Hero CTA Buttons */}
      <motion.div
        initial={{ opacity: 0, y: 15 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="mt-10 flex flex-wrap items-center justify-center gap-4"
      >
        <button
          onClick={() => fileInputRef.current?.click()}
          className="flex items-center gap-2.5 px-8 py-4 rounded-xl text-base font-bold bg-gradient-to-r from-primary-container via-indigo-600 to-tertiary-container hover:from-primary hover:to-secondary text-white shadow-glow hover:shadow-glow-lg transition-all transform hover:-translate-y-0.5 active:translate-y-0"
        >
          <UploadCloud className="w-5 h-5" />
          <span>Upload Your File to Start</span>
          <ArrowRight className="w-5 h-5" />
        </button>

        <button
          onClick={() => fileInputRef.current?.click()}
          className="flex items-center gap-2.5 px-7 py-4 rounded-xl text-base font-semibold bg-surface-container-high hover:bg-surface-variant text-on-surface border border-white/10 shadow-sm transition-all hover:-translate-y-0.5"
        >
          <FolderOpen className="w-5 h-5 text-primary" />
          <span>Browse File from Computer</span>
        </button>
      </motion.div>

      {/* Floating Animated Morphing Core Showcase */}
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.4, duration: 0.6 }}
        className="w-full max-w-5xl mt-16 p-1 rounded-2xl bg-gradient-to-b from-primary/20 via-tertiary/10 to-transparent shadow-2xl"
      >
        <div className="glass-panel rounded-2xl p-6 sm:p-10 border border-white/10 overflow-hidden relative">
          <div className="absolute top-0 right-0 w-96 h-96 bg-primary/10 rounded-full blur-3xl pointer-events-none" />
          <div className="absolute bottom-0 left-0 w-96 h-96 bg-tertiary/10 rounded-full blur-3xl pointer-events-none" />

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-center relative z-10">
            {/* Raw Input Side */}
            <div className="flex flex-col gap-3 p-5 rounded-xl bg-surface-container-lowest/80 border border-white/5">
              <span className="text-xs font-mono uppercase text-outline tracking-wider flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-red-400" />
                Raw Messy Inputs
              </span>
              <div className="space-y-2 text-xs font-mono text-on-surface-variant/80">
                <div className="p-2 rounded bg-surface-container-high flex justify-between">
                  <span>iphone 15</span>
                  <span className="text-red-400">casing mismatch</span>
                </div>
                <div className="p-2 rounded bg-surface-container-high flex justify-between">
                  <span>$1,200 / ₹1,00,000</span>
                  <span className="text-amber-400">mixed currency</span>
                </div>
                <div className="p-2 rounded bg-surface-container-high flex justify-between">
                  <span>01/16/24 vs 2024-01-16</span>
                  <span className="text-blue-400">date formats</span>
                </div>
              </div>
            </div>

            {/* Glowing AI Transformation Core */}
            <div className="flex flex-col items-center justify-center text-center p-6 rounded-xl bg-gradient-to-b from-primary-container/20 to-tertiary-container/20 border border-primary/30 relative">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-primary-container to-tertiary-container flex items-center justify-center shadow-glow mb-3 animate-pulse">
                <Sparkles className="w-8 h-8 text-white" />
              </div>
              <h3 className="font-bold text-base text-gradient">AI Morphing Engine</h3>
              <p className="text-xs text-outline mt-1">Rule Deduction & ML Normalization</p>
              <div className="mt-3 flex items-center gap-2 text-xs font-mono text-emerald-400 bg-emerald-500/10 px-2.5 py-1 rounded-full border border-emerald-500/20">
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>Quality Score: 68% → 98%</span>
              </div>
            </div>

            {/* Clean Structured Output Side */}
            <div className="flex flex-col gap-3 p-5 rounded-xl bg-surface-container-lowest/80 border border-emerald-500/20 shadow-glow">
              <span className="text-xs font-mono uppercase text-emerald-400 tracking-wider flex items-center gap-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-400" />
                Structured Intelligence
              </span>
              <div className="space-y-2 text-xs font-mono text-on-surface">
                <div className="p-2 rounded bg-emerald-950/40 border border-emerald-500/20 flex justify-between">
                  <span className="font-semibold text-emerald-300">iPhone 15</span>
                  <span className="text-emerald-400">Unified</span>
                </div>
                <div className="p-2 rounded bg-emerald-950/40 border border-emerald-500/20 flex justify-between">
                  <span className="font-semibold text-emerald-300">1200.00 Float</span>
                  <span className="text-emerald-400">Standardized</span>
                </div>
                <div className="p-2 rounded bg-emerald-950/40 border border-emerald-500/20 flex justify-between">
                  <span className="font-semibold text-emerald-300">2024-01-16</span>
                  <span className="text-emerald-400">ISO 8601</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Supported Formats Section */}
      <div className="w-full mt-20 text-center">
        <h2 className="text-xs uppercase tracking-widest text-outline font-semibold mb-6">
          Supported Multi-Format Extraction Engine
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
          {fileFormats.map((fmt) => {
            const Icon = fmt.icon;
            return (
              <div
                key={fmt.ext}
                onClick={() => fileInputRef.current?.click()}
                className="p-3 rounded-xl bg-surface-container-low/70 border border-white/5 hover:border-primary/30 transition-all flex flex-col items-center gap-1.5 group cursor-pointer"
              >
                <div className={`p-2 rounded-lg ${fmt.color}`}>
                  <Icon className="w-4 h-4" />
                </div>
                <span className="font-bold font-mono text-sm text-on-surface">{fmt.ext}</span>
                <span className="text-[11px] text-outline">{fmt.label}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* Core Feature Pillars Grid */}
      <div className="w-full mt-24">
        <div className="text-center max-w-3xl mx-auto mb-12">
          <h2 className="text-3xl sm:text-4xl font-bold tracking-tight text-on-surface">
            Engineered for Precision & Speed
          </h2>
          <p className="mt-3 text-on-surface-variant">
            DataMorph AI replaces complex data engineering workflows with a unified, self-healing intelligence workspace.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {features.map((feat, idx) => {
            const Icon = feat.icon;
            return (
              <div
                key={idx}
                className="glass-card glass-card-hover p-8 rounded-2xl border border-white/5 flex flex-col gap-4 relative overflow-hidden"
              >
                <div className="w-12 h-12 rounded-xl bg-primary/10 border border-primary/20 flex items-center justify-center text-primary">
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="text-xl font-bold text-on-surface">{feat.title}</h3>
                <p className="text-on-surface-variant text-sm leading-relaxed">{feat.description}</p>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
