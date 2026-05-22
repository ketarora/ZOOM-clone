'use client';
export default function Webinars() {
  return (
    <div className="p-8">
      <h1 className="text-3xl font-bold mb-6">Webinars</h1>
      <div className="bg-surface border border-border rounded-xl p-12 text-center text-text-secondary">
        <svg className="w-16 h-16 mx-auto mb-4 text-border-strong" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>
        <h2 className="text-xl font-semibold text-text-primary mb-2">Engage your audience</h2>
        <p className="max-w-md mx-auto mb-6">Host large-scale virtual events with advanced registration, panelist controls, and Q&A features.</p>
        <button className="btn-primary mx-auto">Schedule a Webinar</button>
      </div>
    </div>
  );
}
