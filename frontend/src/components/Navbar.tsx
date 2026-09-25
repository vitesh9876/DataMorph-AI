import React from 'react';
import { 
  Sparkles, 
  Plus,
  FileCheck,
  Rocket,
  TableProperties
} from 'lucide-react';

interface NavbarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
  hasActiveFile: boolean;
  activeFileName?: string | null;
  onReset: () => void;
  isBackendConnected: boolean;
}

export const Navbar: React.FC<NavbarProps> = ({
  activeTab,
  setActiveTab,
  hasActiveFile,
  activeFileName,
  onReset,
  isBackendConnected,
}) => {
  return (
    <header className="sticky top-0 z-50 w-full border-b border-surface-variant/40 bg-surface/80 backdrop-blur-xl transition-all">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        {/* Brand Logo */}
        <div 
          onClick={() => setActiveTab('intro')}
          className="flex items-center gap-3 cursor-pointer group"
        >
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-primary-container via-tertiary-container to-primary flex items-center justify-center shadow-glow group-hover:scale-105 transition-transform duration-300">
            <Sparkles className="w-5 h-5 text-white animate-pulse" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="font-bold text-base sm:text-lg tracking-tight text-gradient">DataMorph AI</span>
              <span className="text-[10px] uppercase font-mono px-1.5 py-0.2 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">Studio</span>
            </div>
            <p className="text-[11px] text-outline font-medium hidden sm:block">Raw to Structured Data & Visual Intelligence</p>
          </div>
        </div>

        {/* Center Navigation Tabs: Introduction vs Workspace */}
        <nav className="flex items-center gap-1.5 bg-surface-container-lowest/80 p-1.5 rounded-2xl border border-white/5 shadow-inner">
          <button
            onClick={() => setActiveTab('intro')}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all ${
              activeTab === 'intro'
                ? 'bg-primary text-on-primary shadow-sm'
                : 'text-on-surface-variant hover:text-on-surface hover:bg-white/5'
            }`}
          >
            <Rocket className="w-3.5 h-3.5" />
            <span>Introduction</span>
          </button>

          <button
            onClick={() => setActiveTab('workspace')}
            className={`flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl text-xs font-semibold transition-all ${
              activeTab === 'workspace'
                ? 'bg-primary text-on-primary shadow-sm'
                : 'text-on-surface-variant hover:text-on-surface hover:bg-white/5'
            }`}
          >
            <TableProperties className="w-3.5 h-3.5" />
            <span>DataMorph Workspace</span>
          </button>
        </nav>

        {/* Right Active File & Action Center */}
        <div className="flex items-center gap-3">
          {hasActiveFile && activeFileName && (
            <div className="hidden lg:flex items-center gap-2 px-3 py-1.5 rounded-xl bg-surface-container-high border border-white/5 text-xs text-on-surface font-mono">
              <FileCheck className="w-3.5 h-3.5 text-emerald-400" />
              <span className="max-w-[160px] truncate">{activeFileName}</span>
            </div>
          )}

          {hasActiveFile && (
            <button
              onClick={onReset}
              className="flex items-center gap-1.5 px-3.5 py-2 rounded-xl text-xs font-bold bg-surface-container-high hover:bg-surface-variant border border-white/10 text-on-surface transition-all active:scale-95 shadow-sm"
            >
              <Plus className="w-4 h-4 text-primary" />
              <span>Upload File</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
};
export default Navbar;
