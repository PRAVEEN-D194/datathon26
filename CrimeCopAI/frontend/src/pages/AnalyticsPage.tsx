import React, { useState } from 'react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from 'recharts';
import { Download, FileSpreadsheet, Filter, CheckCircle2, ShieldAlert } from 'lucide-react';
import { PageHeader } from '../components/PageHeader';
import { ChartCard } from '../components/ChartCard';
import { FilterPanel } from '../components/FilterPanel';
import { mockCrimeTrendData, mockDistrictCrimeStats } from '../data/mockData';

export const AnalyticsPage: React.FC = () => {
  const [selectedDistrict, setSelectedDistrict] = useState('All Districts');
  const [selectedCategory, setSelectedCategory] = useState('All Categories');
  const [selectedSeverity, setSelectedSeverity] = useState('All Severities');
  const [dateRange, setDateRange] = useState('30d');
  const [exportNotice, setExportNotice] = useState<string | null>(null);

  const pieData = [
    { name: 'Critical Severity', value: 24, color: '#EF4444' },
    { name: 'High Severity', value: 38, color: '#F59E0B' },
    { name: 'Medium Severity', value: 26, color: '#3B82F6' },
    { name: 'Low Severity', value: 12, color: '#10B981' }
  ];

  const predictiveForecastData = [
    { month: 'Jul (Actual)', actual: 810, forecast: 810 },
    { month: 'Aug (Forecast)', actual: null, forecast: 890 },
    { month: 'Sep (Forecast)', actual: null, forecast: 950 },
    { month: 'Oct (Forecast)', actual: null, forecast: 1020 },
    { month: 'Nov (Forecast)', actual: null, forecast: 980 },
    { month: 'Dec (Forecast)', actual: null, forecast: 910 }
  ];

  const handleExport = (format: string) => {
    setExportNotice(`Successfully exported KSP Crime Analytics Report as ${format.toUpperCase()}`);
    setTimeout(() => setExportNotice(null), 3000);
  };

  const handleResetFilters = () => {
    setSelectedDistrict('All Districts');
    setSelectedCategory('All Categories');
    setSelectedSeverity('All Severities');
    setDateRange('30d');
  };

  return (
    <div className="space-y-6 pb-12">
      <PageHeader
        title="Crime Analytics & Intelligence Engine"
        subtitle="Deep statistical modeling, predictive forecasts, and district risk heat matrices."
        badge="AI PREDICTIVE ACTIVE"
        actions={
          <div className="flex items-center space-x-2">
            <button
              onClick={() => handleExport('csv')}
              className="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-xs font-semibold text-cyan-300 flex items-center space-x-2 border border-slate-700 transition-colors"
            >
              <FileSpreadsheet size={16} />
              <span>Export CSV</span>
            </button>
            <button
              onClick={() => handleExport('pdf')}
              className="px-4 py-2 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-bold text-xs shadow-neon-blue flex items-center space-x-2 transition-all cursor-pointer"
            >
              <Download size={16} />
              <span>Export PDF Intelligence Report</span>
            </button>
          </div>
        }
      />

      {/* Export Notification Toast */}
      {exportNotice && (
        <div className="p-3 rounded-xl bg-emerald-950/80 border border-emerald-500/40 text-emerald-300 text-xs font-semibold flex items-center space-x-2 shadow-lg">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          <span>{exportNotice}</span>
        </div>
      )}

      {/* Filter Panel */}
      <FilterPanel
        selectedDistrict={selectedDistrict}
        setSelectedDistrict={setSelectedDistrict}
        selectedCategory={selectedCategory}
        setSelectedCategory={setSelectedCategory}
        selectedSeverity={selectedSeverity}
        setSelectedSeverity={setSelectedSeverity}
        dateRange={dateRange}
        setDateRange={setDateRange}
        onReset={handleResetFilters}
      />

      {/* Top Row: Line Chart + Pie Chart */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Line Chart: Multi-Category Temporal Velocity */}
        <div className="lg:col-span-2">
          <ChartCard
            title="Temporal Crime Velocity & Category Growth"
            subtitle="Tracking monthly trends in Cybercrime, Financial Fraud, Robbery & Narcotics"
          >
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={mockCrimeTrendData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#1E3A8A" opacity={0.3} />
                <XAxis dataKey="month" stroke="#94A3B8" fontSize={11} tickLine={false} />
                <YAxis stroke="#94A3B8" fontSize={11} tickLine={false} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#10203D',
                    borderColor: 'rgba(59, 130, 246, 0.3)',
                    borderRadius: '12px',
                    color: '#F8FAFC',
                    fontSize: '12px'
                  }}
                />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Line type="monotone" dataKey="cybercrime" name="Cybercrime" stroke="#2563EB" strokeWidth={3} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="fraud" name="Financial Fraud" stroke="#06B6D4" strokeWidth={2} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="narcotics" name="Narcotics" stroke="#F59E0B" strokeWidth={2} dot={{ r: 4 }} />
                <Line type="monotone" dataKey="robbery" name="Robbery" stroke="#EF4444" strokeWidth={2} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* Pie Chart: Threat Severity Breakdown */}
        <div className="glass-card rounded-2xl p-5 border border-blue-500/20 flex flex-col justify-between">
          <div>
            <h3 className="text-xs font-bold text-white uppercase tracking-wider mb-1">Threat Severity Distribution</h3>
            <p className="text-[11px] text-slate-400 mb-4">Percentage breakdown across active FIRs</p>

            <div className="w-full h-52">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={pieData}
                    cx="50%"
                    cy="50%"
                    innerRadius={50}
                    outerRadius={80}
                    paddingAngle={4}
                    dataKey="value"
                  >
                    {pieData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip
                    contentStyle={{
                      backgroundColor: '#10203D',
                      borderColor: 'rgba(59, 130, 246, 0.3)',
                      borderRadius: '12px',
                      color: '#F8FAFC',
                      fontSize: '12px'
                    }}
                  />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="grid grid-cols-2 gap-2 mt-2 pt-2 border-t border-slate-800">
            {pieData.map((item) => (
              <div key={item.name} className="flex items-center space-x-2 text-[11px]">
                <span className="w-2.5 h-2.5 rounded-full" style={{ backgroundColor: item.color }} />
                <span className="text-slate-300 font-medium">{item.name} ({item.value}%)</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Row: Predictive Forecast + District Heat Matrix */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Area Chart: AI Predictive Cybercrime Forecast */}
        <div className="lg:col-span-2">
          <ChartCard
            title="AI Predictive Cybercrime Forecast (H2 2026)"
            subtitle="Machine Learning model predicting incident surge based on historical vectors"
          >
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={predictiveForecastData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="forecastGrad" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#F59E0B" stopOpacity={0.8} />
                    <stop offset="95%" stopColor="#F59E0B" stopOpacity={0.0} />
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
                    fontSize: '12px'
                  }}
                />
                <Area type="monotone" dataKey="forecast" name="Predicted Incidents" stroke="#F59E0B" fillOpacity={1} fill="url(#forecastGrad)" strokeWidth={2} strokeDasharray="4 4" />
                <Area type="monotone" dataKey="actual" name="Actual Incidents" stroke="#2563EB" fill="#2563EB" strokeWidth={3} />
              </AreaChart>
            </ResponsiveContainer>
          </ChartCard>
        </div>

        {/* District Risk Heat Matrix Panel */}
        <div className="glass-card rounded-2xl p-5 border border-blue-500/20 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between border-b border-blue-500/15 pb-3 mb-3">
              <div className="flex items-center space-x-2">
                <ShieldAlert className="w-4 h-4 text-cyan-400" />
                <h3 className="text-xs font-bold text-white uppercase tracking-wider">District Risk Density Index</h3>
              </div>
            </div>

            <div className="space-y-3">
              {mockDistrictCrimeStats.map((ds) => (
                <div key={ds.district} className="space-y-1">
                  <div className="flex justify-between text-xs font-medium">
                    <span className="text-slate-300">{ds.district}</span>
                    <span className="text-cyan-400 font-mono font-bold">{ds.riskScore} / 100 Risk</span>
                  </div>
                  <div className="w-full h-2 rounded-full bg-slate-900 overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${
                        ds.riskScore >= 80 ? 'bg-red-500' : ds.riskScore >= 50 ? 'bg-amber-500' : 'bg-emerald-500'
                      }`}
                      style={{ width: `${ds.riskScore}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-800 text-[10px] text-slate-400 text-center">
            Updated via KSP District Intelligence Nodes every 15 minutes.
          </div>
        </div>
      </div>
    </div>
  );
};
