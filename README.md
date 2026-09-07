# CompetencyIQ

CompetencyIQ is a React and FastAPI MVP for turning assessment evidence into student skill gaps and workforce-readiness decisions.

## Architecture

- `frontend/`: React + TypeScript/Vite client with a centralized API client and live/empty data states.
- `backend/app/`: FastAPI service, SQLAlchemy PostgreSQL connection, JWT verification, role checks, health, and aggregate endpoints.
- `backend/.env.example`: server-only configuration template. Database URLs, JWT secrets, service keys, and AI keys never go to the browser.

The original static prototype had no backend, database, authentication, or API calls. Its visual intent was preserved, but hardcoded score values were replaced with backend responses. An empty database is shown as an empty state, never as fabricated statistics.

## Run locally

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

Backend:

```powershell
cd backend
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
uvicorn app.main:app --reload --port 8000
```

Set `DATABASE_URL` to the Supabase PostgreSQL connection string and `SUPABASE_JWT_SECRET` before using authenticated endpoints. In local development, the frontend calls FastAPI at `http://127.0.0.1:8000`; set `VITE_API_BASE_URL` for another backend location.

## Supabase database setup

1. Create a Supabase project and open **Project Settings → Database**.
2. Copy the connection string and set it as `DATABASE_URL` in `backend/.env`. Use the session pooler connection for local development if direct connections are blocked.
3. Set the Supabase JWT secret as `SUPABASE_JWT_SECRET` in `backend/.env`.
4. Install backend dependencies and apply the schema migration:

```powershell
cd backend
c:/python314/python.exe -m pip install -r requirements.txt
c:/python314/python.exe -m alembic upgrade head
```

5. Start FastAPI and verify `http://127.0.0.1:8000/health` reports `database: healthy`.

Only `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` may be placed in `frontend/.env`. Never put `DATABASE_URL`, `SUPABASE_JWT_SECRET`, a service-role key, or `AI_API_KEY` in the frontend.

## Security notes

Public registration must provision `STUDENT` profiles only. The backend derives identity from the verified Supabase JWT and loads the application role from PostgreSQL; frontend role state is never trusted. Government routes require `GOVERNMENT_ADMIN`. Passwords and Supabase service-role credentials are not stored by this application.

## Current implementation boundary

The core foundation is in place. Remaining production slices are Alembic migrations for the full schema, Supabase sign-in screens, atomic assessment submission, skill-gap and recommendation services, reports, and the protected government UI. They should be added against the same service and authorization boundaries rather than reintroducing client-side business logic.
