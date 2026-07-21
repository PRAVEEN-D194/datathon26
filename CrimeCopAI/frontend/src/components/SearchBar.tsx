import React from 'react';
import { Search, Filter, X } from 'lucide-react';

interface SearchBarProps {
  value: string;
  onChange: (val: string) => void;
  placeholder?: string;
  onClear?: () => void;
  onToggleFilters?: () => void;
  showFilterToggle?: boolean;
  filterCount?: number;
}

export const SearchBar: React.FC<SearchBarProps> = ({
  value,
  onChange,
  placeholder = "Search FIRs, Suspects, Locations or Keywords...",
  onClear,
  onToggleFilters,
  showFilterToggle = true,
  filterCount = 0
}) => {
  return (
    <div className="flex items-center space-x-3 w-full">
      <div className="relative flex-1">
        <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
        <input
          type="text"
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          className="w-full pl-10 pr-10 py-2.5 bg-slate-900/80 border border-blue-500/25 rounded-xl text-xs text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all shadow-inner"
        />
        {value && (
          <button
            onClick={onClear}
            className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-white p-0.5"
          >
            <X size={14} />
          </button>
        )}
      </div>

      {showFilterToggle && onToggleFilters && (
        <button
          onClick={onToggleFilters}
          className="relative px-3.5 py-2.5 rounded-xl bg-slate-900/80 border border-blue-500/25 hover:border-blue-500 text-xs text-slate-200 hover:text-white flex items-center space-x-2 transition-all"
        >
          <Filter className="w-4 h-4 text-cyan-400" />
          <span className="hidden sm:inline font-medium">Filters</span>
          {filterCount > 0 && (
            <span className="w-4 h-4 rounded-full bg-blue-600 text-white text-[10px] font-bold flex items-center justify-center">
              {filterCount}
            </span>
          )}
        </button>
      )}
    </div>
  );
};
