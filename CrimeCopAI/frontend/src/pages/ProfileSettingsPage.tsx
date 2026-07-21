import React, { useState } from 'react';
import { PageHeader } from '../components/PageHeader';
import { mockUserProfile } from '../data/mockData';
import { Shield, User, Bell, Lock, Key, CheckCircle2, Copy, Check, Radio } from 'lucide-react';

export const ProfileSettingsPage: React.FC = () => {
  const [copiedKey, setCopiedKey] = useState(false);
  const [criticalAlertsEnabled, setCriticalAlertsEnabled] = useState(true);
  const [aiAnalysisNotify, setAiAnalysisNotify] = useState(true);
  const [auditLogNotify, setAuditLogNotify] = useState(false);
  const [apiKey] = useState('ksp_live_sec_89421_99x28174a901ff28');

  const handleCopyKey = () => {
    navigator.clipboard.writeText(apiKey);
    setCopiedKey(true);
    setTimeout(() => setCopiedKey(false), 2000);
  };

  return (
    <div className="space-y-6 pb-12">
      <PageHeader
        title="Officer Profile & Command Settings"
        subtitle="Manage officer credentials, notification thresholds, security keys, and system audit logs."
        badge="LEVEL 5 TOP SECRET"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Officer Profile Card */}
        <div className="glass-card rounded-2xl p-6 border border-blue-500/20 shadow-xl space-y-4">
          <div className="flex flex-col items-center text-center pb-4 border-b border-slate-700/60">
            <div className="w-20 h-20 rounded-2xl bg-gradient-to-tr from-blue-600 via-blue-500 to-cyan-400 p-1 shadow-neon-blue flex items-center justify-center mb-3">
              <div className="w-full h-full bg-[#081229] rounded-[14px] flex items-center justify-center text-xl font-bold text-white font-mono">
                IG
              </div>
            </div>
            <h3 className="text-base font-bold text-white">{mockUserProfile.name}</h3>
            <span className="text-xs text-cyan-400 font-mono font-semibold mt-0.5">{mockUserProfile.badgeNumber}</span>
            <span className="mt-2 text-[10px] font-bold px-2.5 py-0.5 rounded-full bg-red-500/20 text-red-400 border border-red-500/30">
              {mockUserProfile.clearanceLevel}
            </span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="flex justify-between py-1.5 border-b border-slate-800">
              <span className="text-slate-400">Department:</span>
              <span className="text-white font-medium">{mockUserProfile.department}</span>
            </div>
            <div className="flex justify-between py-1.5 border-b border-slate-800">
              <span className="text-slate-400">Primary District:</span>
              <span className="text-white font-medium">{mockUserProfile.district}</span>
            </div>
            <div className="flex justify-between py-1.5 border-b border-slate-800">
              <span className="text-slate-400">Officer Email:</span>
              <span className="text-cyan-300 font-mono">{mockUserProfile.email}</span>
            </div>
            <div className="flex justify-between py-1.5 border-b border-slate-800">
              <span className="text-slate-400">Active Mesh IP:</span>
              <span className="text-emerald-400 font-mono">{mockUserProfile.activeSessionIp}</span>
            </div>
          </div>
        </div>

        {/* Right Column: Settings & API Integration Keys (2 cols) */}
        <div className="lg:col-span-2 space-y-6">
          {/* API Keys for Backend Plug-and-Play Integration */}
          <div className="glass-card rounded-2xl p-6 border border-blue-500/20 shadow-xl space-y-4">
            <div className="flex items-center justify-between border-b border-blue-500/15 pb-3">
              <div className="flex items-center space-x-2">
                <Key className="w-4 h-4 text-cyan-400" />
                <h3 className="text-xs font-bold text-white uppercase tracking-wider">KSP API Client Token</h3>
              </div>
              <span className="text-[10px] font-mono text-emerald-400 bg-emerald-500/20 px-2 py-0.5 rounded border border-emerald-500/30">
                ACTIVE PIPELINE
              </span>
            </div>

            <p className="text-xs text-slate-300">
              Use this security token to connect real REST/GraphQL backend APIs or LangChain FastAPI microservices directly to the frontend components.
            </p>

            <div className="flex items-center space-x-2 bg-slate-900 border border-blue-500/30 rounded-xl p-2.5 font-mono text-xs text-cyan-300">
              <span className="flex-1 truncate">{apiKey}</span>
              <button
                onClick={handleCopyKey}
                className="px-3 py-1 rounded-lg bg-blue-600/30 hover:bg-blue-600 text-cyan-300 hover:text-white border border-cyan-500/30 transition-colors flex items-center space-x-1"
              >
                {copiedKey ? <Check size={14} className="text-emerald-400" /> : <Copy size={14} />}
                <span>{copiedKey ? 'Copied' : 'Copy'}</span>
              </button>
            </div>
          </div>

          {/* Notification Thresholds */}
          <div className="glass-card rounded-2xl p-6 border border-blue-500/20 shadow-xl space-y-4">
            <div className="flex items-center space-x-2 border-b border-blue-500/15 pb-3">
              <Bell className="w-4 h-4 text-cyan-400" />
              <h3 className="text-xs font-bold text-white uppercase tracking-wider">Notification & Dispatch Controls</h3>
            </div>

            <div className="space-y-3">
              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-blue-500/15">
                <div>
                  <h4 className="text-xs font-bold text-white">Critical Severity FIR Alerts</h4>
                  <p className="text-[11px] text-slate-400">Push instant popup & audio chime on critical crime events</p>
                </div>
                <input
                  type="checkbox"
                  checked={criticalAlertsEnabled}
                  onChange={(e) => setCriticalAlertsEnabled(e.target.checked)}
                  className="w-4 h-4 accent-blue-600 cursor-pointer"
                />
              </div>

              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-blue-500/15">
                <div>
                  <h4 className="text-xs font-bold text-white">AI Intellibot Pattern Warnings</h4>
                  <p className="text-[11px] text-slate-400">Notify when AI flags new syndicate MO correlations</p>
                </div>
                <input
                  type="checkbox"
                  checked={aiAnalysisNotify}
                  onChange={(e) => setAiAnalysisNotify(e.target.checked)}
                  className="w-4 h-4 accent-blue-600 cursor-pointer"
                />
              </div>

              <div className="flex items-center justify-between p-3 rounded-xl bg-slate-900/60 border border-blue-500/15">
                <div>
                  <h4 className="text-xs font-bold text-white">System Security Audit Trail Logs</h4>
                  <p className="text-[11px] text-slate-400">Log all API read/write transactions into encrypted database</p>
                </div>
                <input
                  type="checkbox"
                  checked={auditLogNotify}
                  onChange={(e) => setAuditLogNotify(e.target.checked)}
                  className="w-4 h-4 accent-blue-600 cursor-pointer"
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
