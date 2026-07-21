import React from 'react';
import { motion } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  BarChart,
  Bar
} from 'recharts';
import {
  ShieldAlert,
  Bot,
  MapPin,
  GitFork,
  FileSpreadsheet,
  ArrowUpRight,
  Zap,
  Activity,
  AlertTriangle
} from 'lucide-react';
import { PageHeader } from '../components/PageHeader';
import { StatCard } from '../components/StatCard';
import { ChartCard } from '../components/ChartCard';
import {
  mockStatMetrics,
  mockRecentAlerts,
  mockCrimeTrendData,
  mockDistrictCrimeStats,
  mockUserProfile
} from '../data/mockData';

export const DashboardPage: React.FC = () => {
  const navigate = useNavigate();

  const quickActions = [
    {
      title: 'Launch KSP Intellibot',
      subtitle: 'Conversational Crime Database Synthesis',
      icon: Bot,
      path: '/ai-assistant',
      color: 'from-blue-600 to-cyan-500',
    },
    {
      title: 'Crime Hotspot Map',
      subtitle: 'Live Incident Density & Geofence Filters',
      icon: MapPin,
      path: '/crime-map',
      color: 'from-cyan-500 to-teal-500',
    },
    {
      title: 'Suspect Network Graph',
      subtitle: 'Syndicate Node & Link Inspection',
      icon: GitFork,
      path: '/criminal-network',
      color: 'from-indigo-600 to-blue-500',
    },
    {
      title: 'Generate Intelligence Report',
      subtitle: 'Export High-Level Case Summaries',
      icon: FileSpreadsheet,
      path: '/reports',
      color: 'from-amber-600 to-orange-500',
    },
  ];

  return (
    <div className="space-y-6 pb-12">
      {/* Page Header with User Welcome */}
      <PageHeader
        title={`Welcome, ${mockUserProfile.name}`}
        subtitle={`Badge: ${mockUserProfile.badgeNumber} | Clearance: ${mockUserProfile.clearanceLevel} | Grid Status: ONLINE`}
        badge="KSP COMMAND CENTER"
        actions={
          <button
            onClick={() => navigate('/ai-assistant')}
            className="px-4 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-bold text-xs shadow-neon-blue flex items-center space-x-2 transition-all cursor-pointer"
          >
            <Bot size={16} />
            <span>Launch Intellibot Copilot</span>
          </button>
        }
      />

      {/* Stat KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {mockStatMetrics.map((stat, idx) => (
          <StatCard key={stat.id} stat={stat} index={idx} />
        ))}
      </div>

      {/* Main Charts & Alert Feed Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Crime Velocity Monthly Trend (Area Chart) */}
        <div className="lg:col-span-2">
          <ChartCard
            title="Karnataka Monthly Crime Velocity (2026)"
            subtitle="Comparing Cybercrime, Financial Fraud, Robbery, and Narcotics"
          >
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={mockCrimeTrendData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="cyberGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2563EB" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#2563EB" stopOpacity={0.0} />
                  </linearGradient>
                  <linearGradient id="fraudGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#06B6D4" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#06B6D4" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#1E3A8A" opacity={0.3} />
                <XAxis dataKey="month" stroke="#94A3B8" fontSize={11} tickLine={false} />
                <YAxis stroke="#94A3B8" fontSize={11} tickLine={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#10203D',
                    borderColor: 'rgba(59, 130, 246, 0.3)',
                    borderRadius: '12px',
                    color: '#F8FAFC',
                    fontSize: '12px',
                  }}
                />
                <Area type="monotone" dataKey="cybercrime" name="Cybercrime" stroke="#2563EB" fillOpacity={1} fill="url(#cyberGrad)" strokeWidth={2} />
                <Area type="monotone" dataKey="fraud" name="Financial Fraud" stroke="#06B6D4" fillOpacity={1} fill="url(#fraudGrad)" strokeWidth={2} />
              </AreaChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* Live Alerts Feed Panel */}
        <div className="glass-card rounded-2xl p-5 border border-blue-500/20 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-blue-500/15 pb-3 mb-3">
              <div className="flex items-center space-x-2">
                <ShieldAlert className="w-4 h-4 text-red-400 animate-pulse" />
                <h3 className="text-xs font-bold text-white uppercase tracking-wider">Critical Live Alerts</h3>
              </div>
              <span className="text-[10px] font-mono text-cyan-300 bg-blue-600/30 px-2 py-0.5 rounded border border-cyan-500/30">
                4 UNRESOLVED
              </span>
            </div>

            <div className="space-y-3 max-h-72 overflow-y-auto pr-1">
              {mockRecentAlerts.map((alert) => (
                <div
                  key={alert.id}
                  onClick={() => navigate('/crime-map')}
                  className="p-3 rounded-xl bg-slate-900/70 border border-blue-500/15 hover:border-blue-500/50 transition-all cursor-pointer group"
                >
                  <div className="flex items-center justify-between">
                    <span className="text-[10px] font-bold text-cyan-400 font-mono">{alert.firNumber}</span>
                    <span className="text-[10px] text-slate-400">{alert.timestamp}</span>
                  </div>
                  <h4 className="text-xs font-semibold text-white mt-1 group-hover:text-blue-300 transition-colors">
                    {alert.title}
                  </h4>
                  <div className="mt-2 flex items-center justify-between text-[10px]">
                    <span className="text-slate-400">{alert.district}</span>
                    <span className={`px-1.5 py-0.5 rounded font-bold ${
                      alert.severity === 'Critical' ? 'bg-red-500/20 text-red-400' : 'bg-amber-500/20 text-amber-400'
                    }`}>
                      {alert.severity}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <button
            onClick={() => navigate('/reports')}
            className="w-full mt-4 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-cyan-300 flex items-center justify-center space-x-1 border border-slate-700 transition-colors"
          >
            <span>View Complete Alert Audit Log</span>
            <ArrowUpRight size={14} />
          </button>
        </div>
      </div>

      {/* District Crime Breakdown & Quick Action Shortcuts */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* District Crime Breakdown (Bar Chart) */}
        <div className="lg:col-span-2">
          <ChartCard
            title="District Total Crime Volume & High Severity Cases"
            subtitle="Comparing Bengaluru Urban, Mysuru, Mangaluru, Hubballi & Belagavi"
          >
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={mockDistrictCrimeStats} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1E3A8A" opacity={0.3} />
                <XAxis dataKey="district" stroke="#94A3B8" fontSize={11} tickLine={false} />
                <YAxis stroke="#94A3B8" fontSize={11} tickLine={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#10203D',
                    borderColor: 'rgba(59, 130, 246, 0.3)',
                    borderRadius: '12px',
                    color: '#F8FAFC',
                    fontSize: '12px',
                  }}
                />
                <Bar dataKey="totalCases" name="Total FIRs" fill="#2563EB" radius={[6, 6, 0, 0]} />
                <Bar dataKey="highSeverity" name="High Severity" fill="#EF4444" radius={[6, 6, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* Quick Action Cards */}
        <div className="space-y-3">
          <h3 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Quick Command Shortcuts</h3>

          {quickActions.map((action, idx) => {
            const Icon = action.icon;
            return (
              <motion.div
                key={action.title}
                whileHover={{ scale: 1.02, x: 4 }}
                onClick={() => navigate(action.path)}
                className="glass-card rounded-2xl p-4 border border-blue-500/20 hover:border-cyan-400/50 flex items-center justify-between cursor-pointer transition-all shadow-md group"
              >
                <div className="flex items-center space-x-3">
                  <div className={`w-10 h-10 rounded-xl bg-gradient-to-tr ${action.color} p-2 text-white flex items-center justify-center shadow-glow-sm`}>
                    <Icon className="w-5 h-5" />
                  </div>
                  <div>
                    <h4 className="text-xs font-bold text-white group-hover:text-cyan-300 transition-colors">
                      {action.title}
                    </h4>
                    <p className="text-[10px] text-slate-400 mt-0.5">{action.subtitle}</p>
                  </div>
                </div>

                <ArrowUpRight className="w-4 h-4 text-slate-500 group-hover:text-cyan-300 transition-colors" />
              </motion.div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
