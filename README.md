# FUTUREYOU

FutureYou is a decision intelligence and scenario simulation application with a FastAPI backend and a Next.js frontend.

## Project Overview

- **Backend:** Python + FastAPI
- **Frontend:** React + Next.js + Tailwind CSS
- **Purpose:** Help users model decisions, simulate scenarios, and explore recommended outcomes.

## Repository Structure

- `backend/` - Python backend service
  - `backend/app/main.py` - FastAPI entrypoint
  - `backend/app/api/` - API routes
  - `backend/app/db/` - Database initialization and session management
  - `backend/app/models/` - ORM entities
  - `backend/app/rag/` - retrieval-augmented generation support
  - `backend/app/schemas/` - request/response schemas
  - `backend/app/services/` - business logic services
- `frontend/` - Next.js application
  - `frontend/app/` - Next.js pages and routes
  - `frontend/components/` - UI components
  - `frontend/lib/` - shared utilities and API client
  - `frontend/types/` - TypeScript types

## Features

- Decision creation and management
- Scenario simulation under each decision
- Data source management
- Full-stack backend + frontend architecture

## Local Development

### Backend

1. Open a terminal in `backend`
2. Create and activate your Python virtual environment:

```powershell
cd c:\FutureYOU\backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Run the backend service:

```powershell
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will start at `http://localhost:8000`.

### Frontend

1. Open a terminal in `frontend`

```powershell
cd c:\FutureYOU\frontend
```

2. Install dependencies:

```powershell
npm install
```

3. Run the frontend app:

```powershell
npm run dev
```

The frontend will start at `http://localhost:3000`.

### Notes

- The backend seeds initial source data on startup via `app.db.init_db`.
- If your backend uses a database file or external database, confirm configuration in `backend/app/core/config.py`.

## Production / Deployment Notes

- Build the frontend with `npm run build` inside `frontend/`.
- Configure a production server or hosting provider for the FastAPI backend.
- Use environment variables for secrets and connection strings rather than hardcoding values.

## GitHub Setup

1. Create a new repository on GitHub called `FUTUREYOU`.
2. From the root of this project run:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/FUTUREYOU.git
git push -u origin main
```

Replace `YOUR_USERNAME` with your GitHub username.

## Recommended `.gitignore`

Add or update a `.gitignore` file to exclude local environment files and build artifacts, for example:

```
.venv/
__pycache__/
*.pyc
node_modules/
.next/
.DS_Store
```

## Contact

If you want, I can also help you add a README `Features` section, architecture diagram, or deployment checklist for your production engineer audience.

## Live Demo

- **Frontend (live):** https://your-frontend.vercel.app  
- **Backend API (live):** https://your-backend.onrender.com

Replace the placeholder URLs above with the real URLs you get after deployment.

### Quick deployment guide

Recommended fast path: deploy the frontend to **Vercel** and the backend to **Render** (or Railway). After both are deployed, add the frontend URL as the `Live Demo` link above.

Frontend (Vercel)

1. Push your repository to GitHub (already done).
2. Sign in to https://vercel.com and create a new project -> "Import Git Repository" -> select `FUTUREYOU`.
3. For the root path, choose `/frontend`.
4. Set the build command to `npm run build` and the output directory to `.next` (Vercel auto-detects Next.js in most cases).
5. Add any environment variables the frontend needs (e.g., `NEXT_PUBLIC_API_URL=https://your-backend.onrender.com`).
6. Deploy — Vercel will provide a live URL (copy it into the `Live Demo` link above).

Backend (Render)

1. Sign in to https://render.com and create a new Web Service -> "Connect a repository" -> choose the `backend` folder.
2. Set the start command to `uvicorn app.main:app --host 0.0.0.0 --port $PORT` and the environment to Python 3.11.
3. Add environment variables (database URL, secrets) in Render's dashboard.
4. Ensure CORS in `backend/app/core/config.py` includes your frontend URL (or `*` for testing) so the deployed frontend can call the API.
5. Deploy — Render provides a URL like `https://your-backend.onrender.com`.

Notes

- Use secure environment variables for keys and DB credentials.  
- For production, enable HTTPS and configure proper DB hosting (Postgres, etc.) instead of local SQLite.  
- To show the live demo on GitHub, edit the `Live Demo` URLs above with the real deployment links and commit the change.

If you'd like, I can deploy the frontend to Vercel and the backend to Render for you (I will guide you through any credentials and environment variables needed). 
