import React, { useState } from 'react';
import { 
  BarChart3, 
  LineChart as LineChartIcon, 
  PieChart as PieChartIcon, 
  ScatterChart as ScatterIcon, 
  AreaChart as AreaIcon,
  Sparkles, 
  Check, 
  Plus, 
  SlidersHorizontal, 
  ArrowRight, 
  Layers,
  ChevronRight,
  TrendingUp,
  LayoutGrid,
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
  CartesianGrid,
  RadarChart,
  Radar,
  PolarGrid,
  PolarAngleAxis,
  PolarRadiusAxis,
  ComposedChart,
  Legend,
  Treemap
} from 'recharts';
import { motion } from 'framer-motion';
import { VisualizationCardData } from '../types';

interface VisualizationStudioViewProps {
  recommendedCharts: VisualizationCardData[];
  availableColumns: string[];
  selectedCharts: VisualizationCardData[];
  onToggleSelectChart: (chart: VisualizationCardData) => void;
  onGenerateCustomChart: (config: { chart_type: string; x_axis: string; y_axis?: string; aggregation?: string }) => Promise<void>;
  onProceedToChat: () => void;
  onProceedToReport: () => void;
}

export const VisualizationStudioView: React.FC<VisualizationStudioViewProps> = ({
  recommendedCharts,
  availableColumns,
  selectedCharts,
  onToggleSelectChart,
  onGenerateCustomChart,
  onProceedToChat,
  onProceedToReport,
}) => {
  const [showCustomBuilder, setShowCustomBuilder] = useState(false);
  const [customType, setCustomType] = useState('bar');
  const [customX, setCustomX] = useState(availableColumns[0] || '');
  const [customY, setCustomY] = useState(availableColumns[1] || '');
  const [customAgg, setCustomAgg] = useState('sum');
  const [isGenerating, setIsGenerating] = useState(false);
  const [activeFilter, setActiveFilter] = useState<string>('all');

  const handleCustomSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!customX) return;
    setIsGenerating(true);
    try {
      await onGenerateCustomChart({
        chart_type: customType,
        x_axis: customX,
        y_axis: customY || undefined,
        aggregation: customAgg,
      });
      setShowCustomBuilder(false);
    } finally {
      setIsGenerating(false);
    }
  };

  const chartColors = ['#2e5bff', '#943fe2', '#b8c3ff', '#4ade80', '#fbbf24', '#f87171', '#38bdf8', '#f43f5e', '#a855f7'];

  const filteredCharts = activeFilter === 'all' 
    ? recommendedCharts 
    : recommendedCharts.filter((c) => c.chart_type === activeFilter);

  const renderChart = (card: VisualizationCardData) => {
    const data = card.chart_data || [];
    if (!data.length) return <div className="h-48 flex items-center justify-center text-xs text-outline">No preview data</div>;

    const xKey = card.chart_config.x_axis || 'name';
    const yKey = card.chart_config.y_axis || 'value';
    const secondaryKey = card.chart_config.group_by || 'secondary_value';

    switch (card.chart_type) {
      case 'line':
        return (
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey={xKey} stroke="#8e90a2" fontSize={10} tickLine={false} />
              <YAxis stroke="#8e90a2" fontSize={10} tickLine={false} />
              <Tooltip 
                contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '12px' }} 
              />
              <Line type="monotone" dataKey={yKey} stroke="#2e5bff" strokeWidth={3} dot={{ fill: '#b8c3ff', r: 4 }} activeDot={{ r: 6 }} />
            </LineChart>
          </ResponsiveContainer>
        );

      case 'bar':
        return (
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey={xKey} stroke="#8e90a2" fontSize={10} tickLine={false} />
              <YAxis stroke="#8e90a2" fontSize={10} tickLine={false} />
              <Tooltip 
                contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '12px' }} 
              />
              <Bar dataKey={yKey} fill="#4ade80" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'horizontal_bar':
        return (
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={data} layout="vertical" margin={{ top: 10, right: 20, left: 30, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis type="number" stroke="#8e90a2" fontSize={10} tickLine={false} />
              <YAxis type="category" dataKey={xKey} stroke="#8e90a2" fontSize={10} tickLine={false} />
              <Tooltip 
                contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '12px' }} 
              />
              <Bar dataKey={yKey} fill="#38bdf8" radius={[0, 6, 6, 0]} />
            </BarChart>
          </ResponsiveContainer>
        );

      case 'donut':
        return (
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Tooltip 
                contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '12px' }} 
              />
              <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={50} outerRadius={80} paddingAngle={4}>
                {data.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={chartColors[index % chartColors.length]} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        );

      case 'pie':
        return (
          <ResponsiveContainer width="100%" height={220}>
            <PieChart>
              <Tooltip 
                contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '12px' }} 
              />
              <Pie data={data} dataKey="value" nameKey="name" cx="50%" cy="50%" innerRadius={0} outerRadius={75}>
                {data.map((_, index) => (
                  <Cell key={`cell-${index}`} fill={chartColors[index % chartColors.length]} />
                ))}
              </Pie>
            </PieChart>
          </ResponsiveContainer>
        );

      case 'area':
        return (
          <ResponsiveContainer width="100%" height={220}>
            <AreaChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey={xKey} stroke="#8e90a2" fontSize={10} tickLine={false} />
              <YAxis stroke="#8e90a2" fontSize={10} tickLine={false} />
              <Tooltip 
                contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '12px' }} 
              />
              <Area type="monotone" dataKey={yKey} stroke="#943fe2" fill="#943fe2" fillOpacity={0.3} />
            </AreaChart>
          </ResponsiveContainer>
        );

      case 'composed':
        return (
          <ResponsiveContainer width="100%" height={220}>
            <ComposedChart data={data} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis dataKey={xKey} stroke="#8e90a2" fontSize={10} tickLine={false} />
              <YAxis yAxisId="left" stroke="#8e90a2" fontSize={10} tickLine={false} />
              <YAxis yAxisId="right" orientation="right" stroke="#8e90a2" fontSize={10} tickLine={false} />
              <Tooltip 
                contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '12px' }} 
              />
              <Bar yAxisId="left" dataKey={yKey} fill="#2e5bff" radius={[4, 4, 0, 0]} />
              <Line yAxisId="right" type="monotone" dataKey={secondaryKey} stroke="#fbbf24" strokeWidth={2.5} dot={{ r: 4 }} />
            </ComposedChart>
          </ResponsiveContainer>
        );

      case 'radar':
        return (
          <ResponsiveContainer width="100%" height={220}>
            <RadarChart data={data}>
              <PolarGrid stroke="rgba(255,255,255,0.1)" />
              <PolarAngleAxis dataKey="name" stroke="#8e90a2" fontSize={10} />
              <PolarRadiusAxis stroke="rgba(255,255,255,0.05)" />
              <Radar name="Metrics" dataKey="value" stroke="#38bdf8" fill="#38bdf8" fillOpacity={0.4} />
              <Tooltip 
                contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '12px' }} 
              />
            </RadarChart>
          </ResponsiveContainer>
        );

      case 'scatter':
        return (
          <ResponsiveContainer width="100%" height={220}>
            <ScatterChart margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" />
              <XAxis type="number" dataKey="x" stroke="#8e90a2" fontSize={10} />
              <YAxis type="number" dataKey="y" stroke="#8e90a2" fontSize={10} />
              <Tooltip 
                contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '12px' }} 
              />
              <Scatter data={data} fill="#f43f5e" />
            </ScatterChart>
          </ResponsiveContainer>
        );

      case 'treemap':
        return (
          <ResponsiveContainer width="100%" height={220}>
            <Treemap
              data={data}
              dataKey="value"
              aspectRatio={4 / 3}
              stroke="#111317"
              fill="#2e5bff"
            >
              <Tooltip 
                contentStyle={{ background: '#1e2026', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', fontSize: '12px' }} 
              />
            </Treemap>
          </ResponsiveContainer>
        );

      default:
        return (
          <ResponsiveContainer width="100%" height={220}>
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

  const chartFilterOptions = [
    { id: 'all', label: 'All Charts' },
    { id: 'line', label: 'Line Trends' },
    { id: 'bar', label: 'Bar Comparison' },
    { id: 'horizontal_bar', label: 'Horizontal Rankings' },
    { id: 'donut', label: 'Donut Share' },
    { id: 'composed', label: 'Dual-Axis Combo' },
    { id: 'area', label: 'Volume Area' },
    { id: 'radar', label: 'Radar Spider' },
    { id: 'treemap', label: 'Treemap' },
    { id: 'scatter', label: 'Scatter Correlation' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 py-10 relative z-10 space-y-8">
      {/* Header & Controls */}
      <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <span className="px-2.5 py-0.5 rounded-md text-[11px] font-mono font-semibold uppercase bg-primary-container/20 text-primary border border-primary/30">
              Enhanced Visualization Studio
            </span>
          </div>
          <h1 className="text-3xl font-extrabold text-on-surface tracking-tight">
            Visual Intelligence & Multi-Dimensional Charts
          </h1>
        </div>

        {/* Action Buttons & Collection Counter */}
        <div className="flex items-center gap-3">
          <button
            onClick={() => setShowCustomBuilder(!showCustomBuilder)}
            className="flex items-center gap-2 px-4 py-2.5 rounded-xl text-xs font-semibold bg-surface-container-high hover:bg-surface-variant text-on-surface border border-white/10 transition-all active:scale-95"
          >
            <SlidersHorizontal className="w-4 h-4 text-primary" />
            <span>Custom Chart Builder</span>
          </button>

          <button
            onClick={onProceedToReport}
            className="flex items-center gap-2 px-5 py-2.5 rounded-xl text-xs sm:text-sm font-bold bg-gradient-to-r from-primary-container to-tertiary-container hover:from-primary hover:to-secondary text-white shadow-glow transition-all active:scale-95"
          >
            <span>Report Collection ({selectedCharts.length})</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </div>

      {/* Filter Tabs Strip */}
      <div className="flex items-center gap-1.5 overflow-x-auto pb-1 scrollbar-none">
        <Filter className="w-4 h-4 text-outline flex-shrink-0 mr-1" />
        {chartFilterOptions.map((f) => (
          <button
            key={f.id}
            onClick={() => setActiveFilter(f.id)}
            className={`px-3 py-1.5 rounded-xl text-xs font-medium whitespace-nowrap transition-all ${
              activeFilter === f.id
                ? 'bg-primary text-on-primary font-semibold shadow-sm'
                : 'bg-surface-container-high hover:bg-surface-variant text-outline hover:text-on-surface border border-white/5'
            }`}
          >
            {f.label}
          </button>
        ))}
      </div>

      {/* Custom Chart Builder Panel (Collapsible) */}
      {showCustomBuilder && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          className="glass-panel p-6 rounded-3xl border border-primary/30 shadow-glow"
        >
          <h3 className="font-bold text-base text-on-surface mb-4">Build Custom Visualization</h3>
          <form onSubmit={handleCustomSubmit} className="grid grid-cols-1 sm:grid-cols-4 gap-4">
            <div>
              <label className="block text-xs font-mono text-outline mb-1.5">Chart Type</label>
              <select
                value={customType}
                onChange={(e) => setCustomType(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-surface-container-high border border-white/10 text-xs font-medium text-on-surface focus:outline-none focus:border-primary"
              >
                <option value="bar">Vertical Bar Chart</option>
                <option value="horizontal_bar">Horizontal Bar Chart</option>
                <option value="line">Line Trend Chart</option>
                <option value="donut">Donut Share Chart</option>
                <option value="pie">Pie Chart</option>
                <option value="area">Area Chart</option>
                <option value="composed">Dual-Axis Composed</option>
                <option value="radar">Radar Spider Chart</option>
                <option value="treemap">Treemap Density</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-mono text-outline mb-1.5">X-Axis Dimension</label>
              <select
                value={customX}
                onChange={(e) => setCustomX(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-surface-container-high border border-white/10 text-xs font-medium text-on-surface focus:outline-none focus:border-primary"
              >
                {availableColumns.map((col) => (
                  <option key={col} value={col}>{col}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-xs font-mono text-outline mb-1.5">Y-Axis Metric</label>
              <select
                value={customY}
                onChange={(e) => setCustomY(e.target.value)}
                className="w-full px-3 py-2 rounded-xl bg-surface-container-high border border-white/10 text-xs font-medium text-on-surface focus:outline-none focus:border-primary"
              >
                <option value="">Count / Frequency</option>
                {availableColumns.map((col) => (
                  <option key={col} value={col}>{col}</option>
                ))}
              </select>
            </div>

            <div className="flex items-end">
              <button
                type="submit"
                disabled={isGenerating}
                className="w-full py-2 rounded-xl text-xs font-bold bg-primary text-on-primary hover:bg-white transition-all shadow-sm flex items-center justify-center gap-1.5"
              >
                <Plus className="w-4 h-4" />
                <span>{isGenerating ? 'Generating...' : 'Add Chart'}</span>
              </button>
            </div>
          </form>
        </motion.div>
      )}

      {/* Recommended Chart Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredCharts.map((card) => {
          const isSelected = selectedCharts.some((c) => c.id === card.id);

          return (
            <motion.div
              key={card.id}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              className={`glass-panel p-5 rounded-3xl border transition-all flex flex-col justify-between ${
                isSelected
                  ? 'border-primary/50 shadow-glow bg-surface-container/90'
                  : 'border-white/10 hover:border-white/20'
              }`}
            >
              <div>
                {/* Card Header with Confidence Badge & Selection Toggle */}
                <div className="flex items-center justify-between gap-2 mb-3">
                  <div className="flex items-center gap-2">
                    <span className="px-2.5 py-0.5 rounded-full text-[11px] font-mono font-bold bg-primary-container/20 text-primary border border-primary/30">
                      {card.confidence_score}% match
                    </span>
                    <span className="text-[11px] font-mono uppercase text-outline">
                      {card.chart_type.replace('_', ' ')}
                    </span>
                  </div>

                  <button
                    onClick={() => onToggleSelectChart(card)}
                    className={`flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold transition-all ${
                      isSelected
                        ? 'bg-primary text-on-primary shadow-sm'
                        : 'bg-surface-container-high hover:bg-surface-variant text-outline hover:text-on-surface border border-white/5'
                    }`}
                  >
                    {isSelected ? <Check className="w-3 h-3" /> : <Plus className="w-3 h-3" />}
                    <span>{isSelected ? 'Selected' : 'Add to Report'}</span>
                  </button>
                </div>

                <h3 className="font-bold text-base text-on-surface mb-1">{card.title}</h3>
                <p className="text-xs text-on-surface-variant leading-relaxed mb-4">{card.reason}</p>

                {/* Chart Preview */}
                <div className="py-2">{renderChart(card)}</div>
              </div>

              {/* Card Footer */}
              <div className="pt-3 border-t border-white/5 flex items-center justify-between text-[11px] font-mono text-outline">
                <span>X: {card.chart_config.x_axis || 'Auto'}</span>
                <span>Y: {card.chart_config.y_axis || 'Aggregate'}</span>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Ask Your Data Navigation Card */}
      <div className="glass-card p-6 rounded-3xl border border-white/10 flex flex-col sm:flex-row items-center justify-between gap-4">
        <div className="flex items-center gap-3.5">
          <div className="p-3 rounded-2xl bg-tertiary-container/20 border border-tertiary/30 text-tertiary">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <h4 className="font-bold text-base text-on-surface">Have specific questions about this data?</h4>
            <p className="text-xs text-on-surface-variant">Ask questions in natural language like "Which product generated highest revenue?" or "Show monthly sales trends".</p>
          </div>
        </div>
        <button
          onClick={onProceedToChat}
          className="whitespace-nowrap px-5 py-2.5 rounded-xl text-xs sm:text-sm font-semibold bg-gradient-to-r from-tertiary-container to-primary-container text-white shadow-glow hover:opacity-90 transition-all active:scale-95 flex items-center gap-1.5"
        >
          <span>Ask Your Data AI</span>
          <ChevronRight className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};
