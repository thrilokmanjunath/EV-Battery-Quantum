"use client";

import dynamic from "next/dynamic";
import { useState } from "react";
import BatteryBlueprintCard from "@/components/blueprint/BatteryBlueprintCard";
import LossLandscape from "@/components/visualizer/LossLandscape";
import ArchitectureExplanation from "@/components/explanation/ArchitectureExplanation";

const SecureTerminalDrawer = dynamic(
  () => import("@/components/telemetry/SecureTerminalDrawer"),
  { ssr: false }
);

interface BlueprintResult {
  anode: string;
  cathode: string;
  electrolyte: string;
}

export default function Home() {
  const [taskId, setTaskId] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [result, setResult] = useState<BlueprintResult | null>(null);

  const handleOptimize = async () => {
    setIsRunning(true);
    setResult(null);
    setTaskId(null);

    try {
      const response = await fetch("http://localhost:8001/optimize", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          parameters: {
            optimization: {
              variables: {
                anode: ["Silicon-Dominant (Si)", "Graphite", "Lithium-Metal"],
                cathode: ["Li-Rich NMC 811", "LFP", "NCA"],
                electrolyte: ["LLZO", "Polymer", "Liquid"]
              }
            }
          }
        })
      });
      const data = await response.json();
      setTaskId(data.task_id);
    } catch (err) {
      console.error("Failed to start optimization", err);
      setIsRunning(false);
    }
  };

  const handleComplete = async () => {
    if (!taskId) return;
    try {
      const response = await fetch(`http://localhost:8001/status/${taskId}`);
      const data = await response.json();
      
      if (data.status === "SUCCESS" && data.result) {
        const optimalVars = data.result.result.optimal_parameters;
        const variables: string[] = data.result.result.variables;
        
        let anode = "Unknown", cathode = "Unknown", electrolyte = "Unknown";
        
        // Match 1s to the variable names
        variables.forEach((v, idx) => {
          if (optimalVars[idx] === 1) {
            if (v.startsWith("anode_")) anode = v.replace("anode_", "").replace(/_/g, "-");
            if (v.startsWith("cathode_")) cathode = v.replace("cathode_", "").replace(/_/g, " ");
            if (v.startsWith("electrolyte_")) electrolyte = v.replace("electrolyte_", "");
          }
        });

        setResult({ anode, cathode, electrolyte });
      }
    } catch (err) {
      console.error("Failed to fetch result", err);
    } finally {
      setIsRunning(false);
    }
  };

  return (
    <main className="min-h-screen p-8 md:p-12 lg:p-24 bg-white text-zinc-900">
      <div className="max-w-6xl mx-auto">
        <header className="mb-12 border-b border-zinc-200 pb-6 flex justify-between items-end">
          <div>
            <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-zinc-900">
              EV Battery Quantum Optimization
            </h1>
            <p className="text-zinc-500 mt-4 text-lg max-w-2xl">
              Real-time synthesis and optimization of next-generation battery chemistries utilizing quantum algorithms.
            </p>
          </div>
          <button 
            onClick={handleOptimize}
            disabled={isRunning}
            className="px-6 py-3 bg-zinc-900 text-white font-medium rounded-lg hover:bg-zinc-800 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {isRunning ? "Optimizing..." : "Run Quantum Optimization"}
          </button>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          <BatteryBlueprintCard result={result} />
          <SecureTerminalDrawer taskId={taskId} onComplete={handleComplete} />
          <LossLandscape running={isRunning} />
        </div>

        <ArchitectureExplanation />
      </div>
    </main>
  );
}
