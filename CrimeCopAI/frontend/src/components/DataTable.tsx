import React, { useState } from 'react';
import { ChevronLeft, ChevronRight, ArrowUpDown } from 'lucide-react';

export interface Column<T> {
  header: string;
  accessor: keyof T | ((row: T) => React.ReactNode);
  sortable?: boolean;
}

interface DataTableProps<T> {
  columns: Column<T>[];
  data: T[];
  keyExtractor: (item: T) => string;
  pageSize?: number;
}

export function DataTable<T>({ columns, data, keyExtractor, pageSize = 5 }: DataTableProps<T>) {
  const [currentPage, setCurrentPage] = useState(1);

  const totalPages = Math.ceil(data.length / pageSize) || 1;
  const currentData = data.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  return (
    <div className="glass-card rounded-2xl border border-blue-500/20 overflow-hidden shadow-xl">
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs text-slate-300">
          <thead className="bg-slate-900/90 text-slate-400 uppercase tracking-wider text-[10px] font-bold border-b border-blue-500/20">
            <tr>
              {columns.map((col, idx) => (
                <th key={idx} className="px-5 py-3.5">
                  <div className="flex items-center space-x-1">
                    <span>{col.header}</span>
                    {col.sortable && <ArrowUpDown className="w-3 h-3 text-slate-500 hover:text-slate-300 cursor-pointer" />}
                  </div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {currentData.length > 0 ? (
              currentData.map((row) => (
                <tr key={keyExtractor(row)} className="hover:bg-blue-600/10 transition-colors">
                  {columns.map((col, idx) => (
                    <td key={idx} className="px-5 py-4 font-medium">
                      {typeof col.accessor === 'function' ? col.accessor(row) : (row[col.accessor] as unknown as React.ReactNode)}
                    </td>
                  ))}
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan={columns.length} className="px-5 py-8 text-center text-slate-400">
                  No police records found matching the active criteria.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination Footer */}
      <div className="px-5 py-3.5 bg-slate-900/80 border-t border-blue-500/20 flex items-center justify-between text-xs text-slate-400">
        <span>
          Showing <span className="text-white font-bold">{data.length ? (currentPage - 1) * pageSize + 1 : 0}</span> to{' '}
          <span className="text-white font-bold">{Math.min(currentPage * pageSize, data.length)}</span> of{' '}
          <span className="text-white font-bold">{data.length}</span> entries
        </span>

        <div className="flex items-center space-x-2">
          <button
            onClick={() => setCurrentPage((p) => Math.max(p - 1, 1))}
            disabled={currentPage === 1}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-blue-600/30 text-slate-300 disabled:opacity-40 disabled:hover:bg-slate-800 transition-colors"
          >
            <ChevronLeft size={16} />
          </button>
          <span className="font-mono text-cyan-300 text-xs px-2">
            Page {currentPage} of {totalPages}
          </span>
          <button
            onClick={() => setCurrentPage((p) => Math.min(p + 1, totalPages))}
            disabled={currentPage === totalPages}
            className="p-1.5 rounded-lg bg-slate-800 hover:bg-blue-600/30 text-slate-300 disabled:opacity-40 disabled:hover:bg-slate-800 transition-colors"
          >
            <ChevronRight size={16} />
          </button>
        </div>
      </div>
    </div>
  );
}
