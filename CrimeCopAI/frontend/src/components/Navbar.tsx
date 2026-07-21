import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Search,
  Bell,
  Clock,
  Shield,
  Radio,
  ChevronDown,
  LogOut,
  User,
  Settings,
  CheckCircle2,
  AlertTriangle
} from 'lucide-react';
import { mockUserProfile, mockRecentAlerts } from '../data/mockData';
import { useNavigate } from 'react-router-dom';

interface NavbarProps {
  onOpenNotifications?: () => void;
}

export const Navbar: React.FC<NavbarProps> = () => {
  const navigate = useNavigate();
  const [currentTime, setCurrentTime] = useState<string>('');
  const [currentDate, setCurrentDate] = useState<string>('');
  const [showNotifications, setShowNotifications] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setCurrentTime(now.toLocaleTimeString('en-IN', { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: true }));
      setCurrentDate(now.toLocaleDateString('en-IN', { weekday: 'short', day: '2-digit', month: 'short', year: 'numeric' }));
    };
    updateTime();
    const timer = setInterval(updateTime, 1000);
    return () => clearInterval(timer);
  }, []);

  return (
    <header className="sticky top-0 z-20 w-full bg-[#081229]/90 backdrop-blur-md border-b border-blue-500/20 px-6 py-3 flex items-center justify-between shadow-lg">
      {/* Left Section: Global Search */}
      <div className="flex items-center space-x-4 flex-1 max-w-xl">
        <div className="relative w-full">
          <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search FIR #, Suspect Alias, District, Crime MO or License Plate... (Ctrl + K)"
            className="w-full pl-10 pr-12 py-2 bg-slate-900/80 border border-blue-500/25 rounded-xl text-xs text-white placeholder-slate-400 focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
          />
          <span className="absolute right-3 top-1/2 -translate-y-1/2 text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400 border border-slate-700">
            ⌘K
          </span>
        </div>
      </div>

      {/* Center Section: Live Alert Ticker */}
      <div className="hidden lg:flex items-center space-x-3 px-4 py-1.5 rounded-full bg-blue-950/40 border border-blue-500/30 max-w-md overflow-hidden">
        <div className="flex items-center space-x-1.5 flex-shrink-0">
          <Radio className="w-4 h-4 text-emerald-400 animate-pulse" />
          <span className="text-[11px] font-bold text-emerald-400 uppercase tracking-wider">LIVE FEED</span>
        </div>
        <div className="h-3.5 w-px bg-slate-700" />
        <div className="truncate text-xs text-slate-300 font-medium">
          <span className="text-amber-400 font-semibold">FIR KA-2026-BLR-00981:</span> Crypto Laundering Hub Intercepted in Koramangala
        </div>
      </div>

      {/* Right Section: Time, Notifications, User Menu */}
      <div className="flex items-center space-x-5">
        {/* Real-time Clock */}
        <div className="hidden sm:flex flex-col items-end border-r border-slate-700/60 pr-4">
          <div className="flex items-center space-x-1.5 text-xs font-mono font-bold text-cyan-300">
            <Clock className="w-3.5 h-3.5 text-cyan-400" />
            <span>{currentTime}</span>
          </div>
          <span className="text-[10px] text-slate-400 tracking-tight">{currentDate}</span>
        </div>

        {/* Notification Bell */}
        <div className="relative">
          <button
            onClick={() => setShowNotifications(!showNotifications)}
            className="relative p-2 rounded-xl bg-slate-900/80 border border-blue-500/25 hover:border-blue-500 text-slate-300 hover:text-white transition-all"
          >
            <Bell className="w-4 h-4" />
            <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-red-500 text-[9px] font-bold text-white shadow-neon-red">
              4
            </span>
          </button>

          {/* Notification Popover Drawer */}
          <AnimatePresence>
            {showNotifications && (
              <motion.div
                initial={{ opacity: 0, y: 10, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 10, scale: 0.95 }}
                className="absolute right-0 mt-3 w-80 sm:w-96 rounded-2xl glass-panel p-4 shadow-2xl z-50 border border-blue-500/30"
              >
                <div className="flex items-center justify-between border-b border-slate-700/60 pb-3">
                  <div className="flex items-center space-x-2">
                    <AlertTriangle className="w-4 h-4 text-amber-400" />
                    <h4 className="text-xs font-bold text-white uppercase tracking-wider">KSP Real-Time Alerts</h4>
                  </div>
                  <span className="text-[10px] font-semibold bg-blue-600/30 text-cyan-300 px-2 py-0.5 rounded-full">
                    4 Unread
                  </span>
                </div>

                <div className="mt-3 space-y-2.5 max-h-72 overflow-y-auto pr-1">
                  {mockRecentAlerts.map((alert) => (
                    <div
                      key={alert.id}
                      className="p-2.5 rounded-xl bg-slate-900/60 border border-blue-500/15 hover:border-blue-500/40 transition-colors cursor-pointer"
                    >
                      <div className="flex items-center justify-between">
                        <span className={`text-[10px] font-bold px-1.5 py-0.5 rounded ${
                          alert.severity === 'Critical' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 'bg-amber-500/20 text-amber-400'
                        }`}>
                          {alert.severity}
                        </span>
                        <span className="text-[10px] text-slate-400 font-mono">{alert.timestamp}</span>
                      </div>
                      <h5 className="text-xs font-semibold text-white mt-1.5">{alert.title}</h5>
                      <p className="text-[11px] text-slate-400 mt-1 line-clamp-2">{alert.summary}</p>
                    </div>
                  ))}
                </div>

                <div className="mt-3 pt-2 border-t border-slate-700/60 text-center">
                  <button
                    onClick={() => { setShowNotifications(false); navigate('/dashboard'); }}
                    className="text-xs font-semibold text-blue-400 hover:text-cyan-300 transition-colors"
                  >
                    View All Active Feeds & System Logs →
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>

        {/* User Profile Badge */}
        <div className="relative">
          <button
            onClick={() => setShowUserMenu(!showUserMenu)}
            className="flex items-center space-x-3 p-1.5 pr-3 rounded-xl bg-slate-900/80 border border-blue-500/25 hover:border-blue-500/50 transition-all"
          >
            <div className="w-8 h-8 rounded-lg bg-gradient-to-tr from-blue-600 to-cyan-500 flex items-center justify-center font-bold text-white text-xs shadow-glow-sm">
              IG
            </div>
            <div className="hidden md:flex flex-col text-left">
              <span className="text-xs font-bold text-white tracking-tight leading-none">{mockUserProfile.name}</span>
              <span className="text-[10px] text-cyan-400 font-mono mt-0.5">{mockUserProfile.badgeNumber}</span>
            </div>
            <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
          </button>

          {/* User Dropdown */}
          <AnimatePresence>
            {showUserMenu && (
              <motion.div
                initial={{ opacity: 0, y: 10, scale: 0.95 }}
                animate={{ opacity: 1, y: 0, scale: 1 }}
                exit={{ opacity: 0, y: 10, scale: 0.95 }}
                className="absolute right-0 mt-3 w-56 rounded-2xl glass-panel p-2 shadow-2xl z-50 border border-blue-500/30"
              >
                <div className="p-2 border-b border-slate-700/60">
                  <p className="text-xs font-bold text-white">{mockUserProfile.name}</p>
                  <p className="text-[10px] text-slate-400">{mockUserProfile.email}</p>
                  <div className="mt-1 flex items-center space-x-1 text-[10px] text-emerald-400 font-semibold">
                    <CheckCircle2 className="w-3 h-3" />
                    <span>Clearance: {mockUserProfile.clearanceLevel}</span>
                  </div>
                </div>

                <div className="py-1 space-y-0.5">
                  <button
                    onClick={() => { setShowUserMenu(false); navigate('/settings'); }}
                    className="w-full flex items-center space-x-2.5 px-3 py-2 text-xs text-slate-300 hover:text-white hover:bg-slate-800/60 rounded-xl transition-colors"
                  >
                    <User className="w-3.5 h-3.5 text-blue-400" />
                    <span>Officer Profile</span>
                  </button>

                  <button
                    onClick={() => { setShowUserMenu(false); navigate('/settings'); }}
                    className="w-full flex items-center space-x-2.5 px-3 py-2 text-xs text-slate-300 hover:text-white hover:bg-slate-800/60 rounded-xl transition-colors"
                  >
                    <Settings className="w-3.5 h-3.5 text-cyan-400" />
                    <span>Account Settings</span>
                  </button>
                </div>

                <div className="pt-1 border-t border-slate-700/60">
                  <button
                    onClick={() => { setShowUserMenu(false); navigate('/login'); }}
                    className="w-full flex items-center space-x-2.5 px-3 py-2 text-xs text-red-400 hover:bg-red-500/10 rounded-xl transition-colors font-medium"
                  >
                    <LogOut className="w-3.5 h-3.5" />
                    <span>Sign Out Command Node</span>
                  </button>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </header>
  );
};
