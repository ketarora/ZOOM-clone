'use client';
import { useState } from 'react';
import { Api } from '@/lib/api';
import { useRouter } from 'next/navigation';

export default function Schedule() {
  const [topic, setTopic] = useState('Alex Thompson\'s Zoom Meeting');
  const [date, setDate] = useState('');
  const [time, setTime] = useState('');
  const [duration, setDuration] = useState('60');
  const [waitingRoom, setWaitingRoom] = useState(false);
  const [usePasscode, setUsePasscode] = useState(true);
  const [loading, setLoading] = useState(false);
  const router = useRouter();

  const handleSchedule = async () => {
    if (!topic || !date || !time) return alert('Please fill in required fields');
    setLoading(true);
    try {
      const start_time = new Date(`${date}T${time}:00`).toISOString();
      const res = await Api.scheduleMeeting({
        topic,
        start_time,
        duration_minutes: parseInt(duration),
        waiting_room: waitingRoom,
        use_passcode: usePasscode
      });
      alert(`Meeting scheduled! ID: ${res.meeting_id}`);
      router.push('/meetings');
    } catch (e) {
      alert('Failed to schedule meeting');
      setLoading(false);
    }
  };

  return (
    <div className="p-8 max-w-4xl mx-auto">
      <h1 className="text-2xl font-bold text-text-primary mb-6">Schedule a Meeting</h1>

      <div className="bg-surface border border-border rounded-xl shadow-sm overflow-hidden">
        <div className="p-6 space-y-6">

          <div className="flex items-start gap-4">
            <label className="w-1/4 text-sm font-semibold text-text-primary pt-2">Topic</label>
            <div className="w-3/4">
              <input type="text" className="form-input" value={topic} onChange={e=>setTopic(e.target.value)} />
            </div>
          </div>

          <div className="flex items-start gap-4">
            <label className="w-1/4 text-sm font-semibold text-text-primary pt-2">Date & Time</label>
            <div className="w-3/4 flex gap-3">
              <input type="date" className="form-input w-40" value={date} onChange={e=>setDate(e.target.value)} />
              <input type="time" className="form-input w-32" value={time} onChange={e=>setTime(e.target.value)} />
            </div>
          </div>

          <div className="flex items-start gap-4">
            <label className="w-1/4 text-sm font-semibold text-text-primary pt-2">Duration</label>
            <div className="w-3/4">
              <select className="form-input w-48" value={duration} onChange={e=>setDuration(e.target.value)}>
                <option value="15">15 minutes</option>
                <option value="30">30 minutes</option>
                <option value="45">45 minutes</option>
                <option value="60">1 hour</option>
                <option value="120">2 hours</option>
              </select>
            </div>
          </div>

          <div className="border-t border-border pt-6 mt-6">
            <div className="flex items-start gap-4">
              <label className="w-1/4 text-sm font-semibold text-text-primary pt-1">Security</label>
              <div className="w-3/4 space-y-3">
                <label className="flex items-center gap-3 cursor-pointer">
                  <div className="relative inline-flex items-center">
                    <input type="checkbox" className="sr-only peer" checked={usePasscode} onChange={e=>setUsePasscode(e.target.checked)} />
                    <div className="w-11 h-6 bg-surface-high peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-border after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                  </div>
                  <span className="text-sm font-medium text-text-primary">Passcode</span>
                </label>
                <p className="text-xs text-text-secondary pl-14">Only users who have the invite link or passcode can join.</p>

                <label className="flex items-center gap-3 cursor-pointer mt-4">
                  <div className="relative inline-flex items-center">
                    <input type="checkbox" className="sr-only peer" checked={waitingRoom} onChange={e=>setWaitingRoom(e.target.checked)} />
                    <div className="w-11 h-6 bg-surface-high peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-border after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
                  </div>
                  <span className="text-sm font-medium text-text-primary">Waiting Room</span>
                </label>
                <p className="text-xs text-text-secondary pl-14">Only users admitted by the host can join.</p>
              </div>
            </div>
          </div>

        </div>

        <div className="bg-surface-low border-t border-border p-4 flex justify-end gap-3">
          <button className="btn-secondary" onClick={() => router.back()}>Cancel</button>
          <button className="btn-primary min-w-[100px]" onClick={handleSchedule} disabled={loading}>{loading ? 'Saving...' : 'Save'}</button>
        </div>
      </div>
    </div>
  );
}
