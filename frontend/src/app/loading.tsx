export default function Loading() {
  return (
    <div className="min-h-screen p-6 md:p-12 lg:p-24 max-w-7xl mx-auto space-y-8 animate-pulse">
      {/* Header Skeleton */}
      <div className="space-y-4">
        <div className="h-10 w-1/3 bg-zinc-200 rounded-lg"></div>
        <div className="h-4 w-1/2 bg-zinc-100 rounded"></div>
      </div>

      {/* Metric Cards Skeleton */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[1, 2, 3, 4].map((i) => (
          <div key={i} className="bg-white p-6 rounded-2xl shadow-sm border border-zinc-100 h-32 space-y-4">
            <div className="h-4 w-1/2 bg-zinc-100 rounded"></div>
            <div className="h-8 w-3/4 bg-zinc-200 rounded-lg"></div>
          </div>
        ))}
      </div>

      {/* Main Content Skeleton */}
      <div className="bg-white p-8 rounded-3xl shadow-sm border border-zinc-100 min-h-[400px] space-y-6">
        <div className="h-6 w-1/4 bg-zinc-200 rounded"></div>
        <div className="h-4 w-full bg-zinc-100 rounded"></div>
        <div className="h-4 w-full bg-zinc-100 rounded"></div>
        <div className="h-4 w-3/4 bg-zinc-100 rounded"></div>
      </div>
    </div>
  );
}
