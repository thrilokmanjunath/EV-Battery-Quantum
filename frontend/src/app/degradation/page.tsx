"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { TrendingDown, Activity, BatteryCharging } from "lucide-react";

export default function DegradationPage() {
  const [cycles, setCycles] = useState(1000);
  const [temp, setTemp] = useState(25);
  const [dod, setDod] = useState(80);
  const [soh, setSoh] = useState<number | null>(null);

  const simulateDegradation = () => {
    // Simplified empirical SOH heuristic:
    // SOH = 100 - (cycles * A) - (Temp_penalty) - (DOD_penalty)
    let degradation = 0;
    
    // Cycle degradation
    degradation += cycles * 0.01; 
    
    // Temperature penalty (ideal is ~25C, accelerates greatly above 45C)
    if (temp > 25) {
      degradation += (temp - 25) * 0.5 * (cycles / 1000);
    } else if (temp < 10) {
      degradation += (10 - temp) * 0.3 * (cycles / 1000);
    }
    
    // DOD penalty (deep cycling hurts)
    if (dod > 50) {
      degradation += (dod - 50) * 0.1 * (cycles / 1000);
    }

    const finalSoh = Math.max(0, 100 - degradation);
    setSoh(finalSoh);
  };

  return (
    <main className="min-h-screen p-8 md:p-12 lg:p-24 max-w-5xl mx-auto">
      <header className="mb-12">
        <h1 className="text-4xl font-bold tracking-tight text-zinc-900 mb-4">Degradation Prediction (SOH)</h1>
        <p className="text-zinc-500 text-lg max-w-2xl">
          Empirical heuristic modeling for State of Health (SOH) capacity fade based on cycling, temperature, and depth of discharge.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white p-8 rounded-2xl border border-zinc-200 shadow-sm"
        >
          <div className="flex items-center gap-3 mb-6 border-b border-zinc-100 pb-4">
            <Activity className="text-red-500" />
            <h2 className="text-xl font-semibold">Stress Factors</h2>
          </div>
          
          <div className="space-y-6">
            <div>
              <div className="flex justify-between mb-1">
                <label className="text-sm font-medium text-zinc-700">Number of Cycles</label>
                <span className="text-sm font-mono text-zinc-500">{cycles}</span>
              </div>
              <input type="range" min="0" max="5000" step="100" value={cycles} onChange={e => setCycles(Number(e.target.value))} className="w-full accent-zinc-900" />
            </div>
            
            <div>
              <div className="flex justify-between mb-1">
                <label className="text-sm font-medium text-zinc-700">Operating Temperature (°C)</label>
                <span className="text-sm font-mono text-zinc-500">{temp}°C</span>
              </div>
              <input type="range" min="-20" max="80" step="1" value={temp} onChange={e => setTemp(Number(e.target.value))} className="w-full accent-zinc-900" />
            </div>

            <div>
              <div className="flex justify-between mb-1">
                <label className="text-sm font-medium text-zinc-700">Depth of Discharge (%)</label>
                <span className="text-sm font-mono text-zinc-500">{dod}%</span>
              </div>
              <input type="range" min="10" max="100" step="5" value={dod} onChange={e => setDod(Number(e.target.value))} className="w-full accent-zinc-900" />
            </div>
            
            <button onClick={simulateDegradation} className="w-full py-2 bg-zinc-900 text-white rounded-md hover:bg-zinc-800 transition-colors font-medium mt-4 flex justify-center items-center gap-2">
              <TrendingDown size={18} /> Run SOH Simulation
            </button>
          </div>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-zinc-900 p-8 rounded-2xl border border-zinc-800 shadow-xl text-white flex flex-col justify-center items-center relative overflow-hidden"
        >
          <BatteryCharging className="absolute -bottom-10 -right-10 w-64 h-64 text-zinc-800 opacity-30" />
          
          <h3 className="text-zinc-400 font-medium tracking-wide uppercase text-sm mb-4">Estimated State of Health</h3>
          
          {soh !== null ? (
            <div className="text-center relative z-10">
              <div className={`text-7xl font-black mb-2 ${soh < 80 ? 'text-red-400' : 'text-emerald-400'}`}>
                {soh.toFixed(1)}%
              </div>
              <p className="text-zinc-400">
                {soh < 80 ? "End of Life (EOL) reached. Unsafe for EV usage." : "Battery is within operational parameters."}
              </p>
            </div>
          ) : (
            <div className="text-center relative z-10 text-zinc-600">
              <div className="text-7xl font-black mb-2">--.-%</div>
              <p>Run simulation to predict degradation</p>
            </div>
          )}
        </motion.div>
      </div>
    </main>
  );
}
