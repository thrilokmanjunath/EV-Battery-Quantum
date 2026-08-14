"use client";

import { motion } from "framer-motion";
import { Server, Cpu, Database, Activity } from "lucide-react";

export default function ArchitectureExplanation() {
  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.8, delay: 0.6 }}
      className="mt-8 rounded-2xl border border-zinc-200 bg-white shadow-sm p-8"
    >
      <h2 className="text-2xl font-semibold text-zinc-900 mb-6">How It Works</h2>
      <p className="text-zinc-600 mb-8 max-w-3xl">
        This platform leverages a microservices architecture to execute complex quantum machine learning 
        algorithms for EV battery material discovery in real-time.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        
        <div className="flex flex-col items-center text-center p-4">
          <div className="w-12 h-12 rounded-full bg-zinc-100 flex items-center justify-center mb-4">
            <Server className="text-zinc-700" />
          </div>
          <h4 className="font-medium text-zinc-900 mb-2">1. Request Initiation</h4>
          <p className="text-sm text-zinc-500">
            The Next.js frontend sends optimization parameters to the FastAPI backend.
          </p>
        </div>

        <div className="flex flex-col items-center text-center p-4">
          <div className="w-12 h-12 rounded-full bg-zinc-100 flex items-center justify-center mb-4">
            <Cpu className="text-zinc-700" />
          </div>
          <h4 className="font-medium text-zinc-900 mb-2">2. Quantum Simulation</h4>
          <p className="text-sm text-zinc-500">
            Celery workers pick up the task and execute Warm-Started QAOA against the QUBO formulations.
          </p>
        </div>

        <div className="flex flex-col items-center text-center p-4">
          <div className="w-12 h-12 rounded-full bg-zinc-100 flex items-center justify-center mb-4">
            <Database className="text-zinc-700" />
          </div>
          <h4 className="font-medium text-zinc-900 mb-2">3. State Management</h4>
          <p className="text-sm text-zinc-500">
            Progress and loss values are updated continuously via Redis Pub/Sub channels.
          </p>
        </div>

        <div className="flex flex-col items-center text-center p-4">
          <div className="w-12 h-12 rounded-full bg-zinc-100 flex items-center justify-center mb-4">
            <Activity className="text-zinc-700" />
          </div>
          <h4 className="font-medium text-zinc-900 mb-2">4. Telemetry Stream</h4>
          <p className="text-sm text-zinc-500">
            Server-Sent Events (SSE) securely push the sanitized quantum state metrics back to the UI in real-time.
          </p>
        </div>

      </div>
    </motion.div>
  );
}
