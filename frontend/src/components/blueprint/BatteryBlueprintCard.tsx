"use client";

import { motion } from "framer-motion";
import { Zap, ShieldCheck, BatteryCharging } from "lucide-react";

interface BlueprintResult {
  anode: string;
  cathode: string;
  electrolyte: string;
}

interface BatteryBlueprintCardProps {
  result?: BlueprintResult | null;
}

export default function BatteryBlueprintCard({ result }: BatteryBlueprintCardProps) {
  const anode = result?.anode || "Pending...";
  const cathode = result?.cathode || "Pending...";
  const electrolyte = result?.electrolyte || "Pending...";

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      className="rounded-2xl border border-zinc-200 bg-white shadow-sm p-6"
    >
      <div className="h-full relative overflow-hidden">
        <h3 className="text-xl font-semibold mb-4 text-zinc-900 flex items-center gap-2">
          <Zap className="text-zinc-500" />
          Optimal Chemistry
        </h3>
        
        <div className="space-y-4">
          <div className="flex justify-between items-center border-b border-zinc-100 pb-2">
            <span className="text-zinc-500">Anode Material</span>
            <span className="font-mono text-zinc-900">{anode}</span>
          </div>
          <div className="flex justify-between items-center border-b border-zinc-100 pb-2">
            <span className="text-zinc-500">Cathode Material</span>
            <span className="font-mono text-zinc-900">{cathode}</span>
          </div>
          <div className="flex justify-between items-center border-b border-zinc-100 pb-2">
            <span className="text-zinc-500">Solid Electrolyte</span>
            <span className="font-mono text-zinc-900">{electrolyte}</span>
          </div>
        </div>

        <div className="mt-6 p-4 rounded-xl bg-zinc-50 border border-zinc-100">
          <h4 className="text-sm font-medium text-zinc-700 mb-2 flex items-center gap-2">
            <ShieldCheck size={16} className="text-zinc-400" />
            Thermal Management
          </h4>
          <p className="text-sm text-zinc-500">
            Active multiphase liquid cooling configured for max heat flux of 45 W/cm² with minimal parasitic loss.
          </p>
        </div>
      </div>
    </motion.div>
  );
}
