'use client';
import { useState, useRef, useEffect } from 'react';
import { Hash, Phone, Video, Send, Search, Image as ImageIcon, Smile, FilePlus2 } from 'lucide-react';

export default function Chat() {
  const [message, setMessage] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleInput = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value);
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 120)}px`;
    }
  };

  return (
    <div className="flex h-[calc(100vh-var(--topbar-h))] bg-surface">
      {/* Sidebar */}
      <div className="w-72 border-r border-border flex flex-col flex-shrink-0">
        <div className="p-4 border-b border-border">
          <div className="relative">
            <Search className="w-4 h-4 absolute left-3 top-1/2 -translate-y-1/2 text-text-muted" />
            <input type="text" placeholder="Jump to..." className="w-full bg-surface-low border border-border rounded-lg py-1.5 pl-9 pr-3 text-sm focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary" />
          </div>
        </div>
        <div className="flex-1 overflow-y-auto p-2 space-y-1">
          <div className="px-2 py-1 text-xs font-semibold text-text-secondary uppercase tracking-wider mt-2 mb-1">Starred</div>
          <button className="w-full flex items-center gap-2 px-2 py-1.5 rounded bg-primary-light text-primary font-medium">
            <Hash className="w-4 h-4" /> engineering-team
          </button>

          <div className="px-2 py-1 text-xs font-semibold text-text-secondary uppercase tracking-wider mt-4 mb-1">Channels</div>
          <button className="w-full flex items-center gap-2 px-2 py-1.5 rounded hover:bg-surface-low text-text-primary text-sm transition">
            <Hash className="w-4 h-4 text-text-muted" /> general
          </button>
          <button className="w-full flex items-center gap-2 px-2 py-1.5 rounded hover:bg-surface-low text-text-primary text-sm transition font-bold">
            <Hash className="w-4 h-4 text-text-muted" /> product-design
            <span className="ml-auto bg-error text-white text-[10px] px-1.5 rounded-full">3</span>
          </button>
        </div>
      </div>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col min-w-0 bg-background">
        <div className="h-14 border-b border-border bg-surface flex items-center justify-between px-6 flex-shrink-0">
          <div className="flex items-center gap-2">
            <Hash className="w-5 h-5 text-text-secondary" />
            <h2 className="font-bold text-text-primary">engineering-team</h2>
          </div>
          <div className="flex items-center gap-2">
            <button className="p-2 text-text-secondary hover:bg-surface-low rounded-lg transition" aria-label="Audio Call"><Phone className="w-4 h-4" /></button>
            <button className="p-2 text-text-secondary hover:bg-surface-low rounded-lg transition" aria-label="Video Call"><Video className="w-4 h-4" /></button>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          <div className="flex gap-4">
            <div className="w-10 h-10 rounded bg-orange text-white flex flex-shrink-0 items-center justify-center font-bold">SJ</div>
            <div>
              <div className="flex items-baseline gap-2">
                <span className="font-bold text-text-primary text-sm">Sarah Jenkins</span>
                <span className="text-xs text-text-muted">10:42 AM</span>
              </div>
              <p className="text-sm text-text-primary mt-0.5">Has anyone looked at the new API rate limits? We are hitting 429s in staging.</p>
            </div>
          </div>

          <div className="flex gap-4">
            <div className="w-10 h-10 rounded bg-primary text-white flex flex-shrink-0 items-center justify-center font-bold">A</div>
            <div>
              <div className="flex items-baseline gap-2">
                <span className="font-bold text-text-primary text-sm">Alex Thompson (You)</span>
                <span className="text-xs text-text-muted">10:45 AM</span>
              </div>
              <p className="text-sm text-text-primary mt-0.5">Yeah, I deployed a fix for that 5 mins ago. Should be resolved now.</p>
            </div>
          </div>
        </div>

        <div className="p-4 bg-surface border-t border-border">
          <div className="border border-border rounded-xl bg-surface focus-within:border-primary focus-within:ring-1 focus-within:ring-primary transition-all overflow-hidden flex flex-col">
            <textarea
              ref={textareaRef}
              value={message}
              onChange={handleInput}
              rows={1}
              className="w-full max-h-[120px] p-3 text-sm text-text-primary outline-none resize-none bg-transparent"
              placeholder="Message #engineering-team"
              style={{ minHeight: '44px' }}
            />
            <div className="bg-surface-low px-2 py-1.5 flex items-center justify-between border-t border-border/50">
              <div className="flex items-center gap-1">
                <button className="p-1.5 text-text-secondary hover:bg-border rounded transition"><FilePlus2 className="w-4 h-4" /></button>
                <button className="p-1.5 text-text-secondary hover:bg-border rounded transition"><ImageIcon className="w-4 h-4" /></button>
                <button className="p-1.5 text-text-secondary hover:bg-border rounded transition"><Smile className="w-4 h-4" /></button>
              </div>
              <button disabled={!message.trim()} className="p-1.5 bg-primary disabled:bg-primary-light disabled:text-primary-light/50 text-white rounded transition">
                <Send className="w-4 h-4" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
