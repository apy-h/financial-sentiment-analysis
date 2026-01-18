# Render Deployment Guide - Fullstack SPA

## Render Configuration

### Web Service Settings

**Build Command:**
```bash
npm install --prefix frontend && pip install -r backend/requirements.txt
```

**Start Command:**
```bash
bash start.sh
```

**Environment Variables:**
- `FLASK_ENV=production`
- `FLASK_DEBUG=false`

### How It Works

1. **Build Phase**:
   - Installs frontend dependencies
   - Installs backend dependencies

2. **Start Phase** (start.sh):
   - Builds React app → `frontend/dist/`
   - Sets `VITE_API_BASE=""` (empty = same server, relative URLs)
   - Runs database migrations
   - Starts Flask with gunicorn
   - Flask serves both:
     - API endpoints at `/api/*`
     - React SPA from `/` (all other routes)

3. **Result**:
   - Single URL for entire app
   - Frontend makes API calls to same domain (no CORS issues)
   - SPA routing works (catch-all serves index.html)

## Testing Locally

Development mode (separate servers):
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

Production mode (single server):
```bash
bash start.sh
# Visit http://localhost:5000
```

## Post-Deployment

Once deployed, your app will be available at:
- Main app: `https://your-app.onrender.com/`
- API: `https://your-app.onrender.com/api/v1/*`
- Health: `https://your-app.onrender.com/api/v1/health`

No need to update CORS origins since frontend and backend share the same domain!
