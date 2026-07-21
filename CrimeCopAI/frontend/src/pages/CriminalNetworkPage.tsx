import React, { useState } from 'react';
import { PageHeader } from '../components/PageHeader';
import { NetworkGraph } from '../components/NetworkGraph';
import { mockCriminalNodes, mockCriminalLinks } from '../data/mockData';
import { CriminalNode } from '../types';
import { Search, ShieldAlert, User, GitFork, AlertTriangle, FileText, Lock } from 'lucide-react';

export const CriminalNetworkPage: React.FC = () => {
  const [selectedNode, setSelectedNode] = useState<CriminalNode | null>(mockCriminalNodes[0]);
  const [searchQuery, setSearchQuery] = useState('');

  const filteredNodes = mockCriminalNodes.filter(
    (n) =>
      n.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      n.alias.toLowerCase().includes(searchQuery.toLowerCase()) ||
      n.gangAffiliation.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="space-y-6 pb-12">
      <PageHeader
        title="Syndicate & Suspect Network Graph"
        subtitle="Graph neural network visualization mapping criminal nodes, co-accused ties, and financial laundering links."
        badge="NEURAL GRAPH ACTIVE"
      />

      {/* Main Grid: Left Graph Container + Right Suspect Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Interactive Network Graph (2 cols) */}
        <div className="lg:col-span-2 space-y-4">
          {/* Top Search Input */}
          <div className="relative">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search Suspect Name, Alias or Gang Syndicate..."
              className="w-full pl-10 pr-4 py-2.5 bg-slate-900/80 border border-blue-500/25 rounded-xl text-xs text-white placeholder-slate-400 focus:outline-none focus:border-blue-500"
            />
          </div>

          <NetworkGraph
            nodes={filteredNodes}
            links={mockCriminalLinks}
            selectedNode={selectedNode}
            onSelectNode={setSelectedNode}
          />
        </div>

        {/* Right Side Inspector Panel (1 col) */}
        <div className="glass-card rounded-2xl p-5 border border-blue-500/20 flex flex-col justify-between shadow-xl">
          {selectedNode ? (
            <div className="space-y-4">
              <div className="flex items-center justify-between border-b border-blue-500/15 pb-3">
                <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">Suspect Dossier</span>
                <span className="text-[10px] font-mono text-cyan-300 bg-blue-600/30 px-2 py-0.5 rounded border border-cyan-500/30">
                  {selectedNode.id}
                </span>
              </div>

              {/* Suspect Photo & Name Banner */}
              <div className="flex items-center space-x-4">
                <div className="relative w-16 h-16 rounded-2xl overflow-hidden border-2 border-blue-500/40 shadow-neon-blue">
                  <img src={selectedNode.avatar} alt={selectedNode.name} className="w-full h-full object-cover" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-white leading-tight">{selectedNode.name}</h3>
                  <span className="text-xs text-cyan-400 font-mono font-semibold">"{selectedNode.alias}"</span>
                  <div className="mt-1 flex items-center space-x-2">
                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded ${
                      selectedNode.status === 'Absconding'
                        ? 'bg-red-500/20 text-red-400 border border-red-500/30'
                        : selectedNode.status === 'In Custody'
                        ? 'bg-blue-500/20 text-blue-400'
                        : 'bg-amber-500/20 text-amber-400'
                    }`}>
                      {selectedNode.status}
                    </span>
                  </div>
                </div>
              </div>

              {/* Risk Score & Key Attributes */}
              <div className="p-3 rounded-xl bg-slate-900/80 border border-blue-500/20 grid grid-cols-2 gap-2 text-center">
                <div>
                  <span className="text-[10px] text-slate-400 block uppercase">Threat Index</span>
                  <span className="text-lg font-black font-mono text-red-400">{selectedNode.riskScore} / 100</span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-400 block uppercase">Active Charges</span>
                  <span className="text-lg font-black font-mono text-cyan-300">{selectedNode.chargesCount} FIRs</span>
                </div>
              </div>

              {/* Detailed Specs */}
              <div className="space-y-2 text-xs">
                <div className="flex justify-between py-1 border-b border-slate-800">
                  <span className="text-slate-400">Role in Syndicate:</span>
                  <span className="text-white font-medium">{selectedNode.role}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-800">
                  <span className="text-slate-400">Primary Gang:</span>
                  <span className="text-amber-400 font-semibold">{selectedNode.gangAffiliation}</span>
                </div>
                <div className="flex justify-between py-1 border-b border-slate-800">
                  <span className="text-slate-400">Operating District:</span>
                  <span className="text-white font-medium">{selectedNode.primaryDistrict}</span>
                </div>
              </div>

              {/* Connected Suspect Nodes list */}
              <div>
                <h4 className="text-[11px] font-bold text-slate-300 uppercase tracking-wider mb-2">Direct Syndicate Associates</h4>
                <div className="space-y-1.5">
                  {selectedNode.connections.map((connId) => {
                    const connNode = mockCriminalNodes.find((cn) => cn.id === connId);
                    if (!connNode) return null;
                    return (
                      <div
                        key={connId}
                        onClick={() => setSelectedNode(connNode)}
                        className="p-2 rounded-xl bg-slate-900/60 border border-blue-500/15 hover:border-blue-500/40 flex items-center justify-between cursor-pointer transition-colors"
                      >
                        <div className="flex items-center space-x-2">
                          <User size={14} className="text-cyan-400" />
                          <span className="text-xs text-slate-200 font-medium">{connNode.name}</span>
                        </div>
                        <span className="text-[10px] text-amber-400 font-mono">"{connNode.alias}"</span>
                      </div>
                    );
                  })}
                </div>
              </div>
            </div>
          ) : (
            <div className="p-8 text-center text-slate-400">Select any node on the graph to inspect suspect profile.</div>
          )}

          <div className="mt-4 pt-3 border-t border-slate-800 text-center">
            <button
              onClick={() => alert(`Detailed Case File requested for ${selectedNode?.name}`)}
              className="w-full py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold uppercase tracking-wider flex items-center justify-center space-x-2 transition-all shadow-glow-sm cursor-pointer"
            >
              <FileText size={16} />
              <span>Generate Suspect Intelligence Brief</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
