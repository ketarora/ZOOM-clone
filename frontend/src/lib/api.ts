const API_BASE = 'http://localhost:8000/api';

export const Api = {
  async login(email: string, password: string) {
    const res = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    if (!res.ok) throw await res.json();
    const data = await res.json();
    if (typeof window !== 'undefined') {
      localStorage.setItem('zc_token', data.access_token);
    }
    return data;
  },

  getToken() {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('zc_token');
    }
    return null;
  },

  authHeaders() {
    const token = this.getToken();
    return {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
    };
  },

  async getDashboard() {
    const res = await fetch(`${API_BASE}/dashboard`, { headers: this.authHeaders() });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async getMeetings(filter = 'upcoming') {
    const res = await fetch(`${API_BASE}/meetings?filter=${filter}`, { headers: this.authHeaders() });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async createMeeting(data: any) {
    const res = await fetch(`${API_BASE}/meetings`, {
      method: 'POST',
      headers: this.authHeaders(),
      body: JSON.stringify(data),
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async deleteMeeting(id: number) {
    const res = await fetch(`${API_BASE}/meetings/${id}`, {
      method: 'DELETE',
      headers: this.authHeaders(),
    });
    if (!res.ok && res.status !== 204) throw await res.json();
  },

  async joinMeeting(meetingId: string, name: string, passcode = '') {
    const res = await fetch(`${API_BASE}/meetings/join`, {
      method: 'POST',
      headers: this.authHeaders(),
      body: JSON.stringify({ meeting_id: meetingId, name, passcode }),
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async startMeeting(id: number) {
    const res = await fetch(`${API_BASE}/meetings/${id}/start`, {
      method: 'POST',
      headers: this.authHeaders(),
    });
    if (!res.ok) throw await res.json();
    return res.json();
  },

  async scheduleMeeting({ topic, description, start_time, duration_minutes, waiting_room, use_passcode }: any) {
    return this.createMeeting({
      topic, description, start_time, duration_minutes,
      waiting_room, use_passcode, timezone: 'UTC',
    });
  },

  async getRecordings(storage = 'all') {
    const res = await fetch(`${API_BASE}/recordings?storage=${storage}`, { headers: this.authHeaders() });
    if (!res.ok) throw await res.json();
    return res.json();
  },
};

export async function autoLogin() {
  if (!Api.getToken()) {
    try {
      await Api.login('alex@zoomconnect.demo', 'demo1234');
      console.log('✅ Auto-logged in as Alex Thompson (demo)');
    } catch (e) {
      console.warn('⚠️ Auto-login failed — backend may not be running');
    }
  }
}
