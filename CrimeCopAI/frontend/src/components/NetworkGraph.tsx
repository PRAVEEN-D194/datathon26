import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { CriminalNode, CriminalLink } from '../types';
import { ShieldAlert, User, Zap } from 'lucide-react';

interface NetworkGraphProps {
  nodes: CriminalNode[];
  links: CriminalLink[];
  selectedNode: CriminalNode | null;
  onSelectNode: (node: CriminalNode) => void;
}

export const NetworkGraph: React.FC<NetworkGraphProps> = ({
  nodes,
  links,
  selectedNode,
  onSelectNode,
}) => {
  const [zoomLevel, setZoomLevel] = useState(1);

  // Layout coordinates map for 5 nodes on a futuristic radar grid
  const nodePositions: Record<string, { x: number; y: number }> = {
    'NODE-101': { x: 300, y: 180 }, // Phantom (Center Top)
    'NODE-102': { x: 150, y: 320 }, // Karan Nair (Left)
    'NODE-103': { x: 450, y: 300 }, // Ananya Sharma (Right)
    'NODE-104': { x: 320, y: 440 }, // Rahim Khan (Bottom)
    'NODE-105': { x: 140, y: 480 }, // Siddharth Varma (Bottom Left)
  };

  return (
    <div className="relative w-full h-[550px] bg-[#050B18] rounded-2xl border border-blue-500/20 overflow-hidden shadow-2xl flex items-center justify-center select-none">
      {/* Background Radar Grid Circles */}
      <div className="absolute inset-0 flex items-center justify-center opacity-20 pointer-events-none">
        <div className="w-[500px] h-[500px] rounded-full border border-blue-500 animate-pulse-slow" />
        <div className="w-[350px] h-[350px] rounded-full border border-cyan-500 absolute" />
        <div className="w-[200px] h-[200px] rounded-full border border-blue-400 absolute" />
        <div className="absolute w-full h-px bg-blue-500/30" />
        <div className="absolute h-full w-px bg-blue-500/30" />
      </div>

      {/* SVG Link Edge Layer */}
      <svg className="absolute inset-0 w-full h-full pointer-events-none">
        {links.map((link, idx) => {
          const sourcePos = nodePositions[link.source] || { x: 100, y: 100 };
          const targetPos = nodePositions[link.target] || { x: 200, y: 200 };
          const isSelected =
            selectedNode && (selectedNode.id === link.source || selectedNode.id === link.target);

          return (
            <g key={idx}>
              {/* Line */}
              <line
                x1={sourcePos.x}
                y1={sourcePos.y}
                x2={targetPos.x}
                y2={targetPos.y}
                stroke={isSelected ? '#06B6D4' : '#1E3A8A'}
                strokeWidth={isSelected ? 3 : 1.5}
                strokeDasharray={link.relationship === 'Financial Transfer' ? '4,4' : undefined}
                className="transition-all duration-300"
              />
              {/* Relationship Label Pill */}
              <rect
                x={(sourcePos.x + targetPos.x) / 2 - 40}
                y={(sourcePos.y + targetPos.y) / 2 - 10}
                width={80}
                height={18}
                rx={4}
                fill="#081229"
                stroke={isSelected ? '#06B6D4' : '#1E3A8A'}
                strokeWidth={1}
              />
              <text
                x={(sourcePos.x + targetPos.x) / 2}
                y={(sourcePos.y + targetPos.y) / 2 + 3}
                fill={isSelected ? '#60A5FA' : '#94A3B8'}
                fontSize="9"
                fontFamily="JetBrains Mono"
                textAnchor="middle"
                fontWeight="bold"
              >
                {link.relationship}
              </text>
            </g>
          );
        })}
      </svg>

      {/* Nodes Layer */}
      <div
        className="relative w-full h-full transition-transform duration-200"
        style={{ transform: `scale(${zoomLevel})` }}
      >
        {nodes.map((node) => {
          const pos = nodePositions[node.id] || { x: 250, y: 250 };
          const isSelected = selectedNode?.id === node.id;

          return (
            <motion.div
              key={node.id}
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              whileHover={{ scale: 1.15 }}
              onClick={() => onSelectNode(node)}
              style={{ left: pos.x - 36, top: pos.y - 36 }}
              className={`absolute w-18 h-18 rounded-2xl p-1 cursor-pointer transition-all duration-300 flex flex-col items-center justify-center ${
                isSelected
                  ? 'bg-gradient-to-tr from-cyan-500 to-blue-600 shadow-neon-cyan ring-4 ring-cyan-400/40 z-30'
                  : 'bg-[#10203D] border border-blue-500/40 shadow-xl hover:border-cyan-400 z-20'
              }`}
            >
              {/* Avatar Photo */}
              <div className="relative w-10 h-10 rounded-xl overflow-hidden border border-blue-400/30">
                <img src={node.avatar} alt={node.name} className="w-full h-full object-cover" />
                <span
                  className={`absolute top-0 right-0 w-2.5 h-2.5 rounded-full border border-slate-900 ${
                    node.status === 'Absconding'
                      ? 'bg-red-500 animate-ping'
                      : node.status === 'In Custody'
                      ? 'bg-blue-500'
                      : 'bg-amber-500'
                  }`}
                />
              </div>

              {/* Node Alias & Risk Score Badge */}
              <div className="mt-1 flex items-center space-x-1">
                <span className="text-[10px] font-bold text-white font-mono truncate max-w-[70px]">
                  {node.alias}
                </span>
                <span
                  className={`text-[9px] font-black px-1 rounded ${
                    node.riskScore >= 90
                      ? 'bg-red-500/30 text-red-300 border border-red-500/40'
                      : 'bg-amber-500/30 text-amber-300'
                  }`}
                >
                  {node.riskScore}
                </span>
              </div>
            </motion.div>
          );
        })}
      </div>

      {/* Floating Network Controls */}
      <div className="absolute bottom-4 left-4 z-30 flex items-center space-x-2 bg-slate-900/90 border border-blue-500/30 px-3 py-1.5 rounded-xl text-xs">
        <button
          onClick={() => setZoomLevel((z) => Math.min(z + 0.15, 1.4))}
          className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 hover:text-white font-bold"
        >
          +
        </button>
        <span className="font-mono text-[11px] text-cyan-300">{(zoomLevel * 100).toFixed(0)}%</span>
        <button
          onClick={() => setZoomLevel((z) => Math.max(z - 0.15, 0.7))}
          className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 hover:text-white font-bold"
        >
          -
        </button>
      </div>

      {/* Floating Legend */}
      <div className="absolute top-4 right-4 z-30 bg-slate-900/90 border border-blue-500/30 p-2.5 rounded-xl text-[10px] space-y-1.5">
        <div className="font-bold text-slate-300 uppercase tracking-wider mb-1">Graph Legend</div>
        <div className="flex items-center space-x-2">
          <span className="w-2 h-2 rounded-full bg-red-500" />
          <span className="text-slate-400">Absconding (Critical)</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2 h-2 rounded-full bg-amber-500" />
          <span className="text-slate-400">Under Surveillance</span>
        </div>
        <div className="flex items-center space-x-2">
          <span className="w-2 h-2 rounded-full bg-blue-500" />
          <span className="text-slate-400">In Custody</span>
        </div>
      </div>
    </div>
  );
};
