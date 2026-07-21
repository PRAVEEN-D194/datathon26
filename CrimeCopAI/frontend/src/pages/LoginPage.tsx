import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Shield, Lock, User, Key, ArrowRight, CheckCircle2, ShieldCheck } from 'lucide-react';
import { UserRole } from '../types';

export const LoginPage: React.FC = () => {
  const navigate = useNavigate();
  const [officerId, setOfficerId] = useState('KSP-89421');
  const [password, setPassword] = useState('••••••••••••');
  const [selectedRole, setSelectedRole] = useState<UserRole>('Inspector General');
  const [isLoading, setIsLoading] = useState(false);

  const roles: UserRole[] = [
    'Inspector General',
    'Senior Analyst',
    'District Superintendent',
    'Field Investigator',
    'Super Admin'
  ];

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setTimeout(() => {
      setIsLoading(false);
      navigate('/dashboard');
    }, 1200);
  };

  return (
    <div className="relative min-h-screen w-full bg-[#081229] flex items-center justify-center p-4 overflow-hidden selection:bg-blue-600 selection:text-white">
      {/* Animated Cyber Grid Mesh Background */}
      <div className="absolute inset-0 bg-grid-pattern opacity-30 pointer-events-none" />
      <div className="absolute -top-40 -left-40 w-96 h-96 bg-blue-600/20 rounded-full blur-3xl pointer-events-none animate-pulse-slow" />
      <div className="absolute -bottom-40 -right-40 w-96 h-96 bg-cyan-500/20 rounded-full blur-3xl pointer-events-none animate-pulse-slow" />

      {/* Main Glassmorphism Login Card */}
      <motion.div
        initial={{ opacity: 0, scale: 0.9, y: 20 }}
        animate={{ opacity: 1, scale: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="relative z-10 w-full max-w-lg glass-panel rounded-3xl p-8 border border-blue-500/30 shadow-2xl"
      >
        {/* Header Branding */}
        <div className="flex flex-col items-center text-center space-y-3">
          <div className="w-16 h-16 rounded-2xl bg-gradient-to-tr from-blue-700 via-blue-600 to-cyan-400 p-0.5 shadow-neon-blue flex items-center justify-center">
            <div className="w-full h-full bg-[#081229] rounded-[14px] flex items-center justify-center">
              <Shield className="w-9 h-9 text-cyan-400 animate-pulse" />
            </div>
          </div>

          <div>
            <h1 className="text-2xl font-black text-white font-mono tracking-tight glow-text-blue">
              CrimeCop <span className="text-cyan-400">AI</span>
            </h1>
            <p className="text-xs text-slate-400 mt-1 uppercase tracking-widest font-semibold">
              Karnataka State Police Intelligence Mesh
            </p>
          </div>
        </div>

        {/* Security Badge Pill */}
        <div className="my-6 p-2.5 rounded-xl bg-blue-950/60 border border-blue-500/30 flex items-center justify-between text-xs text-slate-300">
          <div className="flex items-center space-x-2">
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span className="font-semibold text-emerald-400">KSP Secure Node Online</span>
          </div>
          <span className="text-[10px] font-mono text-cyan-300 bg-blue-600/30 px-2 py-0.5 rounded border border-cyan-500/30">
            TLS 1.3 ENCRYPTED
          </span>
        </div>

        <form onSubmit={handleLogin} className="space-y-4">
          {/* Role Selection Tabs */}
          <div>
            <label className="block text-[11px] font-semibold text-slate-300 uppercase tracking-wider mb-2">
              Select Officer Role
            </label>
            <div className="grid grid-cols-2 gap-1.5 p-1 bg-slate-900/80 rounded-2xl border border-blue-500/20">
              {roles.map((r) => (
                <button
                  type="button"
                  key={r}
                  onClick={() => setSelectedRole(r)}
                  className={`py-1.5 px-2 rounded-xl text-[11px] font-bold transition-all text-center truncate ${
                    selectedRole === r
                      ? 'bg-blue-600 text-white shadow-glow-sm'
                      : 'text-slate-400 hover:text-white hover:bg-slate-800'
                  }`}
                >
                  {r}
                </button>
              ))}
            </div>
          </div>

          {/* Badge ID Input */}
          <div>
            <label className="block text-[11px] font-semibold text-slate-300 uppercase tracking-wider mb-1">
              Officer Badge ID
            </label>
            <div className="relative">
              <User className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input
                type="text"
                required
                value={officerId}
                onChange={(e) => setOfficerId(e.target.value)}
                placeholder="e.g. KSP-89421"
                className="w-full pl-10 pr-4 py-2.5 bg-slate-900 border border-blue-500/30 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all font-mono"
              />
            </div>
          </div>

          {/* Password Input */}
          <div>
            <label className="block text-[11px] font-semibold text-slate-300 uppercase tracking-wider mb-1">
              Security Clearance Passcode
            </label>
            <div className="relative">
              <Key className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter 12-character security key"
                className="w-full pl-10 pr-4 py-2.5 bg-slate-900 border border-blue-500/30 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all font-mono"
              />
            </div>
          </div>

          {/* Submit Action Button */}
          <button
            type="submit"
            disabled={isLoading}
            className="w-full py-3 px-4 rounded-xl bg-gradient-to-r from-blue-600 via-blue-500 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-bold text-xs uppercase tracking-wider shadow-neon-blue flex items-center justify-center space-x-2 transition-all cursor-pointer group disabled:opacity-50"
          >
            {isLoading ? (
              <span className="flex items-center space-x-2">
                <span className="w-4 h-4 rounded-full border-2 border-white border-t-transparent animate-spin" />
                <span>Authenticating Officer...</span>
              </span>
            ) : (
              <>
                <span>Access Police Command Center</span>
                <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </>
            )}
          </button>
        </form>

        {/* Footnote */}
        <div className="mt-6 pt-4 border-t border-slate-700/60 text-center text-[10px] text-slate-400">
          Official Government Platform. Restricted to Authorized Police Officers.
        </div>
      </motion.div>
    </div>
  );
};
