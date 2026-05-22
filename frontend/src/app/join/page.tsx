'use client';
import { useState } from 'react';
import { Api } from '@/lib/api';
import { useRouter } from 'next/navigation';

export default function Join() {
  const [meetingId, setMeetingId] = useState('');
  const [userName, setUserName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleJoin = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!meetingId) {
      setError('Please enter a Meeting ID');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const res = await Api.joinMeeting(meetingId, userName);
      router.push(`/room?id=${res.meeting_id}&name=${encodeURIComponent(userName)}`);
    } catch (err: any) {
      setError(err.detail || 'Meeting not found');
      setLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto mt-20">
      <div className="card p-8 shadow-sm">
        <h1 className="text-2xl font-bold text-center mb-6 text-text-primary">Join Meeting</h1>
        <form onSubmit={handleJoin} className="space-y-4">
          <div>
            <label className="block text-sm font-semibold text-text-primary mb-1">Meeting ID or Personal Link Name</label>
            <input
              type="text"
              className="form-input"
              placeholder="e.g. 123 456 7890"
              value={meetingId}
              onChange={e => setMeetingId(e.target.value)}
            />
          </div>
          <div>
            <label className="block text-sm font-semibold text-text-primary mb-1">Your Name</label>
            <input
              type="text"
              className="form-input"
              placeholder="Alex Thompson"
              value={userName}
              onChange={e => setUserName(e.target.value)}
            />
          </div>

          <div className="space-y-3 pt-2">
            <label className="flex items-center gap-3">
              <input type="checkbox" className="w-4 h-4 text-primary rounded border-border" />
              <span className="text-sm text-text-secondary">Remember my name for future meetings</span>
            </label>
            <label className="flex items-center gap-3">
              <input type="checkbox" className="w-4 h-4 text-primary rounded border-border" />
              <span className="text-sm text-text-secondary">Do not connect to audio</span>
            </label>
            <label className="flex items-center gap-3">
              <input type="checkbox" className="w-4 h-4 text-primary rounded border-border" />
              <span className="text-sm text-text-secondary">Turn off my video</span>
            </label>
          </div>

          {error && <p className="text-error text-sm text-center pt-2 font-medium">{error}</p>}

          <div className="pt-4">
            <button disabled={loading} type="submit" className="btn-primary w-full py-3 text-[15px] disabled:opacity-50">
              {loading ? 'Joining...' : 'Join'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
