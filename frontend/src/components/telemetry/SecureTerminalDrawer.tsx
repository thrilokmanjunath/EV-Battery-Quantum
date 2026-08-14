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
        background: '#ffffff',
        foreground: '#171717',
        cursor: '#3b82f6',
        selectionBackground: '#e2e8f0',
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

      // Fetch the demo token to satisfy the backend's strict JWT requirement
      fetch('http://localhost:8001/api/demo/token')
        .then(res => res.json())
        .then(data => {
          const token = data.access_token;
          eventSource = new EventSource(`http://localhost:8001/api/quantum/stream/demo-task?token=${token}`);

          eventSource.onmessage = (event) => {
            try {
              const parsed = JSON.parse(event.data);
              term.writeln(`\r\n[${new Date().toISOString()}] ${parsed.message || parsed}`);
            } catch {
              term.writeln(`\r\n[${new Date().toISOString()}] ${event.data}`);
            }
          };

          eventSource.onerror = () => {
            term.writeln('\r\n\x1b[31m[ERROR] Connection lost to quantum stream.\x1b[0m');
            if (eventSource) eventSource.close();
          };
        })
        .catch(err => {
          term.writeln('\r\n\x1b[31m[ERROR] Failed to fetch auth token.\x1b[0m');
        });

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
      className="rounded-2xl border border-zinc-200 bg-white shadow-sm overflow-hidden flex flex-col"
    >
      <div className="bg-zinc-50 px-4 py-3 flex items-center gap-2 border-b border-zinc-200">
        <TerminalIcon size={16} className="text-zinc-500" />
        <span className="text-sm font-medium text-zinc-700">Live Telemetry</span>
      </div>
      <div className="p-4 flex-1">
        <div ref={terminalRef} className="w-full h-full" />
      </div>
    </motion.div>
  );
}
