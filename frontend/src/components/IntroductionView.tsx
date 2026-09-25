import React from 'react';
import { 
  Sparkles, 
  TableProperties, 
  BarChart3, 
  FileText, 
  Presentation, 
  FileSpreadsheet, 
  CheckCircle2, 
  ArrowRight, 
  Zap, 
  ShieldCheck, 
  Cpu, 
  Database, 
  Layers, 
  FolderArchive,
  Workflow,
  LineChart as LineChartIcon,
  Check,
  Search,
  Lock,
  FileOutput,
  FileCheck2,
  Sliders,
  TrendingUp,
  BrainCircuit
} from 'lucide-react';
import { motion } from 'framer-motion';

interface IntroductionViewProps {
  onGetStarted: () => void;
}

export const IntroductionView: React.FC<IntroductionViewProps> = ({
  onGetStarted,
}) => {
  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 py-12 sm:py-20 relative z-10 space-y-20">
      
      {/* 🌟 1. ENTERPRISE HERO BANNER */}
      <motion.div 
        initial={{ opacity: 0, y: 24 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="text-center space-y-6 max-w-4xl mx-auto"
      >
        {/* Subtle Tech Pill Badge */}
        <motion.div 
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ delay: 0.15, duration: 0.5 }}
          className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-gradient-to-r from-primary/15 via-tertiary/15 to-primary/15 border border-primary/30 shadow-glow backdrop-blur-md"
        >
          <BrainCircuit className="w-4 h-4 text-emerald-400 animate-pulse" />
          <span className="text-xs font-mono font-bold tracking-wide text-gradient">
            DataMorph AI • Autonomous Data Structuring & Intelligence Engine
          </span>
        </motion.div>

        {/* Hero Title */}
        <h1 className="text-4xl sm:text-6xl md:text-7xl font-black tracking-tight text-on-surface leading-[1.08]">
          Transform <span className="text-gradient">Messy Unstructured Files</span> Into Verified <span className="text-emerald-400">Visual Reports</span>
        </h1>

        {/* Clear Brief Explanation of the Application */}
        <p className="text-base sm:text-lg md:text-xl text-on-surface-variant font-medium max-w-3xl mx-auto leading-relaxed">
          DataMorph AI is an intelligent data extraction and reporting workspace. Upload any raw document, clinical record, invoice, or unformatted text — the engine automatically detects schemas, categorizes sub-tables with interactive checkboxes, renders live vector charts, and generates executive <b>PDF</b>, <b>PowerPoint</b>, and <b>Excel</b> exports.
        </p>

        {/* Primary Launch Action */}
        <div className="pt-2 flex flex-col sm:flex-row items-center justify-center gap-4">
          <motion.button
            whileHover={{ scale: 1.03 }}
            whileTap={{ scale: 0.97 }}
            onClick={onGetStarted}
            className="flex items-center gap-3 px-9 py-4 rounded-2xl bg-gradient-to-r from-primary-container via-primary to-secondary text-white font-extrabold text-base shadow-glow hover:opacity-95 transition-all"
          >
            <span>Launch DataMorph Workspace</span>
            <ArrowRight className="w-5 h-5" />
          </motion.button>
        </div>

        {/* Trust Badges Strip */}
        <div className="pt-4 flex flex-wrap items-center justify-center gap-4 text-xs font-mono text-outline">
          <span className="flex items-center gap-1.5">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            Zero Data Retention
          </span>
          <span>•</span>
          <span className="flex items-center gap-1.5">
            <Zap className="w-4 h-4 text-amber-400" />
            Instant Sub-Table Detection
          </span>
          <span>•</span>
          <span className="flex items-center gap-1.5">
            <BarChart3 className="w-4 h-4 text-primary" />
            10+ Visual Chart Archetypes
          </span>
          <span>•</span>
          <span className="flex items-center gap-1.5">
            <FileOutput className="w-4 h-4 text-tertiary" />
            Multi-Format PDF/PPTX/Excel
          </span>
        </div>
      </motion.div>

      {/* 🚀 2. REAL-TIME MULTI-DIMENSIONAL TRANSFORMATION SHOWCASE */}
      <motion.div 
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.25, duration: 0.8 }}
        className="glass-panel p-6 sm:p-8 rounded-3xl border border-white/10 relative overflow-hidden bg-gradient-to-b from-surface-container-lowest/80 to-surface-container-low/40 shadow-2xl"
      >
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-2 mb-6">
          <div>
            <span className="text-[11px] font-mono uppercase tracking-widest text-emerald-400 font-bold">Autonomous Morphing Pipeline</span>
            <h3 className="text-xl sm:text-2xl font-bold text-on-surface">From Unstructured Notes to Production Datasets</h3>
          </div>
          <span className="text-xs font-mono text-outline px-3 py-1 rounded-xl bg-white/5 border border-white/10">
            Real-Time Extraction Flow
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-11 gap-4 items-center">
          
          {/* Left: Raw Unstructured Source */}
          <div className="md:col-span-5 p-5 rounded-2xl bg-black/60 border border-red-500/20 space-y-3">
            <div className="flex items-center justify-between text-xs font-mono text-red-400">
              <span className="flex items-center gap-1.5 font-bold">
                <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse" />
                Raw Unstructured Source
              </span>
              <span className="text-outline text-[11px]">unstructured_notes.txt</span>
            </div>
            <div className="font-mono text-xs text-slate-400 space-y-2 leading-relaxed bg-black/40 p-4 rounded-xl border border-white/5 select-none">
              <p className="text-red-300/90 font-medium">"Patient fasting glucose recorded at 98 mg/dL.</p>
              <p>Total Serum Cholesterol measured 215 mg/dL (Elevated).</p>
              <p>Hemoglobin reached 14.8 g/dL with Blood Pressure at 122/78 mmHg.</p>
              <p className="text-slate-500 text-[11px]">Category: Diagnostic & Clinical. Evaluation verified by Lab..."</p>
            </div>
            <div className="text-[11px] font-mono text-slate-500 flex items-center justify-between">
              <span>Format: Unorganized Text</span>
              <span className="text-red-400/80">0% Structured</span>
            </div>
          </div>

          {/* Center: Autonomous AI Transformation Node */}
          <div className="md:col-span-1 flex flex-col items-center justify-center py-4">
            <motion.div 
              animate={{ rotate: 360 }}
              transition={{ duration: 12, repeat: Infinity, ease: "linear" }}
              className="w-12 h-12 rounded-2xl bg-gradient-to-tr from-primary via-tertiary to-emerald-400 flex items-center justify-center text-white shadow-glow"
            >
              <Sparkles className="w-6 h-6" />
            </motion.div>
            <span className="text-[10px] font-mono text-emerald-400 font-bold mt-2 tracking-wider">MORPH</span>
          </div>

          {/* Right: Verified Structured Dataset & Visuals */}
          <div className="md:col-span-5 p-5 rounded-2xl bg-emerald-950/20 border border-emerald-500/30 space-y-3">
            <div className="flex items-center justify-between text-xs font-mono text-emerald-400">
              <span className="flex items-center gap-1.5 font-bold">
                <CheckCircle2 className="w-4 h-4" />
                Verified Structured Dataset
              </span>
              <span className="text-emerald-300 bg-emerald-500/20 px-2.5 py-0.5 rounded-full text-[10px] font-bold">
                100% Quality Score
              </span>
            </div>
            
            {/* Mini Structured Table Grid */}
            <div className="font-mono text-xs space-y-1.5 overflow-hidden rounded-xl border border-emerald-500/20 bg-surface-container-lowest/60">
              <div className="grid grid-cols-4 gap-1 bg-emerald-900/30 p-2 text-emerald-300 font-bold text-[11px] border-b border-emerald-500/20">
                <span>Metric</span>
                <span>Value</span>
                <span>Unit</span>
                <span>Assessment</span>
              </div>
              <div className="grid grid-cols-4 gap-1 p-2 bg-surface-container-high/40 text-slate-200 text-[11px]">
                <span className="truncate font-semibold">Glucose</span>
                <span className="text-emerald-400 font-bold">98.0</span>
                <span>mg/dL</span>
                <span className="text-emerald-400">Normal</span>
              </div>
              <div className="grid grid-cols-4 gap-1 p-2 bg-surface-container-high/40 text-slate-200 text-[11px]">
                <span className="truncate font-semibold">Cholesterol</span>
                <span className="text-amber-400 font-bold">215.0</span>
                <span>mg/dL</span>
                <span className="text-amber-400">Elevated</span>
              </div>
              <div className="grid grid-cols-4 gap-1 p-2 bg-surface-container-high/40 text-slate-200 text-[11px]">
                <span className="truncate font-semibold">Hemoglobin</span>
                <span className="text-emerald-400 font-bold">14.8</span>
                <span>g/dL</span>
                <span className="text-emerald-400">Optimal</span>
              </div>
            </div>

            <div className="text-[11px] font-mono text-emerald-400 flex items-center justify-between">
              <span>Ready for: Excel, PDF, PPTX & Charts</span>
              <span className="font-bold">4 Columns • 100% Clean</span>
            </div>
          </div>

        </div>
      </motion.div>

      {/* 📚 3. DETAILED EXPLANATION: THE 4 CORE PILLARS OF DATAMORPH */}
      <div className="space-y-8">
        <div className="text-center space-y-2">
          <span className="text-xs font-mono uppercase tracking-widest text-primary font-bold">Comprehensive Capabilities</span>
          <h2 className="text-2xl sm:text-3xl md:text-4xl font-extrabold text-on-surface">
            How DataMorph AI Powers Your Workflow
          </h2>
          <p className="text-sm text-outline max-w-2xl mx-auto">
            Everything required to ingest, structure, analyze, and publish intelligence reports in one streamlined application.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          
          {/* Pillar 1 */}
          <motion.div 
            whileHover={{ y: -4 }}
            className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4 hover:border-primary/40 transition-all bg-gradient-to-br from-surface-container-lowest/80 to-surface-container-high/30"
          >
            <div className="w-12 h-12 rounded-2xl bg-primary/10 border border-primary/20 flex items-center justify-center text-primary shadow-glow">
              <Database className="w-6 h-6" />
            </div>
            <div className="space-y-1">
              <h3 className="text-lg font-bold text-on-surface">1. Universal Document Ingestion & Schema Extraction</h3>
              <p className="text-xs text-outline font-mono">PDF, Word, Excel, CSV, Invoices, Medical Charts, Notes & API Logs</p>
            </div>
            <p className="text-xs sm:text-sm text-on-surface-variant leading-relaxed">
              DataMorph AI uses multi-layer OCR and entity recognition to parse unstructured text. It automatically detects numerical metrics, headers, column names, units, and dates — converting raw text into normalized tabular datasets with zero manual data entry.
            </p>
          </motion.div>

          {/* Pillar 2 */}
          <motion.div 
            whileHover={{ y: -4 }}
            className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4 hover:border-emerald-500/40 transition-all bg-gradient-to-br from-surface-container-lowest/80 to-surface-container-high/30"
          >
            <div className="w-12 h-12 rounded-2xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 shadow-glow">
              <Layers className="w-6 h-6" />
            </div>
            <div className="space-y-1">
              <h3 className="text-lg font-bold text-on-surface">2. Sub-Table Categorization with 1-Click Checkboxes</h3>
              <p className="text-xs text-outline font-mono">Granular segment filtering & custom export selection</p>
            </div>
            <p className="text-xs sm:text-sm text-on-surface-variant leading-relaxed">
              When a document contains mixed information (e.g. Clinical vs Experimental, Regional Revenue vs Operating Costs), DataMorph segregates them into distinct sub-tables. You can check/uncheck specific categories to customize what appears in your final exported report.
            </p>
          </motion.div>

          {/* Pillar 3 */}
          <motion.div 
            whileHover={{ y: -4 }}
            className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4 hover:border-tertiary/40 transition-all bg-gradient-to-br from-surface-container-lowest/80 to-surface-container-high/30"
          >
            <div className="w-12 h-12 rounded-2xl bg-tertiary/10 border border-tertiary/20 flex items-center justify-center text-tertiary shadow-glow">
              <BarChart3 className="w-6 h-6" />
            </div>
            <div className="space-y-1">
              <h3 className="text-lg font-bold text-on-surface">3. Autonomous Visual Studio & Chart Generation</h3>
              <p className="text-xs text-outline font-mono">Bar, Line, Donut, Radar, Area & Treemap archetypes</p>
            </div>
            <p className="text-xs sm:text-sm text-on-surface-variant leading-relaxed">
              The engine analyzes variance, distributions, and cardinality across your structured columns to automatically recommend and render high-impact interactive visual charts. Simply click <b>"+ Add to Report"</b> on any chart to embed it directly in your export.
            </p>
          </motion.div>

          {/* Pillar 4 */}
          <motion.div 
            whileHover={{ y: -4 }}
            className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4 hover:border-amber-500/40 transition-all bg-gradient-to-br from-surface-container-lowest/80 to-surface-container-high/30"
          >
            <div className="w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 shadow-glow">
              <FileOutput className="w-6 h-6" />
            </div>
            <div className="space-y-1">
              <h3 className="text-lg font-bold text-on-surface">4. Executive Multi-Format Report Synthesis</h3>
              <p className="text-xs text-outline font-mono">High-resolution PDF, 16:9 PowerPoint, Word, Excel & ZIP</p>
            </div>
            <p className="text-xs sm:text-sm text-on-surface-variant leading-relaxed">
              Export comprehensive, presentation-ready documents with real vector graphics, structured data grids, and executive AI insights. Export individual sub-tables, generate multi-sheet Excel workbooks, or download complete ZIP archives in 1 click.
            </p>
          </motion.div>

        </div>
      </div>

      {/* 🧭 4. END-TO-END 3-STEP USER FLOW */}
      <div className="glass-panel p-6 sm:p-10 rounded-3xl border border-white/10 space-y-8 bg-surface-container-lowest/70">
        <div className="text-center space-y-1">
          <span className="text-xs font-mono uppercase tracking-widest text-outline">Simple 3-Step Process</span>
          <h3 className="text-2xl font-extrabold text-on-surface">How to Use DataMorph AI</h3>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="space-y-3 text-center sm:text-left">
            <div className="w-10 h-10 rounded-xl bg-primary/20 text-primary font-mono font-bold flex items-center justify-center mx-auto sm:mx-0 border border-primary/30">
              01
            </div>
            <h4 className="font-bold text-base text-on-surface">Upload Your File</h4>
            <p className="text-xs text-outline leading-relaxed">
              Drop any messy document, spreadsheet, or notes. The pipeline instantly parses, scans, and cleans your data.
            </p>
          </div>

          <div className="space-y-3 text-center sm:text-left">
            <div className="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 font-mono font-bold flex items-center justify-center mx-auto sm:mx-0 border border-emerald-500/30">
              02
            </div>
            <h4 className="font-bold text-base text-on-surface">Select Tables & Charts</h4>
            <p className="text-xs text-outline leading-relaxed">
              Check off the specific sub-table categories and visual charts you want in your final exported document.
            </p>
          </div>

          <div className="space-y-3 text-center sm:text-left">
            <div className="w-10 h-10 rounded-xl bg-tertiary/20 text-tertiary font-mono font-bold flex items-center justify-center mx-auto sm:mx-0 border border-tertiary/30">
              03
            </div>
            <h4 className="font-bold text-base text-on-surface">Export in 1 Click</h4>
            <p className="text-xs text-outline leading-relaxed">
              Download your verified PDF report, PowerPoint presentation, Word document, clean Excel spreadsheet, or ZIP.
            </p>
          </div>
        </div>
      </div>

      {/* 🚀 5. FINAL LAUNCH CTA BANNER */}
      <motion.div 
        initial={{ opacity: 0, scale: 0.98 }}
        whileInView={{ opacity: 1, scale: 1 }}
        viewport={{ once: true }}
        className="glass-panel p-8 sm:p-12 rounded-3xl border border-primary/40 text-center space-y-6 bg-gradient-to-tr from-primary/15 via-surface-container-high/70 to-tertiary/15 shadow-glow"
      >
        <h3 className="text-3xl sm:text-4xl font-black text-on-surface tracking-tight">
          Ready to Experience DataMorph AI?
        </h3>
        <p className="text-sm sm:text-base text-outline max-w-xl mx-auto leading-relaxed">
          Start structuring your documents, generating live visual charts, and exporting verified intelligence reports right now.
        </p>
        <button
          onClick={onGetStarted}
          className="inline-flex items-center gap-3 px-9 py-4 rounded-2xl bg-gradient-to-r from-primary-container via-primary to-secondary text-white font-extrabold text-base shadow-glow hover:opacity-95 transition-all active:scale-95"
        >
          <span>Launch DataMorph Workspace</span>
          <ArrowRight className="w-5 h-5" />
        </button>
      </motion.div>

    </div>
  );
};
export default IntroductionView;
