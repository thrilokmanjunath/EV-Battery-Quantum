"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Scale, Zap, Shield, Thermometer, Box } from "lucide-react";

interface Chemistry {
  id: number;
  name: string;
  family: string;
  nominal_voltage: number;
  specific_capacity: number;
  energy_density: number;
  cycle_life: number;
  safety_rating: number;
  thermal_stability: string;
  efficiency: number;
}

export default function ComparePage() {
  const [chemistries, setChemistries] = useState<Chemistry[]>([]);
  const [selected1, setSelected1] = useState<string>("");
  const [selected2, setSelected2] = useState<string>("");

  useEffect(() => {
    fetch("http://localhost:8001/api/chemistries")
      .then(res => res.json())
      .then(data => {
        setChemistries(data);
        if (data.length >= 2) {
          setSelected1(data[0].id.toString());
          setSelected2(data[1].id.toString());
        }
      });
  }, []);

  const chem1 = chemistries.find(c => c.id.toString() === selected1);
  const chem2 = chemistries.find(c => c.id.toString() === selected2);

  const renderBar = (val1: number, val2: number, max: number, label: string, isHigherBetter = true) => {
    const pct1 = Math.min((val1 / max) * 100, 100);
    const pct2 = Math.min((val2 / max) * 100, 100);
    const c1Better = isHigherBetter ? val1 >= val2 : val1 <= val2;
    const c2Better = isHigherBetter ? val2 >= val1 : val2 <= val1;

    return (
      <div className="mb-6">
        <div className="flex justify-between text-xs font-semibold text-zinc-500 mb-2">
          <span>{label}</span>
          <span>Max: {max}</span>
        </div>
        <div className="relative h-6 bg-zinc-100 rounded-md overflow-hidden mb-1 flex items-center">
          <motion.div initial={{ width: 0 }} animate={{ width: `${pct1}%` }} transition={{ duration: 0.8 }} 
            className={`absolute h-full ${c1Better ? 'bg-blue-500' : 'bg-blue-300'}`} />
          <span className="relative z-10 text-xs font-bold text-white px-2 drop-shadow-md">{val1}</span>
        </div>
        <div className="relative h-6 bg-zinc-100 rounded-md overflow-hidden flex items-center">
          <motion.div initial={{ width: 0 }} animate={{ width: `${pct2}%` }} transition={{ duration: 0.8, delay: 0.1 }} 
            className={`absolute h-full ${c2Better ? 'bg-emerald-500' : 'bg-emerald-300'}`} />
          <span className="relative z-10 text-xs font-bold text-white px-2 drop-shadow-md">{val2}</span>
        </div>
      </div>
    );
  };

  return (
    <main className="min-h-screen p-8 md:p-12 lg:p-24 max-w-6xl mx-auto">
      <header className="mb-12">
        <h1 className="text-4xl font-bold tracking-tight text-zinc-900 mb-4">Battery Comparison Engine</h1>
        <p className="text-zinc-500 text-lg max-w-2xl">
          Side-by-side technical evaluation of electrochemical architectures.
        </p>
      </header>

      {chemistries.length > 0 && chem1 && chem2 ? (
        <div className="bg-white rounded-2xl border border-zinc-200 shadow-sm p-8">
          <div className="grid grid-cols-2 gap-8 mb-12">
            <div>
              <label className="block text-sm font-semibold text-blue-700 mb-2">Chemistry A (Blue)</label>
              <select 
                value={selected1} 
                onChange={e => setSelected1(e.target.value)}
                className="w-full p-3 bg-blue-50 border border-blue-200 rounded-lg text-blue-900 font-medium outline-none focus:ring-2 ring-blue-500"
              >
                {chemistries.map(c => <option key={`a-${c.id}`} value={c.id}>{c.name}</option>)}
              </select>
            </div>
            <div>
              <label className="block text-sm font-semibold text-emerald-700 mb-2">Chemistry B (Green)</label>
              <select 
                value={selected2} 
                onChange={e => setSelected2(e.target.value)}
                className="w-full p-3 bg-emerald-50 border border-emerald-200 rounded-lg text-emerald-900 font-medium outline-none focus:ring-2 ring-emerald-500"
              >
                {chemistries.map(c => <option key={`b-${c.id}`} value={c.id}>{c.name}</option>)}
              </select>
            </div>
          </div>

          <div className="space-y-2">
            {renderBar(chem1.energy_density, chem2.energy_density, 500, "Energy Density (Wh/kg)")}
            {renderBar(chem1.specific_capacity, chem2.specific_capacity, 4000, "Specific Capacity (mAh/g)")}
            {renderBar(chem1.cycle_life, chem2.cycle_life, 5000, "Cycle Life (cycles)")}
            {renderBar(chem1.safety_rating, chem2.safety_rating, 10, "Safety Rating (1-10)")}
            {renderBar(chem1.efficiency, chem2.efficiency, 100, "Round-trip Efficiency (%)")}
            {renderBar(chem1.nominal_voltage, chem2.nominal_voltage, 5, "Nominal Voltage (V)")}
          </div>
        </div>
      ) : (
        <div className="text-zinc-500">Loading comparison engine...</div>
      )}
    </main>
  );
}
