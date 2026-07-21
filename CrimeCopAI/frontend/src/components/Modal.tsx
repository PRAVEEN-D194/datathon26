import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { X } from 'lucide-react';

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  subtitle?: string;
  children: React.ReactNode;
  maxWidth?: string;
}

export const Modal: React.FC<ModalProps> = ({
  isOpen,
  onClose,
  title,
  subtitle,
  children,
  maxWidth = 'max-w-2xl'
}) => {
  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="fixed inset-0 bg-slate-950/80 backdrop-blur-md"
        />

        {/* Modal Window */}
        <motion.div
          initial={{ opacity: 0, scale: 0.95, y: 20 }}
          animate={{ opacity: 1, scale: 1, y: 0 }}
          exit={{ opacity: 0, scale: 0.95, y: 20 }}
          className={`relative w-full ${maxWidth} glass-panel rounded-3xl p-6 shadow-2xl border border-blue-500/30 z-10`}
        >
          {/* Header */}
          <div className="flex items-center justify-between border-b border-blue-500/20 pb-4 mb-4">
            <div>
              <h3 className="text-lg font-bold text-white tracking-wide">{title}</h3>
              {subtitle && <p className="text-xs text-slate-400 mt-0.5">{subtitle}</p>}
            </div>
            <button
              onClick={onClose}
              className="p-1.5 rounded-xl bg-slate-800/80 hover:bg-red-500/20 hover:text-red-400 text-slate-400 transition-colors"
            >
              <X size={18} />
            </button>
          </div>

          {/* Content */}
          <div className="max-h-[75vh] overflow-y-auto pr-1">
            {children}
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
};
