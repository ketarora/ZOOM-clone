'use client';
export default function Phone() {
  return (
    <div className="flex h-[calc(100vh-var(--topbar-h))]">
      <div className="flex-1 flex items-center justify-center p-8">
        <div className="w-[360px] bg-surface rounded-2xl shadow-lg border border-border p-8 flex flex-col items-center">
          <input type="text" readOnly className="w-full text-center text-4xl font-light mb-8 outline-none bg-transparent" placeholder="Enter number" />

          <div className="grid grid-cols-3 gap-6 mb-8 w-full">
            {[1,2,3,4,5,6,7,8,9,'*',0,'#'].map((num, i) => (
              <button key={i} className="w-16 h-16 rounded-full bg-surface-low hover:bg-border text-2xl font-medium flex items-center justify-center transition-colors mx-auto">
                {num}
              </button>
            ))}
          </div>

          <button className="w-16 h-16 rounded-full bg-primary hover:bg-primary-dark text-white flex items-center justify-center shadow-md transition-colors">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" /></svg>
          </button>
        </div>
      </div>
    </div>
  );
}
