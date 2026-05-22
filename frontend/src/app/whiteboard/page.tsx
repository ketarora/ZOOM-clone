'use client';
export default function Whiteboard() {
  return (
    <div className="h-[calc(100vh-var(--topbar-h))] bg-surface relative overflow-hidden bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] bg-opacity-10">
      <div className="absolute top-4 left-4 bg-surface rounded-lg shadow-md border border-border p-2 flex flex-col gap-2">
        <button className="p-2 hover:bg-surface-low rounded bg-primary-light text-primary"><svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.572L16.732 3.732z" /></svg></button>
        <button className="p-2 hover:bg-surface-low rounded text-text-secondary"><svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" /></svg></button>
        <button className="p-2 hover:bg-surface-low rounded text-text-secondary"><svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg></button>
      </div>
      <div className="flex items-center justify-center h-full text-text-muted">
        <p className="bg-surface px-4 py-2 rounded-full shadow-sm text-sm border border-border font-medium">Canvas Ready for Collaboration</p>
      </div>
    </div>
  );
}
