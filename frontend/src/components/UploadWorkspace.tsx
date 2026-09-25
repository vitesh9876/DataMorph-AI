import React, { useState, useRef } from 'react';
import { 
  UploadCloud, 
  TableProperties, 
  BarChart3, 
  CheckCircle2, 
  Loader2, 
  AlertCircle, 
  ArrowRight,
  Zap,
  FileText,
  FileSpreadsheet,
  FileCode2,
  Trash2,
  Sparkles,
  AlignLeft,
  Layers,
  GitMerge,
  File as FileIcon,
  X,
  Plus
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import type { FileProcessingStatus } from '../types';

interface UploadWorkspaceProps {
  onFileUpload: (file: File) => void;
  processingStatus: FileProcessingStatus | null;
  onProceedToAnalysis: () => void;
  onBackToIntro?: () => void;
  activeFileName?: string | null;
}

export const UploadWorkspace: React.FC<UploadWorkspaceProps> = ({
  onFileUpload,
  processingStatus,
  onProceedToAnalysis,
  onBackToIntro,
  activeFileName,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [attachedFiles, setAttachedFiles] = useState<File[]>([]);
  const [rawText, setRawText] = useState('');
  const [customDocName, setCustomDocName] = useState('raw_unstructured_notes.txt');

  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => {
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const newFiles = Array.from(e.dataTransfer.files);
      setAttachedFiles(prev => [...prev, ...newFiles]);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      const newFiles = Array.from(e.target.files);
      setAttachedFiles(prev => [...prev, ...newFiles]);
    }
  };

  const handleRemoveFile = (index: number) => {
    setAttachedFiles(prev => prev.filter((_, idx) => idx !== index));
  };

  // Master Unified Submission (Combines attached files + accompanying text notes)
  const handleProcessCombinedData = async () => {
    const hasFiles = attachedFiles.length > 0;
    const hasText = rawText.trim().length > 0;

    if (!hasFiles && !hasText) return;

    // Case 1: Only 1 file and NO text notes
    if (hasFiles && attachedFiles.length === 1 && !hasText) {
      onFileUpload(attachedFiles[0]);
      return;
    }

    // Case 2: Only raw text and NO files
    if (!hasFiles && hasText) {
      const finalName = customDocName.trim().endsWith('.txt') ? customDocName.trim() : `${customDocName.trim() || 'raw_notes'}.txt`;
      const blob = new Blob([rawText], { type: 'text/plain' });
      const textFile = new window.File([blob], finalName, { type: 'text/plain' });
      onFileUpload(textFile);
      return;
    }

    // Case 3: Combined files + accompanying direct text notes
    let combinedContent = '';

    // Read attached files
    for (const file of attachedFiles) {
      try {
        const text = await file.text();
        const baseName = file.name.replace(/\.[^/.]+$/, '');
        combinedContent += `\n--- Category: ${baseName} | Source_File: ${file.name} ---\n` + text + '\n';
      } catch (err) {
        combinedContent += `\n--- Category: ${file.name} ---\nFile: ${file.name} (Content Attached)\n`;
      }
    }

    // Append accompanying raw text notes if provided
    if (hasText) {
      combinedContent += `\n--- Category: Direct Notes & Context | Source: pasted_notes ---\n` + rawText.trim() + '\n';
    }

    const firstFileName = attachedFiles[0]?.name.replace(/\.[^/.]+$/, '') || 'Data';
    const mergedName = `Combined_${firstFileName}_and_Notes.txt`;
    const blob = new Blob([combinedContent], { type: 'text/plain' });
    const combinedFile = new window.File([blob], mergedName, { type: 'text/plain' });

    onFileUpload(combinedFile);
  };

  const isProcessing = processingStatus?.status === 'processing';
  const isReady = processingStatus?.status === 'ready';
  const isError = processingStatus?.status === 'error';

  const hasInputs = attachedFiles.length > 0 || rawText.trim().length > 0;

  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 py-8 sm:py-14 relative z-10 space-y-6">
      {/* Top Back Navigation */}
      {onBackToIntro && (
        <div className="flex items-center justify-between">
          <button
            onClick={onBackToIntro}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-surface-container-high hover:bg-surface-variant border border-white/10 text-xs font-semibold text-outline hover:text-on-surface transition-all active:scale-95"
          >
            <span>← Back to Introduction</span>
          </button>
        </div>
      )}

      {/* Header */}
      <div className="text-center space-y-2">
        <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-on-surface">
          Upload Files & Add Notes
        </h1>
        <p className="text-sm text-outline max-w-lg mx-auto">
          Attach file(s), add accompanying text notes, or send both combined into a single structured dataset.
        </p>
      </div>

      {/* Main Upload Zone or Processing Timeline */}
      <div className="space-y-6">
        {!processingStatus ? (
          <div className="glass-panel p-6 sm:p-8 rounded-3xl border border-white/15 space-y-5 bg-surface-container-lowest/80 shadow-2xl">
            
            {/* 1. File Drag & Drop Zone */}
            <div
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-2xl p-6 sm:p-8 text-center cursor-pointer transition-all duration-300 relative group overflow-hidden ${
                isDragging
                  ? 'border-primary bg-primary/10 shadow-glow-lg scale-[1.01]'
                  : 'border-white/15 hover:border-primary/50 hover:bg-surface-container-high/40'
              }`}
            >
              <input
                ref={fileInputRef}
                type="file"
                multiple
                onChange={handleFileChange}
                accept=".pdf,.csv,.xlsx,.xls,.pptx,.ppt,.docx,.doc,.txt,.json,.xml,.log"
                className="hidden"
              />

              <div className="w-12 h-12 mx-auto mb-2.5 rounded-2xl bg-gradient-to-tr from-primary-container via-indigo-600 to-tertiary-container flex items-center justify-center text-white shadow-glow group-hover:scale-110 transition-transform">
                <UploadCloud className="w-6 h-6 animate-bounce" style={{ animationDuration: '2.5s' }} />
              </div>

              <h3 className="text-sm sm:text-base font-bold text-on-surface">
                Drag & Drop File(s) Here, or <span className="text-primary underline">Browse</span>
              </h3>
              <p className="mt-1 text-[11px] text-outline">
                Supports PDF, Excel (.xlsx, .csv), Word (.docx), PowerPoint (.pptx), TXT & Invoices
              </p>
            </div>

            {/* Attached Files Pill Strip */}
            {attachedFiles.length > 0 && (
              <div className="space-y-2 p-3 rounded-2xl bg-surface-container-lowest border border-white/5 animate-fadeIn">
                <div className="flex items-center justify-between text-xs font-mono text-outline">
                  <span className="text-emerald-400 font-bold flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    {attachedFiles.length} Attached File(s):
                  </span>
                  <button
                    onClick={() => setAttachedFiles([])}
                    className="text-[10px] text-outline hover:text-red-400 underline"
                  >
                    Clear all files
                  </button>
                </div>

                <div className="flex flex-wrap gap-2">
                  {attachedFiles.map((file, idx) => (
                    <div
                      key={idx}
                      className="flex items-center gap-2 px-3 py-1.5 rounded-xl bg-surface-container-high border border-white/10 text-xs font-mono text-on-surface shadow-sm"
                    >
                      <FileIcon className="w-3.5 h-3.5 text-primary shrink-0" />
                      <span className="truncate max-w-xs">{file.name}</span>
                      <span className="text-[10px] text-outline">({(file.size / 1024).toFixed(1)} KB)</span>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          handleRemoveFile(idx);
                        }}
                        className="p-0.5 rounded-full hover:bg-red-500/20 text-outline hover:text-red-400 transition-colors"
                      >
                        <X className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Subtle Divider */}
            <div className="relative flex items-center justify-center pt-1">
              <div className="border-t border-white/10 w-full" />
              <span className="bg-surface-container-lowest px-3 text-[10px] font-mono text-outline font-bold uppercase tracking-wider whitespace-nowrap">
                Accompanying Notes / Direct Raw Text (Optional)
              </span>
              <div className="border-t border-white/10 w-full" />
            </div>

            {/* 2. Direct Raw Text Area */}
            <div className="space-y-2.5">
              <div className="flex items-center justify-between gap-2">
                <span className="text-xs font-mono text-emerald-400 font-bold flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5" />
                  Text Notes / Context
                </span>
                
                <div className="flex items-center gap-2">
                  <input
                    type="text"
                    value={customDocName}
                    onChange={(e) => setCustomDocName(e.target.value)}
                    placeholder="Filename..."
                    className="px-2.5 py-1 rounded-xl bg-surface-container-high border border-white/10 text-xs text-on-surface font-mono focus:outline-none focus:border-emerald-500 w-36 sm:w-44"
                  />
                  {rawText && (
                    <button
                      onClick={() => setRawText('')}
                      className="p-1 rounded-xl bg-surface-container-high hover:bg-red-500/20 text-outline hover:text-red-400"
                      title="Clear Text"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>
              </div>

              <div className="relative">
                <textarea
                  rows={4}
                  value={rawText}
                  onChange={(e) => setRawText(e.target.value)}
                  placeholder={`Paste additional context, unorganized notes, or values here... e.g.:\nPatient BP 122/78 mmHg, glucose 98 mg/dL, Total Cholesterol 215 mg/dL.\nCategory: Diagnostic & Clinical.`}
                  className="w-full p-3.5 rounded-xl bg-black/50 border border-white/10 text-xs font-mono text-slate-200 placeholder:text-slate-600 focus:outline-none focus:border-emerald-500 leading-relaxed shadow-inner"
                />
                <div className="absolute right-3 bottom-3 text-[10px] font-mono text-outline bg-black/60 px-2 py-0.5 rounded-md border border-white/5 pointer-events-none">
                  {rawText.length} chars
                </div>
              </div>
            </div>

            {/* Master Submission Action Button */}
            <div className="pt-2 flex items-center justify-end">
              <button
                disabled={!hasInputs}
                onClick={handleProcessCombinedData}
                className={`w-full sm:w-auto px-7 py-3 rounded-2xl font-bold text-xs shadow-glow transition-all flex items-center justify-center gap-2 active:scale-95 ${
                  hasInputs
                    ? 'bg-gradient-to-r from-primary-container via-primary to-secondary hover:opacity-95 text-white'
                    : 'bg-surface-container-high text-outline cursor-not-allowed opacity-50'
                }`}
              >
                <Sparkles className="w-4 h-4" />
                <span>
                  {attachedFiles.length > 0 && rawText.trim()
                    ? `Process Combined (${attachedFiles.length} File${attachedFiles.length > 1 ? 's' : ''} + Notes)`
                    : attachedFiles.length > 0
                    ? `Process ${attachedFiles.length} Attached File${attachedFiles.length > 1 ? 's' : ''}`
                    : 'Structure & Morph Text Notes'}
                </span>
                <ArrowRight className="w-4 h-4" />
              </button>
            </div>

          </div>
        ) : (
          /* Processing Progress Timeline */
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="glass-panel p-6 sm:p-8 rounded-3xl border border-white/10 space-y-6"
          >
            <div className="flex items-center justify-between">
              <div>
                <span className="text-xs font-mono text-outline uppercase tracking-wider">Pipeline Execution</span>
                <h3 className="text-xl font-bold text-on-surface flex items-center gap-2 mt-0.5">
                  {isProcessing && <Loader2 className="w-5 h-5 animate-spin text-primary" />}
                  {isReady && <CheckCircle2 className="w-5 h-5 text-emerald-400" />}
                  {isError && <AlertCircle className="w-5 h-5 text-red-400" />}
                  <span>{activeFileName || 'Processing Dataset...'}</span>
                </h3>
              </div>

              <span className="text-sm font-mono font-bold text-primary bg-primary/10 px-3 py-1 rounded-xl border border-primary/20">
                {processingStatus.progress}%
              </span>
            </div>

            {/* Progress Bar */}
            <div className="w-full h-2 rounded-full bg-surface-container-high overflow-hidden">
              <motion.div
                initial={{ width: '0%' }}
                animate={{ width: `${processingStatus.progress}%` }}
                transition={{ duration: 0.5 }}
                className="h-full bg-gradient-to-r from-primary via-tertiary to-emerald-400"
              />
            </div>

            {/* Step Timeline */}
            <div className="space-y-3 pt-2">
              {processingStatus.timeline.map((step, idx) => (
                <div
                  key={step.step_id || idx}
                  className={`flex items-center justify-between p-3 rounded-xl text-xs font-mono transition-all ${
                    step.status === 'completed'
                      ? 'bg-emerald-950/20 text-emerald-300 border border-emerald-500/20'
                      : step.status === 'active'
                      ? 'bg-primary/10 text-primary border border-primary/30 animate-pulse'
                      : 'bg-surface-container-lowest text-outline border border-white/5'
                  }`}
                >
                  <div className="flex items-center gap-3">
                    {step.status === 'completed' && <CheckCircle2 className="w-4 h-4 text-emerald-400" />}
                    {step.status === 'active' && <Loader2 className="w-4 h-4 animate-spin text-primary" />}
                    {step.status === 'waiting' && <span className="w-4 h-4 rounded-full border border-outline/40 flex items-center justify-center text-[10px]">{idx + 1}</span>}
                    <span>{step.label}</span>
                  </div>
                  <span className="capitalize font-bold text-[10px]">{step.status}</span>
                </div>
              ))}
            </div>

            {isReady && (
              <motion.button
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                onClick={onProceedToAnalysis}
                className="w-full py-3.5 rounded-2xl bg-gradient-to-r from-primary-container via-primary to-secondary text-white font-bold text-sm shadow-glow flex items-center justify-center gap-2 hover:opacity-95 transition-all"
              >
                <span>Launch Data & Visual Workspace</span>
                <ArrowRight className="w-4 h-4" />
              </motion.button>
            )}
          </motion.div>
        )}
      </div>

    </div>
  );
};
export default UploadWorkspace;
