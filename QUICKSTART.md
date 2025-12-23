# 🚀 Quick Start Guide

## Gil Vicente Tactical Intelligence Platform

Get up and running in 5 minutes!

---

## Prerequisites

- **Docker** & **Docker Compose** installed
- **Football API Key** from [API-Football via RapidAPI](https://rapidapi.com/api-sports/api/api-football)

---

## Installation Steps

### 1. Setup Environment

```bash
# Navigate to project directory
cd "Football Analysis"

# Copy environment template
cp .env.example .env

# Edit .env and add your API key
nano .env  # or use your preferred editor
```

**Required: Add your API key in .env:**
```env
FOOTBALL_API_KEY=your_api_key_here
```

### 2. Start Services

```bash
# Using the setup script (recommended)
./scripts/setup.sh

# OR manually with Docker Compose
docker-compose up -d
```

### 3. Access the Platform

- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📱 Using the Platform

### Dashboard
View upcoming matches, opponent tracking status, and recent activity.

### Fixtures
- View Gil Vicente's upcoming matches
- Check opponent details
- Schedule analysis

### Opponents
- Track opponent teams
- View match history
- Access statistics

### Tactical Analysis
- Generate opponent analysis
- Get tactical recommendations
- View match briefs

---

## 🔧 Development Setup

### Backend Development

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload
```

### Frontend Development

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

---

## 📊 API Quick Examples

### Get Upcoming Fixtures
```bash
curl http://localhost:8000/api/v1/fixtures/upcoming?limit=5
```

### Analyze Opponent
```bash
curl -X POST http://localhost:8000/api/v1/tactical/analyze \
  -H "Content-Type: application/json" \
  -d '[{"formation":"4-3-3","statistics":{"possession":55},"goals_scored":2,"goals_conceded":1,"result":"W","is_home":true}]'
```

### Get Match Brief
```bash
curl -X POST http://localhost:8000/api/v1/tactical/match-brief \
  -H "Content-Type: application/json" \
  -d '{"opponent_team_id":123,"matches":[...],"gil_vicente_formation":"4-3-3"}'
```

---

## 🛠️ Common Commands

### View Logs
```bash
docker-compose logs -f
docker-compose logs -f backend  # Specific service
```

### Restart Services
```bash
docker-compose restart
docker-compose restart backend  # Specific service
```

### Stop Services
```bash
docker-compose down
```

### Update Code
```bash
git pull
docker-compose up -d --build
```

---

## 📚 Documentation

- **[README.md](README.md)** - Full project documentation
- **[API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md)** - Complete API reference
- **[DEPLOYMENT.md](docs/DEPLOYMENT.md)** - Production deployment guide
- **[API Docs (Interactive)](http://localhost:8000/docs)** - Swagger UI

---

## 🎯 Key Features

✅ **Opponent Tracking** - Automatically identify Gil Vicente's opponents  
✅ **Tactical Analysis** - Analyze formations, playing style, strengths/weaknesses  
✅ **Match Recommendations** - Get tactical suggestions for each match  
✅ **Data Visualization** - Clear, actionable insights dashboard  
✅ **API Integration** - Real-time football data from API-Football  

---

## ⚽ Sample Workflow

1. **Check Upcoming Fixtures** → Dashboard or `/fixtures`
2. **Identify Next Opponent** → Note team ID
3. **Fetch Opponent Data** → API: `/opponents/{team_id}/matches`
4. **Analyze Tactics** → API: `/tactical/analyze`
5. **Generate Recommendations** → API: `/tactical/recommendations`
6. **Review Match Brief** → Dashboard or API response

---

## 🆘 Troubleshooting

### Services won't start
```bash
# Check if ports are available
netstat -tuln | grep -E '3000|8000|5432|6379'

# Check Docker status
docker ps -a
docker-compose ps
```

### API returns errors
```bash
# Verify environment variables
cat .env | grep FOOTBALL_API_KEY

# Check backend logs
docker-compose logs backend
```

### Database connection issues
```bash
# Restart database
docker-compose restart postgres

# Check database is ready
docker-compose exec postgres pg_isready
```

---

## 🔐 Security Notes

- Keep `.env` file private (never commit to git)
- Use strong passwords in production
- Enable SSL/TLS for production deployments
- Rotate API keys regularly
- Monitor API usage to avoid rate limits

---

## 📞 Need Help?

- Check logs: `docker-compose logs -f`
- Review API docs: http://localhost:8000/docs
- Check health endpoint: http://localhost:8000/api/v1/health

---

## ⚽ Ready to Analyze!

Your Gil Vicente Tactical Intelligence Platform is ready!

Start by accessing the dashboard at **http://localhost:3000**

---

**Built with ⚽ for Gil Vicente FC**
