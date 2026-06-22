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
