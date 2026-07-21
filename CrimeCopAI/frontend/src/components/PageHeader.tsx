import React from 'react';
import { Breadcrumb } from './Breadcrumb';

interface PageHeaderProps {
  title: string;
  subtitle?: string;
  badge?: string;
  actions?: React.ReactNode;
}

export const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  subtitle,
  badge,
  actions
}) => {
  return (
    <div className="flex flex-col md:flex-row md:items-center justify-between pb-6 border-b border-blue-500/15 gap-4">
      <div>
        <Breadcrumb />
        <div className="flex items-center space-x-3">
          <h1 className="text-2xl font-black text-white font-mono tracking-tight glow-text-blue">
            {title}
          </h1>
          {badge && (
            <span className="px-2.5 py-0.5 text-xs font-bold rounded-full bg-blue-600/30 text-cyan-300 border border-cyan-500/30 shadow-glow-sm">
              {badge}
            </span>
          )}
        </div>
        {subtitle && <p className="text-xs text-slate-400 mt-1 font-medium">{subtitle}</p>}
      </div>

      {actions && <div className="flex items-center space-x-3">{actions}</div>}
    </div>
  );
};
