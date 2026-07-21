import React from 'react';
import { DistrictName, CrimeCategory, CrimeSeverity } from '../types';
import { RotateCcw } from 'lucide-react';

interface FilterPanelProps {
  selectedDistrict: string;
  setSelectedDistrict: (val: string) => void;
  selectedCategory: string;
  setSelectedCategory: (val: string) => void;
  selectedSeverity: string;
  setSelectedSeverity: (val: string) => void;
  dateRange: string;
  setDateRange: (val: string) => void;
  onReset: () => void;
}

const districts: (DistrictName | 'All Districts')[] = [
  'All Districts',
  'Bengaluru Urban',
  'Mysuru',
  'Mangaluru',
  'Hubballi-Dharwad',
  'Belagavi',
  'Kalaburagi',
  'Shivamogga'
];

const categories: (CrimeCategory | 'All Categories')[] = [
  'All Categories',
  'Cybercrime',
  'Robbery',
  'Homicide',
  'Narcotics',
  'Financial Fraud',
  'Vehicle Theft',
  'Public Order'
];

const severities: (CrimeSeverity | 'All Severities')[] = [
  'All Severities',
  'Low',
  'Medium',
  'High',
  'Critical'
];

export const FilterPanel: React.FC<FilterPanelProps> = ({
  selectedDistrict,
  setSelectedDistrict,
  selectedCategory,
  setSelectedCategory,
  selectedSeverity,
  setSelectedSeverity,
  dateRange,
  setDateRange,
  onReset
}) => {
  return (
    <div className="glass-panel p-4 rounded-2xl border border-blue-500/20 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 shadow-lg">
      {/* District Filter */}
      <div>
        <label className="block text-[11px] font-semibold text-slate-300 uppercase tracking-wider mb-1">District</label>
        <select
          value={selectedDistrict}
          onChange={(e) => setSelectedDistrict(e.target.value)}
          className="w-full py-2 px-3 bg-slate-900 border border-blue-500/30 rounded-xl text-xs text-white focus:outline-none focus:border-blue-500"
        >
          {districts.map((d) => (
            <option key={d} value={d} className="bg-slate-900 text-white">{d}</option>
          ))}
        </select>
      </div>

      {/* Crime Category */}
      <div>
        <label className="block text-[11px] font-semibold text-slate-300 uppercase tracking-wider mb-1">Crime Category</label>
        <select
          value={selectedCategory}
          onChange={(e) => setSelectedCategory(e.target.value)}
          className="w-full py-2 px-3 bg-slate-900 border border-blue-500/30 rounded-xl text-xs text-white focus:outline-none focus:border-blue-500"
        >
          {categories.map((c) => (
            <option key={c} value={c} className="bg-slate-900 text-white">{c}</option>
          ))}
        </select>
      </div>

      {/* Severity */}
      <div>
        <label className="block text-[11px] font-semibold text-slate-300 uppercase tracking-wider mb-1">Threat Severity</label>
        <select
          value={selectedSeverity}
          onChange={(e) => setSelectedSeverity(e.target.value)}
          className="w-full py-2 px-3 bg-slate-900 border border-blue-500/30 rounded-xl text-xs text-white focus:outline-none focus:border-blue-500"
        >
          {severities.map((s) => (
            <option key={s} value={s} className="bg-slate-900 text-white">{s}</option>
          ))}
        </select>
      </div>

      {/* Date Range */}
      <div>
        <label className="block text-[11px] font-semibold text-slate-300 uppercase tracking-wider mb-1">Timeframe</label>
        <select
          value={dateRange}
          onChange={(e) => setDateRange(e.target.value)}
          className="w-full py-2 px-3 bg-slate-900 border border-blue-500/30 rounded-xl text-xs text-white focus:outline-none focus:border-blue-500"
        >
          <option value="7d">Last 7 Days</option>
          <option value="30d">Last 30 Days</option>
          <option value="90d">Last 90 Days</option>
          <option value="1y">Year to Date (2026)</option>
        </select>
      </div>

      {/* Reset Button */}
      <div className="flex items-end">
        <button
          onClick={onReset}
          className="w-full py-2 px-3 rounded-xl bg-slate-800/80 hover:bg-slate-700 text-xs font-semibold text-slate-300 hover:text-white flex items-center justify-center space-x-2 border border-slate-700 transition-colors"
        >
          <RotateCcw className="w-3.5 h-3.5" />
          <span>Reset Filters</span>
        </button>
      </div>
    </div>
  );
};
