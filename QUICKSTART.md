# Quick Start Guide

## Disclaimer / Aviso

**PT:** Este é um projeto **não oficial**, criado por um adepto. O **Gil Vicente FC** **não** solicitou, não aprovou/endossou, não está afiliado e **não** remunerou este trabalho.

**EN:** This is an **unofficial fan-made** project. **Gil Vicente FC** did **not** request or endorse it, is **not** affiliated with it, and **no** remuneration was provided.

## Gil Vicente Tactical Intelligence Platform

Get up and running in 5 minutes.

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

**Local Development:**
- **Frontend Dashboard**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

**Production:**
The platform is deployed and accessible online.

---

## Using the Platform

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

## Development Setup

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

# Run development server
npm run dev

# Build for production
npm run build
```

---

## API Quick Examples

### Get Upcoming Fixtures
```bash
curl http://localhost:8000/api/v1/fixtures/upcoming?limit=5
```

### Get Opponent Statistics
```bash
curl http://localhost:8000/api/v1/opponents/123/statistics
```

### Generate Tactical Analysis
```bash
curl -X POST http://localhost:8000/api/v1/tactical/analyze \
  -H "Content-Type: application/json" \
  -d @matches.json
```

---

## Key Features

**Opponent Tracking** - Automatically identify Gil Vicente's opponents  
**Tactical Analysis** - Analyze formations, playing style, strengths/weaknesses  
**Match Recommendations** - Get tactical suggestions for each match  
**Data Visualization** - Clear, actionable insights dashboard  
**API Integration** - Real-time football data from API-Football  

---

## Sample Workflow

1. **Check Upcoming Fixtures**
   - Navigate to Fixtures page
   - View Gil Vicente's next matches

2. **Select Opponent**
   - Click on opponent team
   - View recent match history

3. **Generate Analysis**
   - Click "Analyze Opponent"
   - Review tactical patterns
   - View formation tendencies

4. **Get Recommendations**
   - Request tactical brief
   - Review suggested formations
   - Export match preparation notes

---

## Troubleshooting

### Services won't start
```bash
# Check if ports are available
netstat -tulpn | grep -E '3000|8000|5432|6379'

# Check Docker logs
docker-compose logs -f
```

### API Key Issues
- Verify key is correct in .env
- Check API quota on RapidAPI dashboard
- Ensure no extra spaces in .env file

### Database Connection
```bash
# Check PostgreSQL is running
docker-compose ps

# Reset database
docker-compose down -v
docker-compose up -d
```

---

## Next Steps

- Review [API Documentation](docs/API_DOCUMENTATION.md)
- Explore [Tactical Features](TACTICAL_FEATURES.md)
- Check [Project Summary](PROJECT_SUMMARY.md)

---

## Ready to Analyze

You're all set! Start by viewing upcoming fixtures and analyzing your next opponent.

For detailed information, see the full README.md

---

**Built for Gil Vicente FC**
