import React from 'react';
import { NavLink, useLocation } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  LayoutDashboard,
  Bot,
  BarChart3,
  MapPin,
  GitFork,
  FileText,
  UserCheck,
  Shield,
  ChevronLeft,
  ChevronRight,
  Radio,
  Lock
} from 'lucide-react';

interface SidebarProps {
  collapsed: boolean;
  setCollapsed: (val: boolean) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ collapsed, setCollapsed }) => {
  const location = useLocation();

  const navItems = [
    { name: 'Dashboard', path: '/dashboard', icon: LayoutDashboard, badge: null },
    { name: 'AI Assistant', path: '/ai-assistant', icon: Bot, badge: 'AI Copilot' },
    { name: 'Analytics', path: '/analytics', icon: BarChart3, badge: null },
    { name: 'Crime Map', path: '/crime-map', icon: MapPin, badge: 'LIVE' },
    { name: 'Criminal Network', path: '/criminal-network', icon: GitFork, badge: 'Graph' },
    { name: 'Reports', path: '/reports', icon: FileText, badge: '4 New' },
    { name: 'Profile & Settings', path: '/settings', icon: UserCheck, badge: null },
  ];

  return (
    <motion.aside
      animate={{ width: collapsed ? 80 : 280 }}
      transition={{ duration: 0.3, ease: 'easeInOut' }}
      className="relative z-30 h-screen sticky top-0 bg-[#081229]/95 backdrop-blur-xl border-r border-blue-500/20 flex flex-col justify-between shadow-2xl selection:bg-blue-600 select-none"
    >
      {/* Top Section: KSP Logo & Header */}
      <div>
        <div className="p-4 flex items-center justify-between border-b border-blue-500/15">
          <div className="flex items-center space-x-3 overflow-hidden">
            <div className="relative flex-shrink-0 w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-700 via-blue-600 to-cyan-400 p-0.5 shadow-neon-blue flex items-center justify-center">
              <div className="w-full h-full bg-[#081229] rounded-[10px] flex items-center justify-center">
                <Shield className="w-6 h-6 text-blue-400 animate-pulse" />
              </div>
              <div className="absolute -top-1 -right-1 w-3 h-3 bg-emerald-500 rounded-full border-2 border-[#081229]" />
            </div>

            {!collapsed && (
              <motion.div
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -10 }}
                className="flex flex-col"
              >
                <div className="flex items-center space-x-1.5">
                  <span className="font-extrabold text-base tracking-wider text-white font-mono">CrimeCop</span>
                  <span className="px-1.5 py-0.5 text-[10px] font-semibold bg-blue-600/30 text-cyan-400 rounded border border-cyan-500/30">AI</span>
                </div>
                <span className="text-[10px] font-medium tracking-wider text-slate-400 uppercase">
                  Karnataka State Police
                </span>
              </motion.div>
            )}
          </div>

          <button
            onClick={() => setCollapsed(!collapsed)}
            className="p-1.5 rounded-lg bg-slate-800/80 hover:bg-blue-600/30 text-slate-300 hover:text-white border border-slate-700/50 transition-colors"
            title={collapsed ? "Expand Sidebar" : "Collapse Sidebar"}
          >
            {collapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
          </button>
        </div>

        {/* System Live Status Pill */}
        {!collapsed && (
          <div className="mx-3 my-3 p-2.5 rounded-xl bg-blue-950/40 border border-blue-500/20 flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <span className="relative flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
              </span>
              <span className="text-xs font-medium text-slate-300">KSP Grid Active</span>
            </div>
            <Radio className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
          </div>
        )}

        {/* Navigation Items */}
        <nav className="p-2 space-y-1.5 mt-2">
          {navItems.map((item) => {
            const isActive = location.pathname === item.path;
            const Icon = item.icon;

            return (
              <NavLink
                key={item.path}
                to={item.path}
                className={({ isActive }) => `
                  relative group flex items-center ${collapsed ? 'justify-center' : 'justify-between'} px-3 py-3 rounded-xl text-sm font-medium transition-all duration-200
                  ${isActive
                    ? 'bg-gradient-to-r from-blue-600/30 to-blue-900/20 text-white border border-blue-500/40 shadow-glow-sm'
                    : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/40 border border-transparent'
                  }
                `}
              >
                <div className="flex items-center space-x-3">
                  <Icon className={`w-5 h-5 transition-transform group-hover:scale-110 ${isActive ? 'text-blue-400' : 'text-slate-400 group-hover:text-cyan-400'}`} />
                  {!collapsed && <span className="truncate">{item.name}</span>}
                </div>

                {!collapsed && item.badge && (
                  <span className={`px-2 py-0.5 text-[10px] font-bold rounded-full uppercase tracking-wider ${
                    item.badge === 'LIVE' ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 animate-pulse' :
                    item.badge === 'AI Copilot' ? 'bg-cyan-500/20 text-cyan-300 border border-cyan-500/30' :
                    'bg-blue-600/30 text-blue-300 border border-blue-500/30'
                  }`}>
                    {item.badge}
                  </span>
                )}

                {/* Active Bar Indicator */}
                {isActive && (
                  <motion.div
                    layoutId="activeNavIndicator"
                    className="absolute left-0 top-1.5 bottom-1.5 w-1 bg-gradient-to-b from-blue-400 to-cyan-400 rounded-r"
                    transition={{ type: "spring", stiffness: 300, damping: 30 }}
                  />
                )}
              </NavLink>
            );
          })}
        </nav>
      </div>

      {/* Bottom Security Classification Card */}
      <div className="p-3 border-t border-blue-500/15">
        {!collapsed ? (
          <div className="p-3 rounded-xl bg-[#10203D] border border-blue-500/20 flex flex-col space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-1.5 text-xs font-semibold text-amber-400">
                <Lock className="w-3.5 h-3.5" />
                <span>TOP SECRET</span>
              </div>
              <span className="text-[10px] text-slate-400 font-mono">CLEARANCE L5</span>
            </div>
            <p className="text-[11px] text-slate-400 leading-tight">
              KSP Restricted Data Node. Unauthorized access is punishable under IT Act.
            </p>
          </div>
        ) : (
          <div className="flex justify-center p-2 text-amber-400" title="Security Clearance Level 5">
            <Lock className="w-5 h-5" />
          </div>
        )}
      </div>
    </motion.aside>
  );
};
