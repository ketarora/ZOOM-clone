'use client';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { Video, Calendar, Home, MonitorPlay, MessageSquare, BookUser, Phone, Settings, CirclePlay, LayoutDashboard } from 'lucide-react';

const navItems = [
  { name: 'Home', href: '/dashboard', icon: Home },
  { name: 'Meetings', href: '/meetings', icon: Video },
  { name: 'Team Chat', href: '/chat', icon: MessageSquare },
  { name: 'Contacts', href: '/contacts', icon: BookUser },
  { name: 'Recordings', href: '/recordings', icon: MonitorPlay },
  { name: 'Webinars', href: '/webinars', icon: LayoutDashboard },
  { name: 'Phone', href: '/phone', icon: Phone },
  { name: 'Whiteboard', href: '/whiteboard', icon: MonitorPlay },
  { name: 'Settings', href: '/settings', icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  // Do not show sidebar in meeting room
  if (pathname.startsWith('/room')) return null;

  return (
    <aside className="w-[var(--sidebar-w)] bg-surface border-r border-border h-screen flex-shrink-0 flex flex-col hidden md:flex sticky top-0 left-0">
      <div className="p-5 flex items-center gap-3 border-b border-border">
        <div className="w-8 h-8 rounded-lg bg-primary text-white flex items-center justify-center font-bold text-lg">Z</div>
        <div>
          <h2 className="font-bold text-text-primary leading-tight">ZoomConnect</h2>
          <p className="text-[11px] text-text-secondary uppercase tracking-wider font-semibold">Enterprise Workspace</p>
        </div>
      </div>

      <nav className="flex-1 overflow-y-auto py-4 px-3 space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname.startsWith(item.href);
          return (
            <Link key={item.name} href={item.href} className={`flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${isActive ? 'bg-primary-light text-primary border-l-4 border-primary' : 'text-text-secondary hover:bg-surface-low hover:text-text-primary border-l-4 border-transparent'}`}>
              <Icon className="w-5 h-5" />
              {item.name}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-border">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-primary-light flex items-center justify-center font-bold text-primary">A</div>
          <div>
            <div className="text-sm font-semibold text-text-primary">Alex Thompson</div>
            <div className="text-xs text-success flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-success inline-block"></span>
              Available
            </div>
          </div>
        </div>
      </div>
    </aside>
  );
}
