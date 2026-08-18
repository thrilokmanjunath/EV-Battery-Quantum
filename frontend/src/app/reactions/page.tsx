"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { FlaskConical, ArrowRight, Activity } from "lucide-react";

interface Reaction {
  id: number;
  chemistry_id: number;
  reaction_type: string;
  equation: string;
  electrons_transferred: number;
  description: string;
}

interface Chemistry {
  id: number;
  name: string;
  family: string;
}

export default function ReactionsPage() {
  const [reactions, setReactions] = useState<(Reaction & { chemistry?: Chemistry })[]>([]);
  const [chemistries, setChemistries] = useState<Chemistry[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      fetch("http://localhost:8001/api/chemistries").then(res => res.json())
    ]).then(([chemData]) => {
      setChemistries(chemData);
      
      const allReactions: any[] = [];
      const fetchPromises = chemData.map((c: any) => 
        fetch(`http://localhost:8001/api/chemistries/${c.id}`)
          .then(r => r.json())
          .then(data => {
            data.reactions.forEach((rx: any) => {
              allReactions.push({ ...rx, chemistry: c });
            });
          })
      );

      Promise.all(fetchPromises).then(() => {
        setReactions(allReactions);
        setLoading(false);
      });
    });
  }, []);

  if (loading) return <div className="min-h-screen p-12 flex items-center justify-center">Loading reaction mechanisms...</div>;

  return (
    <main className="min-h-screen p-8 md:p-12 lg:p-24 max-w-5xl mx-auto">
      <header className="mb-12">
        <h1 className="text-4xl font-bold tracking-tight text-zinc-900 mb-4">Chemical Reaction Viewer</h1>
        <p className="text-zinc-500 text-lg max-w-2xl">
          Scientifically accurate stoichiometric equations representing intercalation and redox mechanisms.
        </p>
      </header>

      <div className="space-y-6">
        {reactions.map((rx, idx) => (
          <motion.div 
            key={rx.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: idx * 0.1 }}
            className="bg-white rounded-xl border border-zinc-200 p-6 shadow-sm flex flex-col md:flex-row gap-6 md:items-center"
          >
            <div className="flex-1">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-xs font-bold px-2 py-1 bg-zinc-100 text-zinc-600 rounded">
                  {rx.chemistry?.name}
                </span>
                <span className={`text-xs font-bold px-2 py-1 rounded ${rx.reaction_type.includes('anode') ? 'bg-amber-100 text-amber-700' : 'bg-blue-100 text-blue-700'}`}>
                  {rx.reaction_type.replace('discharge_', '').toUpperCase()}
                </span>
              </div>
              <p className="text-zinc-600 text-sm mt-3">{rx.description}</p>
            </div>

            <div className="flex-1 bg-zinc-900 rounded-lg p-5 flex items-center justify-center relative overflow-hidden">
              <FlaskConical className="absolute top-[-10px] right-[-10px] text-zinc-800 w-24 h-24 opacity-50" />
              <div className="relative z-10 text-center">
                <div className="font-mono text-lg text-emerald-400 font-bold tracking-wider">
                  {rx.equation.split('->').map((part, i, arr) => (
                    <span key={i}>
                      {part}
                      {i < arr.length - 1 && <span className="text-zinc-500 mx-2">→</span>}
                    </span>
                  ))}
                </div>
                <div className="mt-3 flex items-center justify-center gap-1 text-xs font-mono text-zinc-400">
                  <Activity size={12} /> {rx.electrons_transferred}e⁻ transferred
                </div>
              </div>
            </div>
          </motion.div>
        ))}
      </div>
    </main>
  );
}
