import React from 'react';
import { AlertOctagon, RotateCcw } from 'lucide-react';

interface ErrorStateProps {
  message?: string;
  onRetry?: () => void;
}

export const ErrorState: React.FC<ErrorStateProps> = ({
  message = "Unable to sync with KSP Central Intelligence Mesh Server.",
  onRetry
}) => {
  return (
    <div className="p-6 rounded-2xl bg-red-950/40 border border-red-500/30 flex items-center justify-between text-red-200">
      <div className="flex items-center space-x-3">
        <AlertOctagon className="w-6 h-6 text-red-400 flex-shrink-0 animate-pulse" />
        <div>
          <h5 className="text-xs font-bold uppercase tracking-wider text-red-400">Connection Anomaly Detected</h5>
          <p className="text-xs text-slate-300 mt-0.5">{message}</p>
        </div>
      </div>
      {onRetry && (
        <button
          onClick={onRetry}
          className="px-3.5 py-1.5 rounded-xl bg-red-600/30 hover:bg-red-600 text-white text-xs font-semibold border border-red-500/40 flex items-center space-x-1.5 transition-colors"
        >
          <RotateCcw size={14} />
          <span>Retry Sync</span>
        </button>
      )}
    </div>
  );
};
