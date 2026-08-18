import Link from "next/link";
import { Beaker, Database, Zap, Calculator, Activity } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="sticky top-0 z-50 w-full border-b border-zinc-200 bg-white/80 backdrop-blur-md">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-2">
          <Zap className="h-6 w-6 text-zinc-900" />
          <span className="text-xl font-bold text-zinc-900">QuantumBattery</span>
        </div>
        
        <div className="hidden md:flex items-center gap-8">
          <Link href="/" className="text-sm font-medium text-zinc-600 hover:text-zinc-900 transition-colors flex items-center gap-2">
            <Zap className="h-4 w-4" /> Optimization
          </Link>
          <Link href="/chemistries" className="text-sm font-medium text-zinc-600 hover:text-zinc-900 transition-colors flex items-center gap-2">
            <Beaker className="h-4 w-4" /> Chemistries
          </Link>
          <Link href="/compare" className="text-sm font-medium text-zinc-600 hover:text-zinc-900 transition-colors flex items-center gap-2">
            <Zap className="h-4 w-4" /> Compare
          </Link>
          <Link href="/reactions" className="text-sm font-medium text-zinc-600 hover:text-zinc-900 transition-colors flex items-center gap-2">
            <Database className="h-4 w-4" /> Reactions
          </Link>
          <Link href="/degradation" className="text-sm font-medium text-zinc-600 hover:text-zinc-900 transition-colors flex items-center gap-2">
            <Activity className="h-4 w-4" /> Degradation
          </Link>
          <Link href="/elements" className="text-sm font-medium text-zinc-600 hover:text-zinc-900 transition-colors flex items-center gap-2">
            <Database className="h-4 w-4" /> Elements
          </Link>
          <Link href="/calculator" className="text-sm font-medium text-zinc-600 hover:text-zinc-900 transition-colors flex items-center gap-2">
            <Calculator className="h-4 w-4" /> Calculator
          </Link>
        </div>
      </div>
    </nav>
  );
}
