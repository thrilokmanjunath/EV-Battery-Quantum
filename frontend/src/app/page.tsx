import dynamic from "next/dynamic";
import BatteryBlueprintCard from "@/components/blueprint/BatteryBlueprintCard";
import LossLandscape from "@/components/visualizer/LossLandscape";

const SecureTerminalDrawer = dynamic(
  () => import("@/components/telemetry/SecureTerminalDrawer"),
  { ssr: false }
);
export default function Home() {
  return (
    <main className="min-h-screen p-8 md:p-12 lg:p-24 relative overflow-hidden">
      {/* Background glowing effects */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-quantum-glow/10 blur-[100px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-quantum-accent/10 blur-[100px] pointer-events-none" />

      <div className="max-w-6xl mx-auto relative z-10">
        <header className="mb-12 border-b border-white/10 pb-6">
          <h1 className="text-4xl md:text-5xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-white via-blue-200 to-quantum-glow">
            EV Battery Quantum Optimization
          </h1>
          <p className="text-gray-400 mt-4 text-lg max-w-2xl">
            Real-time synthesis and optimization of next-generation battery chemistries utilizing quantum algorithms.
          </p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <BatteryBlueprintCard />
          <SecureTerminalDrawer />
          <LossLandscape />
        </div>
      </div>
    </main>
  );
}
