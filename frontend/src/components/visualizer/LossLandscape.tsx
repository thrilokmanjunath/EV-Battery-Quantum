"use client";

import { motion } from "framer-motion";
import { Activity } from "lucide-react";

export default function LossLandscape() {
  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.8, delay: 0.4 }}
      className="rounded-2xl border border-zinc-200 bg-white shadow-sm md:col-span-2 p-6"
    >
      <div className="h-full relative overflow-hidden">
        <div className="flex items-center justify-between mb-8">
          <h3 className="text-xl font-semibold text-zinc-900 flex items-center gap-2">
            <Activity className="text-zinc-500" />
            Convergence Landscape
          </h3>
          <div className="flex gap-4 text-xs">
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-zinc-800"></div>
              <span className="text-zinc-500">VQE Energy</span>
            </div>
          </div>
        </div>

        <div className="h-48 w-full relative flex items-end justify-between px-2 border-b border-zinc-100">
          {[...Array(20)].map((_, i) => {
            const baseHeight = 100 - (i * 4) + Math.random() * 20;
            const finalHeight = Math.max(10, baseHeight);
            
            return (
              <motion.div
                key={i}
                initial={{ height: 0 }}
                animate={{ 
                  height: [
                    `${finalHeight + Math.random() * 30}%`, 
                    `${finalHeight}%`,
                    `${finalHeight + Math.random() * 10}%`
                  ] 
                }}
                transition={{
                  duration: 3,
                  repeat: Infinity,
                  repeatType: "reverse",
                  delay: i * 0.1
                }}
                className="w-[3%] bg-zinc-800 rounded-t-sm opacity-80"
              />
            );
          })}
        </div>
        
        <div className="absolute bottom-0 left-0 w-full h-1/4 bg-gradient-to-t from-white to-transparent pointer-events-none"></div>
      </div>
    </motion.div>
  );
}
