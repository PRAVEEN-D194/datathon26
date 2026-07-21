import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Maximize2, Minimize2, MoreVertical, Download } from 'lucide-react';

interface ChartCardProps {
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  actionButtons?: React.ReactNode;
}

export const ChartCard: React.FC<ChartCardProps> = ({
  title,
  subtitle,
  children,
  actionButtons
}) => {
  const [isFullscreen, setIsFullscreen] = useState(false);

  return (
    <motion.div
      layout
      className={`glass-card rounded-2xl p-5 border border-blue-500/20 shadow-xl transition-all ${
        isFullscreen ? 'fixed inset-4 z-50 bg-[#081229]/95 backdrop-blur-2xl flex flex-col justify-between' : 'relative'
      }`}
    >
      {/* Header */}
      <div className="flex items-center justify-between border-b border-blue-500/15 pb-3 mb-4">
        <div>
          <h3 className="text-sm font-extrabold text-white uppercase tracking-wider flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-pulse" />
            <span>{title}</span>
          </h3>
          {subtitle && <p className="text-[11px] text-slate-400 mt-0.5">{subtitle}</p>}
        </div>

        <div className="flex items-center space-x-2">
          {actionButtons}
          
          <button
            onClick={() => setIsFullscreen(!isFullscreen)}
            className="p-1.5 rounded-lg bg-slate-800/80 hover:bg-blue-600/30 text-slate-300 hover:text-white border border-slate-700/50 transition-colors"
            title={isFullscreen ? "Exit Fullscreen" : "Fullscreen View"}
          >
            {isFullscreen ? <Minimize2 size={16} /> : <Maximize2 size={16} />}
          </button>
        </div>
      </div>

      {/* Body / Chart Content */}
      <div className={`w-full ${isFullscreen ? 'flex-1 h-[80vh]' : 'h-72'}`}>
        {children}
      </div>
    </motion.div>
  );
};
