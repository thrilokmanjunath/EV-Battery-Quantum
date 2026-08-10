import React, { useEffect, useState, useRef } from 'react';

function App() {
  const [logs, setLogs] = useState<string[]>([]);
  const logsEndRef = useRef<HTMLDivElement>(null);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [status, setStatus] = useState<'idle' | 'running' | 'success' | 'error'>('idle');
  const [params, setParams] = useState({ layers: 4, learningRate: 0.01, iterations: 100 });

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';
  const WS_URL = API_URL.replace(/^http/, 'ws');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('running');
    setLogs(['> Initiating quantum optimization sequence...']);
    setTaskId(null);
    try {
      const response = await fetch(`${API_URL}/optimize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ parameters: params }),
      });
      if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
      const data = await response.json();
      setTaskId(data.task_id);
    } catch (error) {
      setStatus('error');
      const errorMessage = error instanceof Error ? error.message : String(error);
      setLogs((prev) => [...prev, `> Error: ${errorMessage}`]);
    }
  };

  useEffect(() => {
    if (!taskId) return;

    const ws = new WebSocket(`${WS_URL}/ws/logs/${taskId}`);

    ws.onopen = () => {
      setLogs((prev) => [...prev, '> WebSocket connection established.', '> Listening for telemetry...']);
    };

    ws.onmessage = (event) => {
      setLogs((prev) => [...prev, event.data]);
      const logLower = event.data.toLowerCase();
      if (logLower.includes('success') || logLower.includes('optimization complete')) {
        setStatus('success');
      } else if (logLower.includes('error') || logLower.includes('failed')) {
        setStatus('error');
      }
    };

    ws.onerror = () => {
      setStatus('error');
      setLogs((prev) => [...prev, '> WebSocket connection error.']);
    };

    return () => {
      ws.close();
    };
  }, [taskId]);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans p-6 overflow-hidden relative">
      {/* Background gradients */}
      <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-indigo-600/30 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[30rem] h-[30rem] bg-emerald-600/20 rounded-full blur-[150px] pointer-events-none"></div>

      <header className="mb-10 backdrop-blur-md bg-slate-900/50 p-6 rounded-2xl border border-slate-800/60 shadow-lg shadow-indigo-900/10 flex items-center justify-between transition-all hover:border-slate-700/80">
        <div>
          <h1 className="text-4xl font-extrabold bg-gradient-to-r from-emerald-400 to-indigo-500 bg-clip-text text-transparent">
            EV Battery Quantum Dashboard
          </h1>
          <p className="text-slate-400 mt-2 text-sm font-medium tracking-wide uppercase">Production Quantum Engine</p>
        </div>
        <div className="flex gap-4">
          <div className="flex items-center gap-2 bg-slate-800/80 px-4 py-2 rounded-full border border-slate-700">
            <span className={`w-2 h-2 rounded-full ${status === 'running' ? 'bg-indigo-400 animate-pulse' : status === 'success' ? 'bg-emerald-400' : status === 'error' ? 'bg-red-400' : 'bg-emerald-400'}`}></span>
            <span className={`text-sm font-medium ${status === 'running' ? 'text-indigo-400' : status === 'success' ? 'text-emerald-400' : status === 'error' ? 'text-red-400' : 'text-emerald-400'}`}>
              {status === 'running' ? 'Optimizing...' : status === 'success' ? 'Optimization Complete' : status === 'error' ? 'System Error' : 'System Ready'}
            </span>
          </div>
        </div>
      </header>

      <main className="grid grid-cols-1 md:grid-cols-3 gap-8">
        
        {/* Configuration & Status */}
        <div className="md:col-span-2 group relative">
          <div className="absolute inset-0 bg-gradient-to-br from-indigo-500/10 to-transparent rounded-3xl blur-xl transition-opacity opacity-0 group-hover:opacity-100 duration-500"></div>
          <div className="relative h-full backdrop-blur-lg bg-slate-900/60 border border-slate-800 p-8 rounded-3xl shadow-xl transition-all duration-300 hover:-translate-y-1 hover:border-indigo-500/30 flex flex-col">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-slate-100 flex items-center gap-3">
                <svg className="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 10V3L4 14h7v7l9-11h-7z"></path></svg>
                Quantum Parameters
              </h2>
              <span className={`text-xs px-3 py-1 rounded-full border ${status === 'running' ? 'bg-indigo-500/20 text-indigo-300 border-indigo-500/30' : 'bg-slate-800 text-slate-400 border-slate-700'}`}>
                {status === 'running' ? 'Active Session' : 'Configuration Mode'}
              </span>
            </div>
            
            <form onSubmit={handleSubmit} className="flex-1 flex flex-col gap-6">
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-medium text-slate-400 uppercase tracking-wider">Circuit Layers</label>
                  <input 
                    type="number" 
                    value={params.layers}
                    onChange={(e) => setParams({...params, layers: parseInt(e.target.value)})}
                    disabled={status === 'running'}
                    className="bg-slate-950/50 border border-slate-700 text-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all disabled:opacity-50"
                  />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-medium text-slate-400 uppercase tracking-wider">Learning Rate</label>
                  <input 
                    type="number" 
                    step="0.001"
                    value={params.learningRate}
                    onChange={(e) => setParams({...params, learningRate: parseFloat(e.target.value)})}
                    disabled={status === 'running'}
                    className="bg-slate-950/50 border border-slate-700 text-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all disabled:opacity-50"
                  />
                </div>
                <div className="flex flex-col gap-2">
                  <label className="text-sm font-medium text-slate-400 uppercase tracking-wider">Max Iterations</label>
                  <input 
                    type="number" 
                    value={params.iterations}
                    onChange={(e) => setParams({...params, iterations: parseInt(e.target.value)})}
                    disabled={status === 'running'}
                    className="bg-slate-950/50 border border-slate-700 text-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all disabled:opacity-50"
                  />
                </div>
              </div>
              
              <div className="mt-auto pt-6 flex gap-4 border-t border-slate-800/80">
                <button 
                  type="submit" 
                  disabled={status === 'running'}
                  className="flex-1 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold py-3 px-6 rounded-xl shadow-lg shadow-indigo-900/20 transition-all hover:shadow-indigo-500/20 hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                  {status === 'running' ? (
                    <>
                      <svg className="animate-spin h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle><path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path></svg>
                      Processing Pipeline...
                    </>
                  ) : (
                    <>
                      <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"></path><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                      Start Optimization
                    </>
                  )}
                </button>
                {status !== 'idle' && status !== 'running' && (
                  <button 
                    type="button" 
                    onClick={() => { setStatus('idle'); setLogs([]); setTaskId(null); }}
                    className="px-6 py-3 bg-slate-800 hover:bg-slate-700 text-slate-200 font-bold rounded-xl border border-slate-700 transition-all hover:border-slate-600"
                  >
                    Reset
                  </button>
                )}
              </div>
            </form>
          </div>
        </div>

        {/* Live Logs */}
        <div className="md:col-span-1 group relative">
          <div className="absolute inset-0 bg-gradient-to-br from-emerald-500/10 to-transparent rounded-3xl blur-xl transition-opacity opacity-0 group-hover:opacity-100 duration-500"></div>
          <div className="relative h-full backdrop-blur-lg bg-slate-900/60 border border-slate-800 p-8 rounded-3xl shadow-xl transition-all duration-300 hover:-translate-y-1 hover:border-emerald-500/30 flex flex-col">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-2xl font-bold text-slate-100 flex items-center gap-3">
                <svg className="w-6 h-6 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 6h16M4 12h16M4 18h7"></path></svg>
                Telemetry Logs
              </h2>
              <span className="flex h-3 w-3">
                {status === 'running' && (
                  <>
                    <span className="animate-ping absolute inline-flex h-3 w-3 rounded-full bg-emerald-400 opacity-75"></span>
                    <span className="relative inline-flex rounded-full h-3 w-3 bg-emerald-500"></span>
                  </>
                )}
                {status !== 'running' && (
                  <span className="relative inline-flex rounded-full h-3 w-3 bg-slate-600"></span>
                )}
              </span>
            </div>
            <div className="flex-1 rounded-2xl bg-slate-950/80 border border-slate-800 p-4 font-mono text-sm text-emerald-400/70 overflow-auto relative h-64 max-h-64">
              <div className="absolute inset-0 bg-gradient-to-b from-transparent to-slate-950/90 pointer-events-none sticky top-0 h-full w-full z-10" style={{background: 'linear-gradient(to bottom, transparent 80%, rgba(2,6,23,0.9) 100%)'}}></div>
              <div className="relative z-0">
                {logs.map((log, index) => {
                  const isError = log.toLowerCase().includes('error') || log.toLowerCase().includes('failed');
                  return (
                    <p key={index} className={`mb-2 opacity-80 break-words ${isError ? 'text-red-400' : ''}`}>
                      {log.startsWith('>') ? log : `> ${log}`}
                    </p>
                  );
                })}
                {logs.length === 0 && (
                  <p className="mb-2 text-slate-500 italic">&gt; System idle. Awaiting configuration...</p>
                )}
                <div ref={logsEndRef} />
              </div>
            </div>
          </div>
        </div>

        {/* Simulation History */}
        <div className="md:col-span-3 group relative">
           <div className="absolute inset-0 bg-gradient-to-b from-purple-500/10 to-transparent rounded-3xl blur-xl transition-opacity opacity-0 group-hover:opacity-100 duration-500"></div>
           <div className="relative backdrop-blur-lg bg-slate-900/60 border border-slate-800 p-8 rounded-3xl shadow-xl transition-all duration-300 hover:-translate-y-1 hover:border-purple-500/30">
            <h2 className="text-2xl font-bold text-slate-100 mb-6 flex items-center gap-3">
              <svg className="w-6 h-6 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path></svg>
              Loss Landscape Topology
            </h2>
            <div className="w-full h-64 border-2 border-dashed border-slate-800/80 rounded-2xl bg-slate-950/30 group-hover:bg-slate-950/50 transition-colors flex items-center justify-center overflow-hidden relative">
               <div className={`w-full flex items-end justify-center gap-2 h-48 px-10 transition-opacity ${status === 'running' || status === 'success' ? 'opacity-80' : 'opacity-20'}`}>
                 {[90, 85, 70, 60, 55, 40, 35, 20, 18, 12, 10, 5].map((h, i) => (
                   <div key={i} className={`w-full rounded-t-sm transition-all duration-1000 ${status === 'running' ? 'bg-indigo-500 animate-pulse' : 'bg-gradient-to-t from-purple-600 to-indigo-400'}`} style={{ height: status === 'idle' ? '10%' : `${h}%`, transitionDelay: `${i * 100}ms` }}></div>
                 ))}
               </div>
               {status === 'idle' && (
                 <div className="absolute inset-0 flex items-center justify-center backdrop-blur-[2px]">
                   <p className="text-slate-400 text-lg font-medium bg-slate-900/80 px-6 py-2 rounded-full border border-slate-700/50 shadow-xl">Run optimization to view convergence data</p>
                 </div>
               )}
            </div>
          </div>
        </div>

      </main>
    </div>
  );
}

export default App;
