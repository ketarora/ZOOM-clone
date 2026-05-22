'use client';
import { usePathname } from 'next/navigation';

export function Topbar() {
  const pathname = usePathname();
  if (pathname.startsWith('/room')) return null;

  return (
    <header className="h-[var(--topbar-h)] bg-surface border-b border-border flex items-center justify-between px-6 sticky top-0 z-10 flex-shrink-0">
      <div className="flex-1"></div>
      <div className="flex items-center gap-4">
        <div className="relative">
          <input type="text" placeholder="Search..." className="bg-surface-low border border-border rounded-full py-1.5 px-4 text-sm w-64 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary" />
        </div>
      </div>
    </header>
  );
}
