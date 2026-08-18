"use client";

import { useState } from "react";
import { Calculator as CalcIcon, Battery, Zap } from "lucide-react";
import { motion } from "framer-motion";

export default function CalculatorPage() {
  // Faraday Calculator State
  const [electrons, setElectrons] = useState<number>(1);
  const [molarMass, setMolarMass] = useState<number>(6.94); // Default to Li
  const [capacityResult, setCapacityResult] = useState<number | null>(null);

  // Energy Calculator State
  const [voltage, setVoltage] = useState<number>(3.7);
  const [capacity, setCapacity] = useState<number>(5.0);
  const [mass, setMass] = useState<number>(0.05);
  const [energyResult, setEnergyResult] = useState<{energy_wh?: number, specific_energy_wh_kg?: number} | null>(null);

  const calculateCapacity = async () => {
    try {
      const res = await fetch("http://localhost:8001/api/calculations/theoretical-capacity", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ electrons_transferred: electrons, molar_mass: molarMass })
      });
      const data = await res.json();
      if (data.theoretical_specific_capacity_mah_g) {
        setCapacityResult(data.theoretical_specific_capacity_mah_g);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const calculateEnergy = async () => {
    try {
      const res = await fetch("http://localhost:8001/api/calculations/energy", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ voltage, capacity, mass: mass > 0 ? mass : undefined })
      });
      const data = await res.json();
      setEnergyResult(data);
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <main className="min-h-screen p-8 md:p-12 lg:p-24 max-w-5xl mx-auto">
      <header className="mb-12">
        <h1 className="text-4xl font-bold tracking-tight text-zinc-900 mb-4">Electrochemical Calculator</h1>
        <p className="text-zinc-500 text-lg max-w-2xl">
          Scientifically validated physics-based bounds calculator using Faraday&apos;s laws and Nernst potentials.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Theoretical Capacity */}
        <motion.div 
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white p-8 rounded-2xl border border-zinc-200 shadow-sm"
        >
          <div className="flex items-center gap-3 mb-6 border-b border-zinc-100 pb-4">
            <CalcIcon className="text-blue-500" />
            <h2 className="text-xl font-semibold">Theoretical Specific Capacity</h2>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-zinc-700 mb-1">Electrons Transferred (n)</label>
              <input type="number" value={electrons} onChange={e => setElectrons(Number(e.target.value))} min={1} className="w-full p-2 border border-zinc-300 rounded-md bg-zinc-50 font-mono text-sm" />
            </div>
            <div>
              <label className="block text-sm font-medium text-zinc-700 mb-1">Molar Mass (g/mol)</label>
              <input type="number" value={molarMass} onChange={e => setMolarMass(Number(e.target.value))} min={0.1} step={0.01} className="w-full p-2 border border-zinc-300 rounded-md bg-zinc-50 font-mono text-sm" />
            </div>
            
            <button onClick={calculateCapacity} className="w-full py-2 bg-zinc-900 text-white rounded-md hover:bg-zinc-800 transition-colors font-medium mt-4">
              Calculate Q = nF / 3.6M
            </button>
            
            {capacityResult !== null && (
              <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-100 flex justify-between items-center">
                <span className="text-blue-800 font-medium text-sm">Theoretical Capacity</span>
                <span className="text-xl font-bold text-blue-900 font-mono">{capacityResult} <span className="text-xs font-medium text-blue-700">mAh/g</span></span>
              </div>
            )}
          </div>
        </motion.div>

        {/* Energy Density */}
        <motion.div 
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          className="bg-white p-8 rounded-2xl border border-zinc-200 shadow-sm"
        >
          <div className="flex items-center gap-3 mb-6 border-b border-zinc-100 pb-4">
            <Zap className="text-amber-500" />
            <h2 className="text-xl font-semibold">Energy Density</h2>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-zinc-700 mb-1">Nominal Voltage (V)</label>
              <input type="number" value={voltage} onChange={e => setVoltage(Number(e.target.value))} min={0.1} step={0.1} className="w-full p-2 border border-zinc-300 rounded-md bg-zinc-50 font-mono text-sm" />
            </div>
            <div>
              <label className="block text-sm font-medium text-zinc-700 mb-1">Capacity (Ah)</label>
              <input type="number" value={capacity} onChange={e => setCapacity(Number(e.target.value))} min={0.1} step={0.1} className="w-full p-2 border border-zinc-300 rounded-md bg-zinc-50 font-mono text-sm" />
            </div>
            <div>
              <label className="block text-sm font-medium text-zinc-700 mb-1">Mass (kg) <span className="text-zinc-400 font-normal">- Optional</span></label>
              <input type="number" value={mass} onChange={e => setMass(Number(e.target.value))} min={0} step={0.01} className="w-full p-2 border border-zinc-300 rounded-md bg-zinc-50 font-mono text-sm" />
            </div>
            
            <button onClick={calculateEnergy} className="w-full py-2 bg-zinc-900 text-white rounded-md hover:bg-zinc-800 transition-colors font-medium mt-4">
              Calculate Energy Metrics
            </button>
            
            {energyResult !== null && (
              <div className="mt-6 space-y-2">
                <div className="p-4 bg-amber-50 rounded-lg border border-amber-100 flex justify-between items-center">
                  <span className="text-amber-800 font-medium text-sm">Total Energy</span>
                  <span className="text-xl font-bold text-amber-900 font-mono">{energyResult.energy_wh} <span className="text-xs font-medium text-amber-700">Wh</span></span>
                </div>
                {energyResult.specific_energy_wh_kg && (
                  <div className="p-4 bg-emerald-50 rounded-lg border border-emerald-100 flex justify-between items-center">
                    <span className="text-emerald-800 font-medium text-sm">Specific Energy</span>
                    <span className="text-xl font-bold text-emerald-900 font-mono">{energyResult.specific_energy_wh_kg} <span className="text-xs font-medium text-emerald-700">Wh/kg</span></span>
                  </div>
                )}
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </main>
  );
}
