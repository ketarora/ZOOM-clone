# ZoomConnect — Backend README

## Quick Start

```bash
# 1. Go into backend folder
cd backend

# 2. Install dependencies
pip install -r requirements.txt

# 3. Seed demo data (optional)
python seed.py

# 4. Start the server
python main.py
# OR with auto-reload:
uvicorn main:app --reload --port 8000
```

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc

## Demo Login
```
Email:    alex@zoomconnect.demo
Password: demo1234
```

## Architecture

```
backend/
  main.py       — FastAPI app, all routes, WebSocket handlers
  models.py     — SQLAlchemy ORM models (SQLite)
  schemas.py    — Pydantic request/response schemas
  seed.py       — Demo data seeder
  requirements.txt
  zoomconnect.db  (auto-created on first run)
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/auth/register | Create account |
| POST | /api/auth/login | Get JWT token |
| GET | /api/users/me | Get profile |
| PATCH | /api/users/me | Update profile |
| GET | /api/meetings | List meetings |
| POST | /api/meetings | Create meeting |
| GET | /api/meetings/{id} | Get meeting |
| PATCH | /api/meetings/{id} | Update meeting |
| DELETE | /api/meetings/{id} | Delete meeting |
| POST | /api/meetings/{id}/start | Start meeting |
| POST | /api/meetings/join | Join by ID |
| GET | /api/recordings | List recordings |
| DELETE | /api/recordings/{id} | Delete recording |
| GET | /api/channels | List channels |
| POST | /api/channels | Create channel |
| GET | /api/channels/{id}/messages | Get messages |
| POST | /api/channels/{id}/messages | Send message |
| GET | /api/contacts | List contacts |
| POST | /api/contacts | Add contact |
| DELETE | /api/contacts/{id} | Remove contact |
| GET | /api/webinars | List webinars |
| POST | /api/webinars | Schedule webinar |
| GET | /api/dashboard | Dashboard stats |
| WS | /ws/meeting/{id} | WebRTC signaling |
| WS | /ws/chat/{channel_id} | Real-time chat |

## Tech Stack
- **FastAPI** — Modern async Python web framework
- **SQLAlchemy** — ORM with SQLite
- **Pydantic v2** — Data validation
- **JWT (python-jose)** — Auth tokens
- **bcrypt (passlib)** — Password hashing
- **WebSockets** — Real-time meeting signaling + chat
