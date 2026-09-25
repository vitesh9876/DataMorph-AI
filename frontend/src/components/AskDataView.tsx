import React, { useState } from 'react';
import { 
  MessageSquareCode, 
  Send, 
  Sparkles, 
  User, 
  Bot, 
  Plus, 
  Check, 
  Table, 
  BarChart2, 
  ChevronRight, 
  Loader2,
  HelpCircle
} from 'lucide-react';
import { motion } from 'framer-motion';
import { AskDataMessage, VisualizationCardData } from '../types';

interface AskDataViewProps {
  messages: AskDataMessage[];
  onSendMessage: (question: string) => Promise<void>;
  onAddChartToReport: (chart: VisualizationCardData) => void;
  selectedChartIds: string[];
}

export const AskDataView: React.FC<AskDataViewProps> = ({
  messages,
  onSendMessage,
  onAddChartToReport,
  selectedChartIds,
}) => {
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sampleQuestions = [
    'Which product generated the highest revenue?',
    'Show monthly sales trends over time.',
    'Are there any unusual transactions or anomalies?',
    'Compare performance across all regional segments.'
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!inputText.trim() || isLoading) return;

    const query = inputText.trim();
    setInputText('');
    setIsLoading(true);
    try {
      await onSendMessage(query);
    } finally {
      setIsLoading(false);
    }
  };

  const handlePresetClick = (q: string) => {
    setInputText(q);
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 py-10 relative z-10 space-y-6">
      {/* Header */}
      <div>
        <div className="flex items-center gap-2 mb-1">
          <span className="px-2.5 py-0.5 rounded-md text-[11px] font-mono font-semibold uppercase bg-tertiary-container/20 text-tertiary border border-tertiary/30">
            Conversational Data Intelligence
          </span>
        </div>
        <h1 className="text-3xl font-extrabold text-on-surface tracking-tight">
          Ask Your Data
        </h1>
        <p className="mt-1 text-on-surface-variant text-sm">
          Ask questions in natural English. DataMorph AI computes verified answers and synthesizes relevant data slices and visual charts.
        </p>
      </div>

      {/* Preset Questions Chips */}
      <div className="flex flex-wrap gap-2 pt-2">
        {sampleQuestions.map((q) => (
          <button
            key={q}
            onClick={() => handlePresetClick(q)}
            className="px-3 py-1.5 rounded-xl text-xs font-medium bg-surface-container-high hover:bg-surface-variant text-on-surface border border-white/5 transition-all flex items-center gap-1.5 active:scale-95"
          >
            <HelpCircle className="w-3.5 h-3.5 text-primary" />
            <span>{q}</span>
          </button>
        ))}
      </div>

      {/* Chat Messages Stream */}
      <div className="glass-panel p-6 rounded-3xl border border-white/10 min-h-[420px] max-h-[600px] overflow-y-auto space-y-6 flex flex-col">
        {messages.length === 0 ? (
          <div className="flex-1 flex flex-col items-center justify-center text-center p-8 text-outline">
            <div className="w-16 h-16 rounded-2xl bg-surface-container-high border border-white/5 flex items-center justify-center text-primary mb-3">
              <MessageSquareCode className="w-8 h-8" />
            </div>
            <h3 className="font-semibold text-base text-on-surface">No queries asked yet</h3>
            <p className="text-xs text-on-surface-variant max-w-sm mt-1">
              Select a suggested question above or type any analytical inquiry about your structured dataset.
            </p>
          </div>
        ) : (
          messages.map((msg) => {
            const isUser = msg.role === 'user';

            return (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex gap-3.5 ${isUser ? 'justify-end' : 'justify-start'}`}
              >
                {!isUser && (
                  <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-primary-container to-tertiary-container flex-shrink-0 flex items-center justify-center text-white shadow-glow">
                    <Bot className="w-5 h-5" />
                  </div>
                )}

                <div
                  className={`p-4 rounded-2xl max-w-2xl text-sm leading-relaxed ${
                    isUser
                      ? 'bg-primary text-on-primary font-medium rounded-tr-sm'
                      : 'glass-card border-white/10 text-on-surface rounded-tl-sm space-y-4'
                  }`}
                >
                  <p className="whitespace-pre-line">{msg.content}</p>

                  {/* Supporting Data Slice Table */}
                  {!isUser && msg.structured_data && msg.structured_data.length > 0 && (
                    <div className="p-3 rounded-xl bg-surface-container-lowest/80 border border-white/5 space-y-2">
                      <div className="flex items-center gap-1.5 text-xs font-mono text-outline">
                        <Table className="w-3.5 h-3.5 text-primary" />
                        <span>Supporting Verified Data Slice</span>
                      </div>
                      <div className="overflow-x-auto max-h-48 text-xs font-mono">
                        <table className="w-full text-left">
                          <thead className="border-b border-white/10 text-outline">
                            <tr>
                              {Object.keys(msg.structured_data[0]).map((k) => (
                                <th key={k} className="py-1 px-2">{k}</th>
                              ))}
                            </tr>
                          </thead>
                          <tbody className="divide-y divide-white/5 text-on-surface-variant">
                            {msg.structured_data.slice(0, 5).map((row, rIdx) => (
                              <tr key={rIdx}>
                                {Object.keys(row).map((k) => (
                                  <td key={k} className="py-1 px-2">{String(row[k])}</td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    </div>
                  )}

                  {/* Suggested Chart Preview & Pin Button */}
                  {!isUser && msg.suggested_chart && (
                    <div className="p-3 rounded-xl bg-surface-container-lowest/80 border border-primary/20 flex flex-col sm:flex-row items-center justify-between gap-3">
                      <div className="flex items-center gap-2">
                        <BarChart2 className="w-4 h-4 text-primary" />
                        <span className="font-semibold text-xs text-on-surface">
                          {msg.suggested_chart.title} ({msg.suggested_chart.chart_type.toUpperCase()})
                        </span>
                      </div>

                      <button
                        onClick={() => msg.suggested_chart && onAddChartToReport(msg.suggested_chart)}
                        className={`flex items-center gap-1.5 px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
                          selectedChartIds.includes(msg.suggested_chart.id)
                            ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                            : 'bg-primary text-on-primary hover:bg-white shadow-sm'
                        }`}
                      >
                        {selectedChartIds.includes(msg.suggested_chart.id) ? (
                          <>
                            <Check className="w-3 h-3" />
                            <span>Added to Report</span>
                          </>
                        ) : (
                          <>
                            <Plus className="w-3 h-3" />
                            <span>Add Chart to Report</span>
                          </>
                        )}
                      </button>
                    </div>
                  )}
                </div>

                {isUser && (
                  <div className="w-9 h-9 rounded-xl bg-surface-container-high border border-white/10 flex-shrink-0 flex items-center justify-center text-on-surface">
                    <User className="w-5 h-5" />
                  </div>
                )}
              </motion.div>
            );
          })
        )}

        {isLoading && (
          <div className="flex items-center gap-3 text-xs text-outline font-mono">
            <div className="w-8 h-8 rounded-xl bg-primary-container/20 flex items-center justify-center text-primary animate-pulse">
              <Loader2 className="w-4 h-4 animate-spin" />
            </div>
            <span>Evaluating pandas expressions & generating response...</span>
          </div>
        )}
      </div>

      {/* Chat Input Bar */}
      <form onSubmit={handleSubmit} className="relative">
        <input
          type="text"
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="Ask anything about your data (e.g. Which category is leading sales?)..."
          className="w-full pl-5 pr-28 py-4 rounded-2xl bg-surface-container-high border border-white/10 text-sm text-on-surface focus:outline-none focus:border-primary/60 shadow-lg placeholder:text-outline"
        />
        <button
          type="submit"
          disabled={!inputText.trim() || isLoading}
          className="absolute right-2.5 top-2.5 bottom-2.5 px-4 rounded-xl font-bold text-xs bg-gradient-to-r from-primary-container to-tertiary-container hover:from-primary hover:to-secondary text-white shadow-glow disabled:opacity-40 disabled:cursor-not-allowed flex items-center gap-1.5 transition-all active:scale-95"
        >
          <span>Ask</span>
          <Send className="w-3.5 h-3.5" />
        </button>
      </form>
    </div>
  );
};
