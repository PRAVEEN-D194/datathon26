import React from 'react';
import { useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import { Bot, Sparkles } from 'lucide-react';

export const FloatingAIButton: React.FC = () => {
  const navigate = useNavigate();

  return (
    <motion.button
      whileHover={{ scale: 1.08 }}
      whileTap={{ scale: 0.95 }}
      onClick={() => navigate('/ai-assistant')}
      className="fixed bottom-6 right-6 z-40 p-4 rounded-2xl bg-gradient-to-tr from-blue-700 via-blue-600 to-cyan-400 text-white shadow-neon-blue border border-cyan-300/40 flex items-center space-x-3 group cursor-pointer"
      title="Open KSP Intellibot AI Assistant"
    >
      <div className="relative">
        <Bot className="w-6 h-6 animate-pulse" />
        <Sparkles className="w-3.5 h-3.5 text-yellow-300 absolute -top-2 -right-2 animate-bounce" />
      </div>
      <div className="hidden sm:flex flex-col text-left">
        <span className="text-xs font-black tracking-wider uppercase font-mono">KSP Intellibot</span>
        <span className="text-[10px] text-cyan-200 font-semibold">AI Copilot Ready</span>
      </div>
    </motion.button>
  );
};
