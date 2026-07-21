import React from 'react';
import { motion } from 'framer-motion';
import { ShieldAlert, Cpu, Users, Activity, TrendingUp, TrendingDown } from 'lucide-react';
import { StatMetric } from '../types';

interface StatCardProps {
  stat: StatMetric;
  index?: number;
}

export const StatCard: React.FC<StatCardProps> = ({ stat, index = 0 }) => {
  const getIcon = (name: string) => {
    switch (name) {
      case 'ShieldAlert': return ShieldAlert;
      case 'Cpu': return Cpu;
      case 'Users': return Users;
      case 'Activity': return Activity;
      default: return Activity;
    }
  };

  const IconComponent = getIcon(stat.iconName);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: index * 0.1 }}
      className="glass-card glass-card-hover rounded-2xl p-5 relative overflow-hidden group cursor-pointer"
    >
      {/* Background Accent Mesh Glow */}
      <div className="absolute -right-6 -bottom-6 w-24 h-24 bg-blue-600/10 rounded-full blur-2xl group-hover:bg-blue-500/20 transition-all" />

      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">{stat.title}</span>
        <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-blue-600/20 to-cyan-500/20 border border-blue-500/30 flex items-center justify-center text-cyan-400 group-hover:text-white group-hover:border-cyan-400/50 transition-all">
          <IconComponent className="w-5 h-5" />
        </div>
      </div>

      <div className="mt-3 flex items-baseline justify-between">
        <h3 className="text-2xl font-black text-white font-mono tracking-tight glow-text-blue">
          {stat.value}
        </h3>

        <div className={`flex items-center space-x-1 px-2 py-0.5 rounded-full text-[11px] font-bold ${
          stat.isPositive ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30' : 'bg-red-500/15 text-red-400 border border-red-500/30'
        }`}>
          {stat.isPositive ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
          <span>{stat.change}</span>
        </div>
      </div>

      <p className="text-[11px] text-slate-400 mt-2 font-medium">
        {stat.timeframe}
      </p>
    </motion.div>
  );
};
