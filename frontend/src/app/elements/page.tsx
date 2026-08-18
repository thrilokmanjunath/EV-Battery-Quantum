"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Database, AlertTriangle } from "lucide-react";

interface ElementMaterial {
  id: number;
  name: string;
  formula: string;
  molar_mass: number;
  atomic_number: number;
  oxidation_states: string;
  abundance: string;
  supply_risk: number;
  toxicity: string;
}

export default function ElementsPage() {
  const [elements, setElements] = useState<ElementMaterial[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8001/api/elements")
      .then(res => res.json())
      .then(data => {
        setElements(data.sort((a: any, b: any) => a.atomic_number - b.atomic_number));
        setLoading(false);
      })
      .catch(err => {
        console.error("Failed to load elements", err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="min-h-screen p-12 flex items-center justify-center">Loading element data...</div>;
  }

  return (
    <main className="min-h-screen p-8 md:p-12 lg:p-24 max-w-7xl mx-auto">
      <header className="mb-12">
        <h1 className="text-4xl font-bold tracking-tight text-zinc-900 mb-4">Battery Elements</h1>
        <p className="text-zinc-500 text-lg max-w-2xl">
          Database of critical elements used in electrochemical energy storage, including supply risk and atomic properties.
        </p>
      </header>

      <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-5 gap-4">
        {elements.map((el, idx) => (
          <motion.div 
            key={el.id}
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: idx * 0.05 }}
            className={`bg-white rounded-xl border p-4 shadow-sm flex flex-col relative overflow-hidden ${
              el.supply_risk >= 8 ? 'border-red-200' : 
              el.supply_risk >= 5 ? 'border-amber-200' : 'border-zinc-200'
            }`}
          >
            {el.supply_risk >= 8 && (
              <div className="absolute top-0 right-0 p-2">
                <AlertTriangle size={14} className="text-red-500" />
              </div>
            )}
            
            <div className="text-xs font-semibold text-zinc-400 mb-1">{el.atomic_number}</div>
            <div className="text-3xl font-bold text-zinc-900 mb-1">{el.formula}</div>
            <div className="text-sm font-medium text-zinc-700 mb-4">{el.name}</div>
            
            <div className="mt-auto space-y-2 text-xs">
              <div className="flex justify-between border-b border-zinc-100 pb-1">
                <span className="text-zinc-500">Mass</span>
                <span className="font-mono text-zinc-800">{el.molar_mass.toFixed(2)}</span>
              </div>
              <div className="flex justify-between border-b border-zinc-100 pb-1">
                <span className="text-zinc-500">Oxidation</span>
                <span className="font-mono text-zinc-800">{el.oxidation_states}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-zinc-500">Risk</span>
                <span className={`font-mono ${el.supply_risk >= 8 ? 'text-red-600 font-bold' : 'text-zinc-800'}`}>
                  {el.supply_risk.toFixed(1)}/10
                </span>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </main>
  );
}
