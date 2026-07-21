import React from 'react';
import { Database, RefreshCw } from 'lucide-react';

interface EmptyStateProps {
  title?: string;
  description?: string;
  onRefresh?: () => void;
}

export const EmptyState: React.FC<EmptyStateProps> = ({
  title = "No Intelligence Records Found",
  description = "No matching cases or suspect files match your active filters.",
  onRefresh
}) => {
  return (
    <div className="flex flex-col items-center justify-center p-10 glass-card rounded-2xl border border-blue-500/20 text-center">
      <div className="w-14 h-14 rounded-2xl bg-blue-600/10 border border-blue-500/30 flex items-center justify-center text-blue-400 mb-4">
        <Database className="w-7 h-7" />
      </div>
      <h4 className="text-sm font-bold text-white uppercase tracking-wider">{title}</h4>
      <p className="text-xs text-slate-400 max-w-sm mt-1 mb-4">{description}</p>
      {onRefresh && (
        <button
          onClick={onRefresh}
          className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold flex items-center space-x-2 transition-all shadow-glow-sm"
        >
          <RefreshCw size={14} />
          <span>Reset Search Criteria</span>
        </button>
      )}
    </div>
  );
};
