'use client';
import { useSearchParams } from 'next/navigation';
import { useEffect, useState, Suspense } from 'react';
import { Mic, MicOff, Video, VideoOff, MonitorUp, Users, MessageSquare, PhoneOff, Settings, ShieldAlert, ChevronUp } from 'lucide-react';

function RoomContent() {
  const searchParams = useSearchParams();
  const meetingId = searchParams.get('id');
  const [isVideoOn, setIsVideoOn] = useState(true);
  const [isMuted, setIsMuted] = useState(false);
  const [timer, setTimer] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => setTimer(t => t + 1), 1000);
    return () => clearInterval(interval);
  }, []);

  const formatTime = (seconds: number) => {
    const h = Math.floor(seconds / 3600).toString().padStart(2, '0');
    const m = Math.floor((seconds % 3600) / 60).toString().padStart(2, '0');
    const s = (seconds % 60).toString().padStart(2, '0');
    return `${h}:${m}:${s}`;
  };

  return (
    <div className="h-screen w-screen bg-[#111111] flex flex-col fixed inset-0 z-[100] text-white">
      {/* Top Info Bar */}
      <div className="h-10 absolute top-0 left-0 w-full flex items-center justify-between px-4 z-10 bg-gradient-to-b from-black/60 to-transparent pointer-events-none">
        <div className="flex items-center gap-2 pointer-events-auto bg-black/40 px-3 py-1 rounded-md backdrop-blur-md">
          <ShieldAlert className="w-4 h-4 text-green-500" />
          <span className="text-xs font-semibold tracking-wide">ZoomConnect Meeting</span>
          <span className="text-xs text-gray-400 font-mono ml-2">ID: {meetingId || 'Unknown'}</span>
        </div>
        <div className="flex items-center gap-4 pointer-events-auto">
          <div className="bg-black/40 px-3 py-1 rounded-md backdrop-blur-md text-xs font-mono">
            {formatTime(timer)}
          </div>
          <button className="bg-black/40 hover:bg-black/60 px-3 py-1 rounded-md backdrop-blur-md text-xs font-semibold flex items-center gap-1 transition">
            <Users className="w-3 h-3" /> View
          </button>
        </div>
      </div>

      {/* Main Video Canvas */}
      <div className="flex-1 flex items-center justify-center relative p-6 pt-12 overflow-hidden">
        <div className="w-full max-w-7xl h-full bg-[#1e1e1e] rounded-xl relative overflow-hidden flex items-center justify-center border border-gray-800 shadow-2xl transition-all">
          {isVideoOn ? (
            <img src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?auto=format&fit=crop&q=80&w=1200" alt="Video feed" className="object-cover w-full h-full" />
          ) : (
            <div className="w-32 h-32 rounded-full bg-gray-800 text-white flex items-center justify-center text-4xl font-semibold shadow-inner">AT</div>
          )}
          <div className="absolute bottom-4 left-4 bg-black/70 backdrop-blur-md px-3 py-1.5 rounded-lg text-white text-sm font-medium flex items-center gap-2">
            Alex Thompson {isMuted && <MicOff className="w-4 h-4 text-red-500 ml-1" />}
          </div>
        </div>
      </div>

      {/* Zoom Bottom Toolbar */}
      <div className="h-[72px] bg-[#1a1a1a] flex items-center justify-between px-4 text-white border-t border-black relative">
        <div className="flex items-center gap-1">
          <div className="flex flex-col items-center">
            <button aria-label={isMuted ? "Unmute Microphone" : "Mute Microphone"} onClick={() => setIsMuted(!isMuted)} className={`w-12 h-12 flex flex-col items-center justify-center rounded-lg hover:bg-[#333333] transition ${isMuted ? 'text-red-500' : 'text-gray-300'}`}>
              {isMuted ? <MicOff className="w-6 h-6 mb-1" /> : <Mic className="w-6 h-6 mb-1" />}
              <span className="text-[10px] font-medium leading-none">{isMuted ? 'Unmute' : 'Mute'}</span>
            </button>
          </div>
          <button className="w-4 h-12 flex items-center justify-center rounded-r-lg hover:bg-[#333333] text-gray-400">
            <ChevronUp className="w-3 h-3" />
          </button>

          <div className="w-px h-8 bg-gray-700 mx-1"></div>

          <div className="flex flex-col items-center">
            <button aria-label={isVideoOn ? "Stop Video" : "Start Video"} onClick={() => setIsVideoOn(!isVideoOn)} className={`w-12 h-12 flex flex-col items-center justify-center rounded-lg hover:bg-[#333333] transition ${!isVideoOn ? 'text-red-500' : 'text-gray-300'}`}>
              {!isVideoOn ? <VideoOff className="w-6 h-6 mb-1" /> : <Video className="w-6 h-6 mb-1" />}
              <span className="text-[10px] font-medium leading-none">{!isVideoOn ? 'Start Video' : 'Stop Video'}</span>
            </button>
          </div>
          <button className="w-4 h-12 flex items-center justify-center rounded-r-lg hover:bg-[#333333] text-gray-400">
            <ChevronUp className="w-3 h-3" />
          </button>
        </div>

        <div className="flex items-center gap-2 absolute left-1/2 -translate-x-1/2">
          <button aria-label="Participants" className="w-16 h-12 flex flex-col items-center justify-center rounded-lg hover:bg-[#333333] text-gray-300 transition relative">
            <Users className="w-6 h-6 mb-1" />
            <span className="text-[10px] font-medium leading-none">Participants</span>
            <span className="absolute top-1 right-2 bg-gray-700 text-[9px] px-1 rounded-sm">1</span>
          </button>
          <button aria-label="Chat" className="w-16 h-12 flex flex-col items-center justify-center rounded-lg hover:bg-[#333333] text-gray-300 transition">
            <MessageSquare className="w-6 h-6 mb-1" />
            <span className="text-[10px] font-medium leading-none">Chat</span>
          </button>
          <button aria-label="Share Screen" className="w-16 h-12 flex flex-col items-center justify-center rounded-lg hover:bg-[#333333] text-green-500 transition">
            <MonitorUp className="w-6 h-6 mb-1" />
            <span className="text-[10px] font-medium leading-none text-green-500">Share</span>
          </button>
        </div>

        <div className="flex items-center gap-4">
          <button aria-label="End Meeting" className="px-4 py-1.5 bg-[#DE2828] hover:bg-red-700 text-white rounded-md text-sm font-semibold transition" onClick={() => window.location.href='/dashboard'}>
            End
          </button>
        </div>
      </div>
    </div>
  );
}

export default function Room() {
  return (
    <Suspense fallback={<div className="h-screen w-screen bg-black flex items-center justify-center text-white">Loading...</div>}>
      <RoomContent />
    </Suspense>
  )
}
