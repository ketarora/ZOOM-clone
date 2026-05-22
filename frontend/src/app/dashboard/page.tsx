'use client';
import { useEffect, useState } from 'react';
import { Api, autoLogin } from '@/lib/api';
import { useRouter } from 'next/navigation';
import { Video, Calendar, MonitorUp, Plus } from 'lucide-react';

function useLiveClock() {
  const [time, setTime] = useState(new Date());
  useEffect(() => {
    const timer = setInterval(() => setTime(new Date()), 1000);
    return () => clearInterval(timer);
  }, []);
  return time;
}

export default function Dashboard() {
  const [data, setData] = useState<any>(null);
  const router = useRouter();
  const time = useLiveClock();

  useEffect(() => {
    autoLogin().then(() => {
      Api.getDashboard().then(setData).catch(console.error);
    });
  }, []);

  const createInstantMeeting = async () => {
    try {
      const now = new Date();
      now.setSeconds(0, 0);
      const meeting = await Api.createMeeting({
        topic: 'Instant Meeting',
        start_time: now.toISOString(),
        duration_minutes: 60,
        waiting_room: false,
        use_passcode: false,
        timezone: 'UTC',
      });
      router.push(`/room?id=${meeting.meeting_id}`);
    } catch (e) {
      alert('Failed to create meeting');
    }
  };

  const handleStart = async (meetingId: number) => {
    try {
      const res = await Api.startMeeting(meetingId);
      router.push(`/room?id=${res.meeting_id}`);
    } catch (e) {
      alert('Failed to start meeting');
    }
  };

  if (!data) return <div className="p-10 text-text-secondary">Loading...</div>;

  return (
    <div className="p-8 max-w-6xl mx-auto">
      {/* Top 4 Buttons - Zoom Core Layout */}
      <div className="grid grid-cols-4 gap-6 mb-10">
        <button onClick={createInstantMeeting} className="flex flex-col items-center justify-center p-6 bg-surface rounded-xl border border-border hover:shadow-md transition group">
          <div className="w-16 h-16 bg-orange rounded-[20px] flex items-center justify-center mb-3 group-hover:scale-105 transition-transform shadow-sm">
            <Video className="w-8 h-8 text-white" />
          </div>
          <span className="font-semibold text-text-primary text-sm">New Meeting</span>
        </button>
        <button onClick={() => router.push('/join')} className="flex flex-col items-center justify-center p-6 bg-surface rounded-xl border border-border hover:shadow-md transition group">
          <div className="w-16 h-16 bg-primary rounded-[20px] flex items-center justify-center mb-3 group-hover:scale-105 transition-transform shadow-sm">
            <Plus className="w-8 h-8 text-white" />
          </div>
          <span className="font-semibold text-text-primary text-sm">Join</span>
        </button>
        <button onClick={() => router.push('/schedule')} className="flex flex-col items-center justify-center p-6 bg-surface rounded-xl border border-border hover:shadow-md transition group">
          <div className="w-16 h-16 bg-primary rounded-[20px] flex items-center justify-center mb-3 group-hover:scale-105 transition-transform shadow-sm">
            <Calendar className="w-8 h-8 text-white" />
          </div>
          <span className="font-semibold text-text-primary text-sm">Schedule</span>
        </button>
        <button className="flex flex-col items-center justify-center p-6 bg-surface rounded-xl border border-border hover:shadow-md transition group">
          <div className="w-16 h-16 bg-primary rounded-[20px] flex items-center justify-center mb-3 group-hover:scale-105 transition-transform shadow-sm">
            <MonitorUp className="w-8 h-8 text-white" />
          </div>
          <span className="font-semibold text-text-primary text-sm">Share Screen</span>
        </button>
      </div>

      <div className="flex gap-8">
        {/* Left Col: Clock & Background */}
        <div className="w-1/3">
          <div className="bg-surface rounded-xl border border-border overflow-hidden relative h-48">
            <div className="absolute inset-0 bg-gradient-to-br from-primary to-primary-dark opacity-10"></div>
            <div className="relative p-6 h-full flex flex-col justify-center">
              <h1 className="text-5xl font-light text-text-primary tabular-nums tracking-tight mb-2" suppressHydrationWarning>
                {time.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </h1>
              <p className="text-text-secondary font-medium" suppressHydrationWarning>
                {time.toLocaleDateString([], { weekday: 'long', month: 'long', day: 'numeric' })}
              </p>
            </div>
          </div>
        </div>

        {/* Right Col: Meetings */}
        <div className="w-2/3">
          <div className="bg-surface rounded-xl border border-border overflow-hidden">
            <div className="px-6 py-4 border-b border-border bg-surface-low">
              <h2 className="font-semibold text-text-primary">Upcoming Meetings</h2>
            </div>
            <div className="divide-y divide-border">
              {data.upcoming_meetings?.length === 0 ? (
                <div className="p-8 text-center text-text-secondary text-sm">No upcoming meetings today.</div>
              ) : (
                data.upcoming_meetings?.map((m: any) => (
                  <div key={m.id} className="p-4 flex items-center justify-between hover:bg-surface-low transition">
                    <div className="flex items-center gap-4">
                      <div className="w-20 border-r border-border pr-4">
                        <div className="text-sm font-semibold text-text-primary">{new Date(m.start_time).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</div>
                      </div>
                      <div>
                        <h4 className="font-semibold text-text-primary text-sm">{m.topic}</h4>
                        <p className="text-xs text-text-secondary mt-1 tracking-wide">Meeting ID: {m.meeting_id}</p>
                      </div>
                    </div>
                    <button onClick={() => handleStart(m.id)} className="btn-primary py-1.5 px-4 text-sm">Start</button>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
