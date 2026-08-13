"use client";

import { useEffect, useRef } from "react";
import { Terminal } from "xterm";
import "xterm/css/xterm.css";
import { Terminal as TerminalIcon } from "lucide-react";
import { motion } from "framer-motion";

export default function SecureTerminalDrawer() {
  const terminalRef = useRef<HTMLDivElement>(null);
  const isInitialized = useRef(false);

  useEffect(() => {
    if (!terminalRef.current || isInitialized.current) return;
    isInitialized.current = true;
    terminalRef.current.innerHTML = '';

    const term = new Terminal({
      theme: {
        background: '#0B0F19',
        foreground: '#38bdf8',
        cursor: '#818cf8',
      },
      fontFamily: '"Fira Code", monospace',
      fontSize: 14,
      rows: 12,
    });

    let eventSource: EventSource | null = null;

    const timer = setTimeout(() => {
      if (!terminalRef.current) return;
      
      term.open(terminalRef.current);
      term.writeln('Initializing Secure Quantum Telemetry...');

      eventSource = new EventSource('http://localhost:8001/api/quantum/stream/demo-task');

      eventSource.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          term.writeln(`\r\n[${new Date().toISOString()}] ${data.message || data}`);
        } catch {
          term.writeln(`\r\n[${new Date().toISOString()}] ${event.data}`);
        }
      };

      eventSource.onerror = () => {
        term.writeln('\r\n\x1b[31m[ERROR] Connection lost to quantum stream.\x1b[0m');
        if (eventSource) eventSource.close();
      };
    }, 50);

    return () => {
      clearTimeout(timer);
      term.dispose();
      if (eventSource) eventSource.close();
      isInitialized.current = false;
    };
  }, []);

  return (
    <motion.div 
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.8, delay: 0.2 }}
      className="p-[1px] rounded-2xl bg-gradient-to-br from-quantum-accent/50 to-transparent"
    >
      <div className="bg-[#0f172a] rounded-2xl overflow-hidden h-full">
        <div className="bg-black/50 px-4 py-3 flex items-center gap-2 border-b border-white/10">
          <TerminalIcon size={16} className="text-quantum-accent" />
          <span className="text-sm font-medium text-gray-300">Live Telemetry (xterm.js)</span>
        </div>
        <div className="p-4 bg-[#0B0F19]">
          <div ref={terminalRef} className="w-full h-full" />
        </div>
      </div>
    </motion.div>
  );
}
