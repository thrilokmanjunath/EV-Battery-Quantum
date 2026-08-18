"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Battery, Zap, Shield, Thermometer } from "lucide-react";

interface Chemistry {
  id: number;
  name: string;
  family: string;
  cathode: string;
  anode: string;
  electrolyte: string;
  energy_density: number;
  cycle_life: number;
  safety_rating: number;
  thermal_stability: string;
  advantages: string[];
}

export default function ChemistriesPage() {
  const [chemistries, setChemistries] = useState<Chemistry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8001/api/chemistries")
      .then(res => res.json())
      .then(data => {
        setChemistries(data);
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load chemistries", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="min-h-screen p-12 flex items-center justify-center">Loading chemistry data...</div>;
  }

  return (
    <main className="min-h-screen p-8 md:p-12 lg:p-24 max-w-7xl mx-auto">
      <header className="mb-12">
        <h1 className="text-4xl font-bold tracking-tight text-zinc-900 mb-4">Battery Chemistries</h1>
        <p className="text-zinc-500 text-lg max-w-2xl">
          Explore validated electrochemical architectures, from standard Lithium-ion to next-generation Solid-State and Na-ion systems.
        </p>
      </header>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {chemistries.map((chem, idx) => (
          <motion.div 
            key={chem.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="bg-white rounded-2xl border border-zinc-200 p-6 shadow-sm hover:shadow-md transition-shadow"
          >
            <div className="flex items-center gap-3 mb-4">
              <div className="w-10 h-10 rounded-full bg-zinc-100 flex items-center justify-center text-zinc-700">
                <Battery size={20} />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-zinc-900">{chem.name}</h2>
                <span className="text-xs font-medium px-2 py-1 bg-zinc-100 text-zinc-600 rounded-md">
                  {chem.family}
                </span>
              </div>
            </div>

            <div className="space-y-4 mb-6">
              <div className="text-sm">
                <span className="text-zinc-500 block mb-1">Architecture</span>
                <div className="font-mono text-xs text-zinc-700 bg-zinc-50 p-2 rounded border border-zinc-100">
                  <span className="text-blue-600">C:</span> {chem.cathode}<br/>
                  <span className="text-amber-600">A:</span> {chem.anode}<br/>
                  <span className="text-emerald-600">E:</span> {chem.electrolyte}
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="flex items-center gap-1 text-zinc-500 mb-1">
                    <Zap size={14} /> <span className="text-xs">Energy Density</span>
                  </div>
                  <div className="font-semibold text-zinc-900">{chem.energy_density} <span className="text-xs text-zinc-500 font-normal">Wh/kg</span></div>
                </div>
                <div>
                  <div className="flex items-center gap-1 text-zinc-500 mb-1">
                    <Thermometer size={14} /> <span className="text-xs">Thermal</span>
                  </div>
                  <div className="font-semibold text-zinc-900">{chem.thermal_stability}</div>
                </div>
              </div>
            </div>

            <div className="border-t border-zinc-100 pt-4">
              <h4 className="text-xs font-medium text-zinc-500 uppercase tracking-wider mb-2">Advantages</h4>
              <ul className="text-sm text-zinc-700 space-y-1">
                {chem.advantages.slice(0, 3).map((adv, i) => (
                  <li key={i} className="flex items-start gap-2">
                    <span className="text-green-500 mt-0.5">•</span>
                    <span>{adv}</span>
                  </li>
                ))}
              </ul>
            </div>
            
          </motion.div>
        ))}
      </div>
    </main>
  );
}
