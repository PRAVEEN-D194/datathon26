import React from 'react';

export const SkeletonLoader: React.FC<{ rows?: number }> = ({ rows = 4 }) => {
  return (
    <div className="space-y-3 p-4">
      <div className="h-6 skeleton-shimmer rounded-xl w-1/3" />
      {Array.from({ length: rows }).map((_, i) => (
        <div key={i} className="h-12 skeleton-shimmer rounded-xl w-full opacity-80" />
      ))}
    </div>
  );
};
