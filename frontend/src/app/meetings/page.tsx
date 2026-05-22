'use client';
import { useEffect, useState } from 'react';
import { Api } from '@/lib/api';
import { useRouter } from 'next/navigation';
import { Play, Copy, Edit2, Trash2, Video } from 'lucide-react';

export default function Meetings() {
  const [meetings, setMeetings] = useState<any[]>([]);
  const [selectedMeeting, setSelectedMeeting] = useState<any>(null);
  const router = useRouter();

  const loadMeetings = async () => {
    try {
      const data = await Api.getMeetings('upcoming');
      setMeetings(data);
      if (data.length > 0 && !selectedMeeting) {
        setSelectedMeeting(data[0]);
      } else if (data.length === 0) {
        setSelectedMeeting(null);
      }
    } catch (e) {
      console.error(e);
    }
  };

  useEffect(() => { loadMeetings(); }, []);

  const handleDelete = async (id: number) => {
    if (confirm('Delete this meeting?')) {
      await Api.deleteMeeting(id);
      setSelectedMeeting(null);
      loadMeetings();
    }
  };

  const handleStart = async (id: number) => {
    try {
      const res = await Api.startMeeting(id);
      router.push(`/room?id=${res.meeting_id}`);
    } catch (e) {
      alert('Failed to start meeting');
    }
  };

  return (
    <div className="flex h-[calc(100vh-var(--topbar-h))]">
      {/* Left List Pane */}
      <div className="w-80 border-r border-border bg-surface flex flex-col flex-shrink-0">
        <div className="p-4 border-b border-border flex items-center justify-between">
          <h2 className="text-xl font-bold">Meetings</h2>
          <button onClick={() => router.push('/schedule')} className="text-sm bg-surface-high hover:bg-border px-3 py-1.5 rounded-lg font-medium transition">Schedule</button>
        </div>
        <div className="flex-1 overflow-y-auto">
          {meetings.length === 0 ? (
            <div className="p-6 text-center text-text-secondary text-sm">No upcoming meetings.</div>
          ) : (
            meetings.map((m) => (
              <div
                key={m.id}
                onClick={() => setSelectedMeeting(m)}
                className={`p-4 border-b border-border cursor-pointer transition-colors ${selectedMeeting?.id === m.id ? 'bg-primary-light' : 'hover:bg-surface-low'}`}
              >
                <div className="text-xs font-semibold text-text-secondary mb-1">
                  {new Date(m.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
                </div>
                <div className={`font-semibold ${selectedMeeting?.id === m.id ? 'text-primary-dark' : 'text-text-primary'}`}>
                  {m.topic}
                </div>
                <div className="text-xs text-text-muted mt-1">ID: {m.meeting_id}</div>
              </div>
            ))
          )}
        </div>
      </div>

      {/* Right Detail Pane */}
      <div className="flex-1 bg-background p-8">
        {selectedMeeting ? (
          <div className="max-w-2xl bg-surface border border-border rounded-xl p-8 shadow-sm">
            <h1 className="text-3xl font-bold text-text-primary mb-2">{selectedMeeting.topic}</h1>
            <p className="text-text-secondary font-medium mb-8">
              {new Date(selectedMeeting.start_time).toLocaleString([], {weekday: 'long', month: 'long', day: 'numeric', hour: '2-digit', minute: '2-digit'})}
            </p>

            <div className="flex items-center gap-4 mb-8 pb-8 border-b border-border">
              <button onClick={() => handleStart(selectedMeeting.id)} className="btn-primary">
                <Play className="w-4 h-4 fill-white" /> Start
              </button>
              <button onClick={() => { navigator.clipboard.writeText(`Join my meeting: ${selectedMeeting.meeting_id}`); alert("Copied!"); }} className="btn-secondary">
                <Copy className="w-4 h-4" /> Copy Invitation
              </button>
              <button className="btn-secondary px-3" aria-label="Edit"><Edit2 className="w-4 h-4" /></button>
              <button onClick={() => handleDelete(selectedMeeting.id)} className="btn-secondary text-error hover:bg-error-light hover:text-error px-3" aria-label="Delete">
                <Trash2 className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-4">
              <div className="flex">
                <div className="w-1/3 text-sm text-text-secondary font-medium">Meeting ID</div>
                <div className="w-2/3 text-sm font-semibold tracking-wide">{selectedMeeting.meeting_id}</div>
              </div>
              <div className="flex">
                <div className="w-1/3 text-sm text-text-secondary font-medium">Security</div>
                <div className="w-2/3 text-sm space-y-1">
                  {selectedMeeting.use_passcode && <div>Passcode: <span className="font-mono bg-surface-high px-1 rounded">{selectedMeeting.passcode}</span></div>}
                  {selectedMeeting.waiting_room && <div>Waiting Room</div>}
                  {!selectedMeeting.use_passcode && !selectedMeeting.waiting_room && <div className="text-text-muted">None</div>}
                </div>
              </div>
            </div>
          </div>
        ) : (
          <div className="h-full flex flex-col items-center justify-center text-text-secondary">
            <Video className="w-12 h-12 mb-4 opacity-20" />
            <p>Select a meeting to view details</p>
          </div>
        )}
      </div>
    </div>
  );
}
