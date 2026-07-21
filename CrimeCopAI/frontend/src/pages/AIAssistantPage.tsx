import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import {
  Bot,
  User,
  Send,
  Mic,
  Paperclip,
  Copy,
  RotateCcw,
  Sparkles,
  Check,
  Plus,
  MessageSquare,
  Shield,
  MapPin,
  ExternalLink,
  ChevronRight
} from 'lucide-react';
import { PageHeader } from '../components/PageHeader';
import { mockChatThreads, mockInitialMessages } from '../data/mockData';
import { ChatMessage, ChatThread } from '../types';

export const AIAssistantPage: React.FC = () => {
  const [threads, setThreads] = useState<ChatThread[]>(mockChatThreads);
  const [activeThreadId, setActiveThreadId] = useState<string>('thread-1');
  const [messages, setMessages] = useState<ChatMessage[]>(mockInitialMessages);
  const [inputText, setInputText] = useState<string>('');
  const [isTyping, setIsTyping] = useState<boolean>(false);
  const [copiedMsgId, setCopiedMsgId] = useState<string | null>(null);
  const [isRecordingVoice, setIsRecordingVoice] = useState<boolean>(false);

  const suggestedPrompts = [
    'Summarize repeat offenders in Bengaluru Urban over the last 30 days.',
    'Analyze modus operandi for vehicle theft in Mysuru district.',
    'Generate crime pattern forecast report for Q3 Cyber Fraud.',
    'Map high-value financial transactions linked to Koramangala IT hub.'
  ];

  const handleSendMessage = (textToSend?: string) => {
    const query = textToSend || inputText;
    if (!query.trim()) return;

    const userMsg: ChatMessage = {
      id: `msg-${Date.now()}`,
      sender: 'user',
      text: query,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };

    setMessages((prev) => [...prev, userMsg]);
    if (!textToSend) setInputText('');
    setIsTyping(true);

    // Simulate AI response synthesis
    setTimeout(() => {
      const aiMsg: ChatMessage = {
        id: `msg-${Date.now() + 1}`,
        sender: 'ai',
        text: `### KSP Intelligence Automated Synthesis

Regarding your request: **"${query}"**

#### Analysis Results:
- **Primary Data Source:** 112 FIR Records + Bank Transaction Logs (KSP Database Mesh)
- **High Risk Flag:** 3 active criminal nodes identified in selected scope
- **Recommended Officer Action:** Issue section 91 notice to primary wallet intermediary and deploy patrol geofence in affected district.`,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        structuredData: {
          summaryMetrics: [
            { label: 'FIR Matches', value: '18 Cases', color: '#2563EB' },
            { label: 'Risk Rating', value: 'HIGH', color: '#F59E0B' },
            { label: 'Confidence Index', value: '96.2%', color: '#22C55E' }
          ],
          evidenceTable: [
            { key: 'Target Sector', detail: 'Urban Financial Corridor' },
            { key: 'Associated MO', detail: 'Telegram P2P Wallet Swap' }
          ],
          locationPreview: {
            district: 'Bengaluru Urban',
            coordinates: [12.9716, 77.5946],
            riskLevel: 'Elevated Risk'
          }
        }
      };

      setMessages((prev) => [...prev, aiMsg]);
      setIsTyping(false);
    }, 1500);
  };

  const handleCopyText = (id: string, text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedMsgId(id);
    setTimeout(() => setCopiedMsgId(null), 2000);
  };

  return (
    <div className="space-y-4 pb-8 h-[calc(100vh-100px)] flex flex-col">
      <PageHeader
        title="KSP Intellibot — Conversational Copilot"
        subtitle="Natural language queries over Karnataka State Police crime database & FIR records."
        badge="NEURAL ENGINE V4.2"
      />

      <div className="flex-1 grid grid-cols-1 lg:grid-cols-4 gap-4 overflow-hidden min-h-0">
        {/* Left Sidebar: Case Threads / Chat History */}
        <div className="glass-card rounded-2xl p-4 border border-blue-500/20 flex flex-col justify-between hidden lg:flex">
          <div>
            <div className="flex items-center justify-between border-b border-blue-500/15 pb-3 mb-3">
              <span className="text-xs font-extrabold text-white uppercase tracking-wider">Case Threads</span>
              <button
                onClick={() => {
                  const newT: ChatThread = {
                    id: `thread-${Date.now()}`,
                    title: `New Intelligence Session #${threads.length + 1}`,
                    lastUpdated: 'Just now',
                    previewText: 'Ready for officer query...',
                    category: 'General'
                  };
                  setThreads([newT, ...threads]);
                  setActiveThreadId(newT.id);
                  setMessages([]);
                }}
                className="p-1 rounded-lg bg-blue-600/30 hover:bg-blue-600 text-cyan-300 hover:text-white border border-cyan-500/30 transition-colors"
                title="New Case Thread"
              >
                <Plus size={16} />
              </button>
            </div>

            <div className="space-y-2 max-h-[60vh] overflow-y-auto pr-1">
              {threads.map((thread) => {
                const isActive = thread.id === activeThreadId;
                return (
                  <div
                    key={thread.id}
                    onClick={() => setActiveThreadId(thread.id)}
                    className={`p-3 rounded-xl cursor-pointer transition-all border ${
                      isActive
                        ? 'bg-blue-600/25 border-blue-500/50 text-white shadow-glow-sm'
                        : 'bg-slate-900/60 border-blue-500/15 text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-[10px] font-bold text-cyan-400 uppercase tracking-wider">{thread.category}</span>
                      <span className="text-[9px] text-slate-500 font-mono">{thread.lastUpdated}</span>
                    </div>
                    <h4 className="text-xs font-semibold mt-1 truncate">{thread.title}</h4>
                    <p className="text-[11px] text-slate-400 mt-1 truncate">{thread.previewText}</p>
                  </div>
                );
              })}
            </div>
          </div>

          <div className="p-3 rounded-xl bg-blue-950/40 border border-blue-500/20 text-[11px] text-slate-400 flex items-center space-x-2">
            <Shield className="w-4 h-4 text-cyan-400 flex-shrink-0" />
            <span>All queries logged in KSP Audit Trail.</span>
          </div>
        </div>

        {/* Right Main Chat Window */}
        <div className="lg:col-span-3 glass-card rounded-2xl border border-blue-500/20 flex flex-col justify-between overflow-hidden shadow-2xl">
          {/* Chat Header */}
          <div className="px-5 py-3.5 bg-slate-900/90 border-b border-blue-500/20 flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-400 p-0.5 shadow-glow-sm flex items-center justify-center">
                <Bot className="w-5 h-5 text-white" />
              </div>
              <div>
                <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center space-x-2">
                  <span>KSP Intellibot Copilot</span>
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
                </h3>
                <span className="text-[10px] text-cyan-400 font-mono">Connected to KSP Central Database</span>
              </div>
            </div>

            <div className="flex items-center space-x-2">
              <span className="text-[10px] font-bold bg-blue-600/30 text-cyan-300 px-2.5 py-1 rounded-full border border-cyan-500/30">
                GPT-4o Crime Fine-Tuned
              </span>
            </div>
          </div>

          {/* Messages Container */}
          <div className="flex-1 p-5 overflow-y-auto space-y-4">
            {/* Suggested Prompts if short history */}
            {messages.length <= 2 && (
              <div className="mb-4">
                <p className="text-xs font-semibold text-slate-400 uppercase tracking-wider mb-2 flex items-center space-x-1.5">
                  <Sparkles className="w-3.5 h-3.5 text-cyan-400" />
                  <span>Suggested Police Intelligence Prompts</span>
                </p>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                  {suggestedPrompts.map((prompt, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleSendMessage(prompt)}
                      className="p-3 rounded-xl bg-slate-900/80 border border-blue-500/20 hover:border-blue-500/60 text-left text-xs text-slate-300 hover:text-white transition-all group cursor-pointer flex items-center justify-between"
                    >
                      <span className="line-clamp-2">{prompt}</span>
                      <ChevronRight className="w-4 h-4 text-slate-500 group-hover:text-cyan-300 flex-shrink-0 ml-2" />
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Chat Message Stream */}
            {messages.map((msg) => (
              <motion.div
                key={msg.id}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                className={`flex space-x-3 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {msg.sender === 'ai' && (
                  <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-400 flex items-center justify-center text-white flex-shrink-0 shadow-glow-sm">
                    <Bot size={18} />
                  </div>
                )}

                <div className={`max-w-2xl rounded-2xl p-4 text-xs leading-relaxed ${
                  msg.sender === 'user'
                    ? 'bg-blue-600 text-white rounded-tr-none shadow-neon-blue font-medium'
                    : 'bg-slate-900/90 text-slate-200 border border-blue-500/30 rounded-tl-none shadow-xl'
                }`}>
                  <div className="prose prose-invert max-w-none text-xs">
                    <ReactMarkdown>{msg.text}</ReactMarkdown>
                  </div>

                  {/* Rich AI Structured Data Card (Metrics + Evidence Table + Map Preview) */}
                  {msg.structuredData && (
                    <div className="mt-3 pt-3 border-t border-slate-700/60 space-y-3">
                      {/* Summary Metrics */}
                      {msg.structuredData.summaryMetrics && (
                        <div className="grid grid-cols-3 gap-2">
                          {msg.structuredData.summaryMetrics.map((sm, idx) => (
                            <div key={idx} className="p-2 rounded-xl bg-slate-800/80 border border-blue-500/20 text-center">
                              <span className="text-[10px] text-slate-400 block">{sm.label}</span>
                              <span className="text-xs font-black font-mono mt-0.5 block" style={{ color: sm.color || '#38BDF8' }}>
                                {sm.value}
                              </span>
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Evidence Table */}
                      {msg.structuredData.evidenceTable && (
                        <div className="p-2.5 rounded-xl bg-slate-800/60 border border-blue-500/20 space-y-1">
                          {msg.structuredData.evidenceTable.map((et, idx) => (
                            <div key={idx} className="flex justify-between text-[11px]">
                              <span className="text-slate-400 font-semibold">{et.key}:</span>
                              <span className="text-cyan-300 font-mono">{et.detail}</span>
                            </div>
                          ))}
                        </div>
                      )}

                      {/* Location Preview Card */}
                      {msg.structuredData.locationPreview && (
                        <div className="p-2.5 rounded-xl bg-blue-950/40 border border-blue-500/30 flex items-center justify-between">
                          <div className="flex items-center space-x-2">
                            <MapPin className="w-4 h-4 text-cyan-400" />
                            <div>
                              <span className="text-xs font-bold text-white block">{msg.structuredData.locationPreview.district}</span>
                              <span className="text-[10px] text-slate-400 font-mono">
                                [{msg.structuredData.locationPreview.coordinates.join(', ')}]
                              </span>
                            </div>
                          </div>
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-red-500/20 text-red-400 border border-red-500/30">
                            {msg.structuredData.locationPreview.riskLevel}
                          </span>
                        </div>
                      )}
                    </div>
                  )}

                  {/* Actions Bar for AI Message */}
                  {msg.sender === 'ai' && (
                    <div className="mt-3 pt-2 border-t border-slate-800 flex items-center justify-between text-[10px] text-slate-400">
                      <span>{msg.timestamp} • Verified by KSP AI Node</span>
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => handleCopyText(msg.id, msg.text)}
                          className="flex items-center space-x-1 hover:text-cyan-300 transition-colors"
                        >
                          {copiedMsgId === msg.id ? <Check size={12} className="text-emerald-400" /> : <Copy size={12} />}
                          <span>{copiedMsgId === msg.id ? 'Copied' : 'Copy'}</span>
                        </button>
                        <button
                          onClick={() => handleSendMessage(messages[messages.length - 2]?.text)}
                          className="flex items-center space-x-1 hover:text-cyan-300 transition-colors"
                        >
                          <RotateCcw size={12} />
                          <span>Regenerate</span>
                        </button>
                      </div>
                    </div>
                  )}
                </div>

                {msg.sender === 'user' && (
                  <div className="w-8 h-8 rounded-xl bg-slate-800 border border-blue-500/30 flex items-center justify-center text-cyan-300 flex-shrink-0">
                    <User size={18} />
                  </div>
                )}
              </motion.div>
            ))}

            {/* Typing Indicator */}
            {isTyping && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex items-center space-x-3">
                <div className="w-8 h-8 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-400 flex items-center justify-center text-white">
                  <Bot size={18} />
                </div>
                <div className="px-4 py-3 rounded-2xl bg-slate-900/90 border border-blue-500/30 flex items-center space-x-1.5">
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce" />
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce [animation-delay:0.2s]" />
                  <span className="w-2 h-2 rounded-full bg-cyan-400 animate-bounce [animation-delay:0.4s]" />
                  <span className="text-xs text-slate-400 font-mono ml-2">Synthesizing Crime Database...</span>
                </div>
              </motion.div>
            )}
          </div>

          {/* Bottom Chat Input Bar */}
          <div className="p-3 bg-slate-900/90 border-t border-blue-500/20">
            <div className="flex items-center space-x-2 bg-slate-950 border border-blue-500/30 rounded-2xl p-2 focus-within:border-blue-500 focus-within:ring-1 focus-within:ring-blue-500 transition-all">
              <button
                type="button"
                onClick={() => alert("Upload FIR PDF / Image attachment interface activated.")}
                className="p-2 rounded-xl text-slate-400 hover:text-cyan-300 hover:bg-slate-800 transition-colors"
                title="Attach FIR Document / Photo"
              >
                <Paperclip size={18} />
              </button>

              <button
                type="button"
                onClick={() => setIsRecordingVoice(!isRecordingVoice)}
                className={`p-2 rounded-xl transition-colors ${
                  isRecordingVoice ? 'bg-red-500 text-white animate-pulse' : 'text-slate-400 hover:text-cyan-300 hover:bg-slate-800'
                }`}
                title="Voice Input Command"
              >
                <Mic size={18} />
              </button>

              <input
                type="text"
                value={inputText}
                onChange={(e) => setInputText(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSendMessage()}
                placeholder="Ask Intellibot about FIRs, suspect profiles, modus operandi or district stats..."
                className="flex-1 bg-transparent px-2 text-xs text-white placeholder-slate-500 focus:outline-none"
              />

              <button
                onClick={() => handleSendMessage()}
                disabled={!inputText.trim()}
                className="p-2.5 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-500 text-white hover:from-blue-500 hover:to-cyan-400 disabled:opacity-40 transition-all cursor-pointer shadow-glow-sm"
              >
                <Send size={16} />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
