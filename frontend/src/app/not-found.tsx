import Link from 'next/link';
import { AlertCircle } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="min-h-[80vh] flex flex-col items-center justify-center px-4 text-center">
      <div className="bg-red-50 text-red-500 p-4 rounded-full mb-6">
        <AlertCircle className="w-12 h-12" />
      </div>
      <h2 className="text-4xl font-extrabold text-zinc-900 tracking-tight mb-4">
        404 - Metric Not Found
      </h2>
      <p className="text-zinc-500 max-w-md mb-8">
        We couldn't find the battery chemistry or specific metric you were looking for. It might have been moved or removed.
      </p>
      <Link 
        href="/" 
        className="px-6 py-3 bg-zinc-900 text-white font-medium rounded-full hover:bg-zinc-800 transition-colors"
      >
        Return to Dashboard
      </Link>
    </div>
  );
}
