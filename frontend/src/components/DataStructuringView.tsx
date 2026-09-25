import React, { useState } from 'react';
import { 
  TableProperties, 
  Sparkles, 
  Check, 
  X, 
  ArrowRight, 
  TrendingUp, 
  AlertTriangle, 
  CheckCircle2, 
  Layers, 
  FileSpreadsheet,
  Sliders
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { StructuringOverview } from '../types';

interface DataStructuringViewProps {
  structuring: StructuringOverview;
  onApplyRule: (recommendationId: string, action: 'accept' | 'reject') => Promise<void>;
  onProceedToVisualizations: () => void;
}

export const DataStructuringView: React.FC<DataStructuringViewProps> = ({
  structuring,
  onApplyRule,
  onProceedToVisualizations,
}) => {
  const [loadingRuleId, setLoadingRuleId] = useState<string | null>(null);

  const handleRuleAction = async (id: string, action: 'accept' | 'reject') => {
    setLoadingRuleId(id);
    try {
      await onApplyRule(id, action);
    } finally {
      setLoadingRuleId(null);
    }
  };

  const rawColumns = structuring.raw_sample.length > 0 ? Object.keys(structuring.raw_sample[0]) : [];
  const cleanColumns = structuring.structured_sample.length > 0 ? Object.keys(structuring.structured_sample[0]) : [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-10 relative z-10 space-y-8">
      {/* Header with Live Quality Score Improvement */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-md text-[11px] font-mono font-semibold uppercase bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
              Interactive Structuring Workspace
            </span>
          </div>
          <h1 className="text-3xl font-extrabold text-on-surface tracking-tight">
            Data Morphing & Optimization
          </h1>
        </div>

        {/* Quality Score Animated Transformation Pill */}
        <div className="flex items-center gap-3 bg-surface-container-high px-4 py-2 rounded-2xl border border-white/10 shadow-glow">
          <div className="flex flex-col">
            <span className="text-[10px] uppercase font-mono text-outline">Before Cleaning</span>
            <span className="text-base font-bold font-mono text-amber-400">{structuring.quality_score_before}%</span>
          </div>
          <ArrowRight className="w-4 h-4 text-primary" />
          <div className="flex flex-col">
            <span className="text-[10px] uppercase font-mono text-outline">After Cleaning</span>
            <motion.span 
              key={structuring.quality_score_after}
              initial={{ scale: 1.2, color: '#4ade80' }}
              animate={{ scale: 1 }}
              className="text-base font-bold font-mono text-emerald-400"
            >
              {structuring.quality_score_after}%
            </motion.span>
          </div>
        </div>
      </div>

      {/* Recommendations Cards Section */}
      <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-5 h-5 text-primary" />
            <h3 className="font-bold text-base text-on-surface">
              AI Cleaning Recommendations ({structuring.recommendations.length})
            </h3>
          </div>
          <span className="text-xs text-outline font-mono">Review and apply optimizations</span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {structuring.recommendations.map((rec) => {
            const isPending = rec.status === 'pending';
            const isAccepted = rec.status === 'accepted';
            const isRejected = rec.status === 'rejected';
            const isLoading = loadingRuleId === rec.id;

            return (
              <motion.div
                key={rec.id}
                layout
                className={`p-4 rounded-2xl border transition-all flex flex-col justify-between ${
                  isAccepted
                    ? 'bg-emerald-950/20 border-emerald-500/30'
                    : isRejected
                    ? 'bg-surface-container-lowest/40 border-white/5 opacity-60'
                    : 'glass-card border-white/10 hover:border-primary/40'
                }`}
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span className="text-[10px] font-mono uppercase px-2 py-0.5 rounded bg-surface-container-high text-primary border border-white/5">
                      {rec.rule_type.replace('_', ' ')}
                    </span>
                    <span className="text-xs font-mono font-bold text-emerald-400">
                      +{rec.impact_score_gain}% gain
                    </span>
                  </div>

                  <h4 className="font-semibold text-sm text-on-surface mb-1">{rec.title}</h4>
                  <p className="text-xs text-on-surface-variant leading-relaxed mb-3">{rec.description}</p>
                </div>

                <div className="pt-3 border-t border-white/5 flex items-center justify-between gap-2">
                  <span className="text-[11px] font-mono text-outline">
                    {isAccepted ? 'Applied' : isRejected ? 'Dismissed' : 'Action required'}
                  </span>

                  {isPending && (
                    <div className="flex items-center gap-1.5">
                      <button
                        disabled={isLoading}
                        onClick={() => handleRuleAction(rec.id, 'reject')}
                        className="px-2.5 py-1 rounded-lg text-xs font-medium bg-surface-container-high hover:bg-surface-variant text-outline hover:text-on-surface border border-white/5 transition-all"
                      >
                        Reject
                      </button>
                      <button
                        disabled={isLoading}
                        onClick={() => handleRuleAction(rec.id, 'accept')}
                        className="flex items-center gap-1 px-3 py-1 rounded-lg text-xs font-bold bg-primary text-on-primary hover:bg-white transition-all shadow-sm"
                      >
                        <Check className="w-3 h-3" />
                        <span>Accept</span>
                      </button>
                    </div>
                  )}

                  {isAccepted && (
                    <span className="inline-flex items-center gap-1 text-xs font-semibold text-emerald-400">
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>Accepted</span>
                    </span>
                  )}
                </div>
              </motion.div>
            );
          })}
        </div>
      </div>

      {/* Side-by-Side Comparison Workspace */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Left Side: Raw Extracted Data */}
        <div className="glass-panel p-6 rounded-3xl border border-white/10 space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono uppercase text-red-400 flex items-center gap-1.5 font-bold">
              <span className="w-2 h-2 rounded-full bg-red-400" />
              Raw Extracted Records
            </span>
            <span className="text-xs font-mono text-outline">{structuring.total_rows_raw} rows</span>
          </div>

          <div className="overflow-x-auto max-h-96 border border-white/5 rounded-2xl bg-surface-container-lowest/60">
            <table className="w-full text-left text-xs font-mono">
              <thead className="sticky top-0 bg-surface-container-high text-outline">
                <tr className="border-b border-white/10">
                  {rawColumns.map((col) => (
                    <th key={col} className="py-2.5 px-3 whitespace-nowrap">{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-on-surface-variant">
                {structuring.raw_sample.slice(0, 10).map((row, idx) => (
                  <tr key={idx} className="hover:bg-white/5">
                    {rawColumns.map((col) => (
                      <td key={col} className="py-2 px-3 whitespace-nowrap">
                        {String(row[col] ?? '—')}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Right Side: AI-Structured Data */}
        <div className="glass-panel p-6 rounded-3xl border border-emerald-500/20 shadow-glow space-y-3">
          <div className="flex items-center justify-between">
            <span className="text-xs font-mono uppercase text-emerald-400 flex items-center gap-1.5 font-bold">
              <span className="w-2 h-2 rounded-full bg-emerald-400" />
              AI-Structured & Cleaned Data
            </span>
            <span className="text-xs font-mono text-emerald-400 font-semibold">{structuring.total_rows_clean} rows</span>
          </div>

          <div className="overflow-x-auto max-h-96 border border-emerald-500/20 rounded-2xl bg-emerald-950/10">
            <table className="w-full text-left text-xs font-mono">
              <thead className="sticky top-0 bg-surface-container-high text-emerald-300">
                <tr className="border-b border-white/10">
                  {cleanColumns.map((col) => (
                    <th key={col} className="py-2.5 px-3 whitespace-nowrap">{col}</th>
                  ))}
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5 text-on-surface">
                {structuring.structured_sample.slice(0, 10).map((row, idx) => (
                  <tr key={idx} className="hover:bg-emerald-500/10">
                    {cleanColumns.map((col) => (
                      <td key={col} className="py-2 px-3 whitespace-nowrap font-medium">
                        {String(row[col] ?? '—')}
                      </td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Bottom CTA to proceed to Visualizations */}
      <div className="flex items-center justify-end pt-4">
        <button
          onClick={onProceedToVisualizations}
          className="flex items-center gap-2 px-6 py-3 rounded-xl text-sm font-bold bg-gradient-to-r from-primary-container to-tertiary-container hover:from-primary hover:to-secondary text-white shadow-glow transition-all active:scale-95"
        >
          <span>Explore Visualization Studio</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
