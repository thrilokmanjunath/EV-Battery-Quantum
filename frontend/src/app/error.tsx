"use client";

import { useEffect } from "react";
import { AlertOctagon } from "lucide-react";

export default function Error({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  useEffect(() => {
    // Log the error to an error reporting service
    console.error(error);
  }, [error]);

  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center px-4 text-center">
      <div className="bg-red-50 text-red-600 p-4 rounded-full mb-6">
        <AlertOctagon className="w-12 h-12" />
      </div>
      <h2 className="text-3xl font-bold text-zinc-900 mb-4">
        Simulation Computation Error
      </h2>
      <p className="text-zinc-500 max-w-md mb-8">
        A critical error occurred while attempting to compute the battery logic or fetch from the quantum solvers.
      </p>
      <button
        onClick={() => reset()}
        className="px-6 py-3 bg-red-600 text-white font-medium rounded-full hover:bg-red-700 transition-colors"
      >
        Try again
      </button>
    </div>
  );
}
