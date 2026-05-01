# Setup & Deployment Guide

This guide covers the steps required to set up the Slooze platform in various environments.

## 💻 Local Development

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.10+

### 1. Environment Setup
Copy the example environment file and adjust if necessary:
```bash
cp .env.example .env
```

### 2. Infrastructure
Start the database and cache services:
```bash
docker compose up -d postgres redis
```

### 3. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
# Run database migrations/seeding
python -m app.database.seed
# Start server
uvicorn app.main:app --reload
```

### 4. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

---

## 🐋 Dockerized Setup (Full Stack)

To run the entire platform (Frontend + Backend + Nginx + DB) in a single command:
```bash
docker compose up --build
```
The application will be accessible at `http://localhost`.

---

## 🚀 Production Considerations

### Database
- Use a managed service (AWS RDS, GCP Cloud SQL).
- Enable daily backups and Point-In-Time Recovery (PITR).

### Security
- Change the `JWT_SECRET_KEY` in `.env`.
- Ensure Nginx is configured with SSL (Certbot/Let's Encrypt).
- Set `DEBUG=false` in the backend.

### Scaling
- **Horizontal Scaling:** The backend is stateless and can be scaled to multiple replicas behind a load balancer.
- **Cache:** Increase `CACHE_TTL` for restaurant data in high-traffic scenarios.
