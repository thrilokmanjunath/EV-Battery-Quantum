"use client";

import { motion } from "framer-motion";
import { Zap, ShieldCheck, BatteryCharging } from "lucide-react";

export default function BatteryBlueprintCard() {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8 }}
      className="p-[1px] rounded-2xl bg-gradient-to-br from-quantum-glow/50 via-quantum-accent/20 to-transparent"
    >
      <div className="bg-[#0f172a] rounded-2xl p-6 h-full shadow-[0_0_30px_rgba(56,189,248,0.15)] relative overflow-hidden">
        <div className="absolute -top-10 -right-10 w-32 h-32 bg-quantum-glow/10 rounded-full blur-2xl"></div>
        <h3 className="text-xl font-semibold mb-4 text-white flex items-center gap-2">
          <Zap className="text-quantum-glow" />
          Optimal Chemistry
        </h3>
        
        <div className="space-y-4">
          <div className="flex justify-between items-center border-b border-white/10 pb-2">
            <span className="text-gray-400">Anode Material</span>
            <span className="font-mono text-quantum-glow">Silicon-Dominant (Si)</span>
          </div>
          <div className="flex justify-between items-center border-b border-white/10 pb-2">
            <span className="text-gray-400">Cathode Material</span>
            <span className="font-mono text-quantum-glow">Li-Rich NMC 811</span>
          </div>
          <div className="flex justify-between items-center border-b border-white/10 pb-2">
            <span className="text-gray-400">Solid Electrolyte</span>
            <span className="font-mono text-quantum-glow">LLZO</span>
          </div>
        </div>

        <div className="mt-6 p-4 rounded-xl bg-black/40 border border-white/5">
          <h4 className="text-sm text-gray-400 mb-2 flex items-center gap-2">
            <ShieldCheck size={16} className="text-quantum-accent" />
            Thermal Management
          </h4>
          <p className="text-sm text-gray-300">
            Active multiphase liquid cooling configured for max heat flux of 45 W/cm² with minimal parasitic loss.
          </p>
        </div>
      </div>
    </motion.div>
  );
}
