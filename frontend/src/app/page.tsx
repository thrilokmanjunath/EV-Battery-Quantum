import dynamic from "next/dynamic";
import BatteryBlueprintCard from "@/components/blueprint/BatteryBlueprintCard";
import LossLandscape from "@/components/visualizer/LossLandscape";
import ArchitectureExplanation from "@/components/explanation/ArchitectureExplanation";

const SecureTerminalDrawer = dynamic(
  () => import("@/components/telemetry/SecureTerminalDrawer"),
  { ssr: false }
);
export default function Home() {
  return (
    <main className="min-h-screen p-8 md:p-12 lg:p-24 bg-white text-zinc-900">
      <div className="max-w-6xl mx-auto">
        <header className="mb-12 border-b border-zinc-200 pb-6">
          <h1 className="text-4xl md:text-5xl font-bold tracking-tight text-zinc-900">
            EV Battery Quantum Optimization
          </h1>
          <p className="text-zinc-500 mt-4 text-lg max-w-2xl">
            Real-time synthesis and optimization of next-generation battery chemistries utilizing quantum algorithms.
          </p>
        </header>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-12">
          <BatteryBlueprintCard />
          <SecureTerminalDrawer />
          <LossLandscape />
        </div>

        <ArchitectureExplanation />
      </div>
    </main>
  );
}
