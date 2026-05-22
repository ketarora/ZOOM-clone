'use client';
export default function Contacts() {
  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Contacts</h1>
      <div className="bg-surface border border-border rounded-xl shadow-sm">
        <div className="p-4 border-b border-border">
          <input type="text" placeholder="Search contacts..." className="form-input w-full max-w-md" />
        </div>
        <div className="p-0">
          <div className="bg-surface-low px-6 py-2 text-sm font-bold text-text-secondary border-b border-border sticky top-[var(--topbar-h)]">A</div>
          <div className="flex items-center gap-4 p-4 px-6 border-b border-border hover:bg-surface-low cursor-pointer">
            <div className="w-10 h-10 rounded-full bg-primary-light text-primary flex items-center justify-center font-bold">AT</div>
            <div>
              <div className="font-semibold text-text-primary">Alex Thompson</div>
              <div className="text-sm text-text-secondary">alex@zoomconnect.demo</div>
            </div>
          </div>

          <div className="bg-surface-low px-6 py-2 text-sm font-bold text-text-secondary border-b border-border sticky top-[calc(var(--topbar-h)+36px)]">S</div>
          <div className="flex items-center gap-4 p-4 px-6 hover:bg-surface-low cursor-pointer">
            <div className="w-10 h-10 rounded-full bg-orange/20 text-orange flex items-center justify-center font-bold">SJ</div>
            <div>
              <div className="font-semibold text-text-primary">Sarah Jenkins</div>
              <div className="text-sm text-text-secondary">sarah@zoomconnect.demo</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
