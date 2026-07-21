import React, { useState } from 'react';
import { PageHeader } from '../components/PageHeader';
import { DataTable, Column } from '../components/DataTable';
import { mockIntelligenceReports } from '../data/mockData';
import { IntelligenceReport } from '../types';
import { Download, FileText, CheckCircle2, ShieldAlert, FileSpreadsheet, Lock } from 'lucide-react';

export const ReportsPage: React.FC = () => {
  const [downloadNotice, setDownloadNotice] = useState<string | null>(null);

  const handleDownload = (reportTitle: string) => {
    setDownloadNotice(`Downloading secure report: ${reportTitle}`);
    setTimeout(() => setDownloadNotice(null), 3000);
  };

  const tableColumns: Column<IntelligenceReport>[] = [
    {
      header: 'Report Code & Title',
      accessor: (row) => (
        <div>
          <div className="flex items-center space-x-2">
            <span className="font-mono text-cyan-400 font-bold text-[11px]">{row.reportCode}</span>
            <span className={`text-[9px] font-bold px-1.5 py-0.5 rounded ${
              row.classification === 'TOP SECRET' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 'bg-blue-600/30 text-cyan-300'
            }`}>
              {row.classification}
            </span>
          </div>
          <p className="text-xs font-semibold text-white mt-0.5">{row.title}</p>
        </div>
      ),
      sortable: true
    },
    {
      header: 'Category',
      accessor: 'category',
      sortable: true
    },
    {
      header: 'District',
      accessor: 'district',
      sortable: true
    },
    {
      header: 'Generated Date',
      accessor: 'dateGenerated',
      sortable: true
    },
    {
      header: 'Status',
      accessor: (row) => (
        <span className={`px-2 py-0.5 text-[10px] font-bold rounded-full ${
          row.status === 'Verified' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-amber-500/20 text-amber-400'
        }`}>
          {row.status}
        </span>
      )
    },
    {
      header: 'Actions',
      accessor: (row) => (
        <button
          onClick={() => handleDownload(row.title)}
          className="px-3 py-1.5 rounded-xl bg-blue-600/30 hover:bg-blue-600 text-cyan-300 hover:text-white border border-cyan-500/30 text-xs font-semibold flex items-center space-x-1.5 transition-all cursor-pointer"
        >
          <Download size={14} />
          <span>PDF ({row.fileSize})</span>
        </button>
      )
    }
  ];

  return (
    <div className="space-y-6 pb-12">
      <PageHeader
        title="Intelligence Reports & Case Audit Archives"
        subtitle="Automated PDF/Excel exports synthesized from KSP district intelligence nodes."
        badge="DIGITAL SIGNATURE ACTIVE"
      />

      {/* Download Notification Toast */}
      {downloadNotice && (
        <div className="p-3 rounded-xl bg-emerald-950/80 border border-emerald-500/40 text-emerald-300 text-xs font-semibold flex items-center space-x-2 shadow-lg">
          <CheckCircle2 className="w-4 h-4 text-emerald-400 animate-pulse" />
          <span>{downloadNotice}</span>
        </div>
      )}

      {/* Featured Intelligence Report Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {mockIntelligenceReports.slice(0, 2).map((rep) => (
          <div key={rep.id} className="glass-card rounded-2xl p-5 border border-blue-500/20 shadow-xl flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between border-b border-blue-500/15 pb-2 mb-3">
                <span className="text-[10px] font-mono text-cyan-400 font-bold">{rep.reportCode}</span>
                <span className="text-[9px] font-bold px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30">
                  {rep.classification}
                </span>
              </div>
              <h3 className="text-sm font-bold text-white">{rep.title}</h3>
              <p className="text-xs text-slate-300 mt-1.5 leading-relaxed">{rep.summary}</p>
            </div>

            <div className="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between">
              <span className="text-[11px] text-slate-400 font-mono">Size: {rep.fileSize}</span>
              <button
                onClick={() => handleDownload(rep.title)}
                className="px-4 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-bold text-xs shadow-glow-sm flex items-center space-x-2 cursor-pointer"
              >
                <Download size={14} />
                <span>Export PDF Dossier</span>
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Complete Historical Audit Table */}
      <div className="space-y-3">
        <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">All Synthesized Intelligence Reports</h3>
        <DataTable
          columns={tableColumns}
          data={mockIntelligenceReports}
          keyExtractor={(item) => item.id}
          pageSize={5}
        />
      </div>
    </div>
  );
};
