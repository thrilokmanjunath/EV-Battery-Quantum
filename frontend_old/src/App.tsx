import React, { useEffect, useState, useRef } from 'react';

function App() {
  const [logs, setLogs] = useState<string[]>([]);
  const logsEndRef = useRef<HTMLDivElement>(null);
  const [taskId, setTaskId] = useState<string | null>(null);
  const [status, setStatus] = useState<'idle' | 'running' | 'success' | 'error'>('idle');
  const [params, setParams] = useState({ layers: 4, learningRate: 0.01, iterations: 100 });
  const [optimalResult, setOptimalResult] = useState<{ variables: string[], optimal_parameters: number[], cost: number } | null>(null);
  const [showLogs, setShowLogs] = useState(false);

  const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8001';
  const WS_URL = API_URL.replace(/^http/, 'ws');

  const VARIABLES = {
    chemistry: ["NMC", "LFP", "Solid-State", "NCA"],
    cooling: ["Liquid", "Air", "Phase-Change", "Immersion"],
    anode: ["Graphite", "Silicon", "Lithium-Metal"],
    format: ["Cylindrical", "Prismatic", "Pouch"]
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus('running');
    setLogs(['> Initiating quantum battery simulation...']);
    setTaskId(null);
    setOptimalResult(null);
    setShowLogs(true);
    
    const payload = {
      optimization: { variables: VARIABLES },
      qaoa: params
    };

    try {
      const response = await fetch(`${API_URL}/optimize`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ parameters: payload }),
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
      setLogs((prev) => [...prev, '> Quantum cluster connection established.', '> Solving QUBO topology...']);
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
      setLogs((prev) => [...prev, '> Cluster connection lost.']);
    };

    return () => {
      ws.close();
    };
  }, [taskId, WS_URL]);

  useEffect(() => {
    if (status === 'success' && taskId) {
      const fetchResult = async () => {
        try {
          const res = await fetch(`${API_URL}/status/${taskId}`);
          const data = await res.json();
          if (data.status === 'SUCCESS' && data.result?.result) {
            setOptimalResult(data.result.result);
            setShowLogs(false);
          }
        } catch (e) {
          console.error("Failed to fetch final results", e);
        }
      };
      fetchResult();
    }
  }, [status, taskId, API_URL]);

  useEffect(() => {
    logsEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  // Parse result to get selected traits
  const getSelectedTraits = () => {
    if (!optimalResult) return [];
    const traits: {category: string, value: string}[] = [];
    optimalResult.variables.forEach((variable, idx) => {
      if (optimalResult.optimal_parameters[idx] === 1) {
        // e.g. "chemistry_Solid_State"
        Object.keys(VARIABLES).forEach(cat => {
          if (variable.startsWith(cat)) {
            traits.push({
              category: cat.charAt(0).toUpperCase() + cat.slice(1),
              value: variable.replace(`${cat}_`, '').replace('_', '-')
            });
          }
        });
      }
    });
    return traits;
  };

  const selectedTraits = getSelectedTraits();

  return (
    <div className="min-h-screen bg-slate-950 text-slate-200 font-sans p-6 overflow-hidden relative">
      {/* Background gradients */}
      <div className="absolute top-[-10%] left-[-10%] w-96 h-96 bg-indigo-600/30 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-[-10%] right-[-10%] w-[30rem] h-[30rem] bg-emerald-600/20 rounded-full blur-[150px] pointer-events-none"></div>

      <header className="max-w-6xl mx-auto mb-10 backdrop-blur-md bg-slate-900/50 p-6 rounded-2xl border border-slate-800/60 shadow-lg flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-extrabold bg-gradient-to-r from-emerald-400 to-indigo-500 bg-clip-text text-transparent">
            Q-Battery Optimizer
          </h1>
          <p className="text-slate-400 mt-2 text-sm font-medium tracking-wide uppercase">AI-Driven Quantum Chemistry Search</p>
        </div>
        <div className="flex gap-4">
          <div className="flex items-center gap-2 bg-slate-800/80 px-4 py-2 rounded-full border border-slate-700">
            <span className={`w-2 h-2 rounded-full ${status === 'running' ? 'bg-indigo-400 animate-pulse' : status === 'success' ? 'bg-emerald-400' : status === 'error' ? 'bg-red-400' : 'bg-emerald-400'}`}></span>
            <span className={`text-sm font-medium ${status === 'running' ? 'text-indigo-400' : status === 'success' ? 'text-emerald-400' : status === 'error' ? 'text-red-400' : 'text-emerald-400'}`}>
              {status === 'running' ? 'Simulating...' : status === 'success' ? 'Blueprint Ready' : status === 'error' ? 'System Error' : 'System Ready'}
            </span>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-8">
        
        {/* Left Column: Input Form */}
        <div className="md:col-span-1 flex flex-col gap-8">
          <div className="backdrop-blur-lg bg-slate-900/60 border border-slate-800 p-8 rounded-3xl shadow-xl">
            <h2 className="text-xl font-bold text-slate-100 flex items-center gap-3 mb-6">
              <svg className="w-5 h-5 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
              Quantum Settings
            </h2>
            
            <form onSubmit={handleSubmit} className="flex flex-col gap-5">
              <div className="flex flex-col gap-2">
                <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Circuit Layers (Depth)</label>
                <input 
                  type="number" 
                  value={params.layers}
                  onChange={(e) => setParams({...params, layers: parseInt(e.target.value)})}
                  disabled={status === 'running'}
                  className="bg-slate-950/50 border border-slate-700 text-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all disabled:opacity-50"
                />
              </div>
              <div className="flex flex-col gap-2">
                <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Learning Rate</label>
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
                <label className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Max Iterations</label>
                <input 
                  type="number" 
                  value={params.iterations}
                  onChange={(e) => setParams({...params, iterations: parseInt(e.target.value)})}
                  disabled={status === 'running'}
                  className="bg-slate-950/50 border border-slate-700 text-slate-200 rounded-xl px-4 py-3 focus:outline-none focus:border-indigo-500 focus:ring-1 focus:ring-indigo-500 transition-all disabled:opacity-50"
                />
              </div>
              
              <button 
                type="submit" 
                disabled={status === 'running'}
                className="mt-4 w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-bold py-4 px-6 rounded-xl shadow-lg transition-all hover:shadow-indigo-500/20 hover:-translate-y-0.5 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
              >
                {status === 'running' ? 'Simulating...' : 'Generate Blueprint'}
              </button>
            </form>
          </div>

          <div className="backdrop-blur-lg bg-slate-900/60 border border-slate-800 p-6 rounded-3xl shadow-xl">
             <button 
               type="button"
               onClick={() => setShowLogs(!showLogs)}
               className="w-full flex justify-between items-center text-slate-300 font-medium text-sm"
             >
               <span className="flex items-center gap-2">
                 <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M8 9l3 3-3 3m5 0h3M4 12a8 8 0 1116 0 8 8 0 01-16 0z"></path></svg>
                 View Cluster Telemetry
               </span>
               <svg className={`w-4 h-4 transition-transform ${showLogs ? 'rotate-180' : ''}`} fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
             </button>
             
             {showLogs && (
               <div className="mt-4 rounded-xl bg-slate-950 border border-slate-800 p-4 font-mono text-xs text-emerald-400/80 overflow-auto h-48">
                 {logs.map((log, index) => (
                   <p key={index} className="mb-1 opacity-80 break-words">{log.startsWith('>') ? log : `> ${log}`}</p>
                 ))}
                 <div ref={logsEndRef} />
               </div>
             )}
          </div>
        </div>

        {/* Right Column: Blueprint & Topology */}
        <div className="md:col-span-2 flex flex-col gap-8">
          
          {/* Optimal Blueprint Card */}
          <div className="backdrop-blur-lg bg-slate-900/60 border border-slate-800 p-8 rounded-3xl shadow-xl relative overflow-hidden flex flex-col justify-center min-h-[300px]">
            {status === 'success' && selectedTraits.length > 0 ? (
              <>
                <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/10 rounded-full blur-[80px] pointer-events-none"></div>
                <h2 className="text-2xl font-bold text-slate-100 mb-2 flex items-center gap-3">
                  <svg className="w-7 h-7 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z"></path></svg>
                  Optimized Battery Blueprint
                </h2>
                <p className="text-slate-400 mb-8 font-mono text-sm">Targeting maximum energy density & thermal stability.</p>
                
                <div className="grid grid-cols-2 gap-4">
                  {selectedTraits.map((trait, i) => (
                    <div key={i} className="bg-slate-800/50 border border-slate-700/50 rounded-2xl p-4 flex flex-col items-center justify-center text-center hover:bg-slate-800 transition-colors">
                      <span className="text-xs uppercase tracking-widest text-slate-500 font-bold mb-2">{trait.category}</span>
                      <span className="text-lg font-bold text-emerald-300">{trait.value}</span>
                    </div>
                  ))}
                </div>
              </>
            ) : status === 'running' ? (
               <div className="flex flex-col items-center justify-center h-full text-center space-y-6">
                 <div className="relative">
                   <div className="absolute inset-0 rounded-full border-t-2 border-indigo-500 animate-spin w-16 h-16 mx-auto"></div>
                   <svg className="w-16 h-16 text-indigo-400/30" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1" d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5"></path></svg>
                 </div>
                 <p className="text-indigo-300 font-medium text-lg animate-pulse">Computing combinatorial state space...</p>
               </div>
            ) : (
               <div className="flex flex-col items-center justify-center h-full text-slate-500">
                 <svg className="w-16 h-16 mb-4 opacity-50" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
                 <p className="text-lg font-medium">Awaiting simulation parameters.</p>
               </div>
            )}
          </div>

          {/* Loss Landscape */}
          <div className="backdrop-blur-lg bg-slate-900/60 border border-slate-800 p-8 rounded-3xl shadow-xl flex flex-col justify-center flex-1">
             <h3 className="text-lg font-bold text-slate-100 mb-6 flex items-center gap-2">
               <svg className="w-5 h-5 text-purple-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6"></path></svg>
               Convergence Energy Landscape
             </h3>
             <div className="w-full h-40 border border-slate-800/80 rounded-2xl bg-slate-950/50 flex items-center justify-center overflow-hidden relative">
               <div className={`w-full flex items-end justify-center gap-2 h-32 px-10 transition-opacity ${status === 'running' || status === 'success' ? 'opacity-80' : 'opacity-20'}`}>
                 {[95, 80, 65, 50, 45, 30, 25, 20, 15, 12, 8, 5].map((h, i) => (
                   <div key={i} className={`w-full rounded-t-sm transition-all duration-1000 ${status === 'running' ? 'bg-indigo-500 animate-pulse' : 'bg-gradient-to-t from-purple-600 to-indigo-400'}`} style={{ height: status === 'idle' ? '10%' : `${h}%`, transitionDelay: `${i * 100}ms` }}></div>
                 ))}
               </div>
               {status === 'idle' && (
                 <div className="absolute inset-0 flex items-center justify-center backdrop-blur-[1px]">
                   <p className="text-slate-400 text-sm font-medium">No active optimization data</p>
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
