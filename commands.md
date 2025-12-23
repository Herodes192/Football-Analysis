# API Commands - Free API Live Football Data

## 🔑 API Keys (Automatic Fallback)

**Primary Key:** `ee524b1393msh0d80966992ba97ep11cf63jsn6686add35168`
**Backup Key:** `0783b704d5msh4c7f1c835680fccp1bdf77jsn28306145b1f3`

> ⚠️ The system automatically falls back to the backup key when the primary key hits rate limits (429) or auth errors.

---

## Countries

### Get All Countries
```bash
curl --request GET \
  --url https://free-api-live-football-data.p.rapidapi.com/football-get-all-countries \
  --header 'x-rapidapi-host: free-api-live-football-data.p.rapidapi.com' \
  --header 'x-rapidapi-key: ee524b1393msh0d80966992ba97ep11cf63jsn6686add35168'
```

---

## Seasons

### Get All Seasons
```bash
curl --request GET \
  --url https://free-api-live-football-data.p.rapidapi.com/football-get-all-seasons \
  --header 'x-rapidapi-host: free-api-live-football-data.p.rapidapi.com' \
  --header 'x-rapidapi-key: ee524b1393msh0d80966992ba97ep11cf63jsn6686add35168'
```

---

## Livescores

### Get Current Live Matches
```bash
curl --request GET \
  --url https://free-api-live-football-data.p.rapidapi.com/football-current-live \
  --header 'x-rapidapi-host: free-api-live-football-data.p.rapidapi.com' \
  --header 'x-rapidapi-key: ee524b1393msh0d80966992ba97ep11cf63jsn6686add35168'
```

---

## Fixtures

### Get Matches by Date
```bash
curl --request GET \
  --url 'https://free-api-live-football-data.p.rapidapi.com/football-get-matches-by-date?date=20241107' \
  --header 'x-rapidapi-host: free-api-live-football-data.p.rapidapi.com' \
  --header 'x-rapidapi-key: ee524b1393msh0d80966992ba97ep11cf63jsn6686add35168'
```

### Get All Matches by League ID (Liga Portugal = 61)
```bash
curl --request GET \
  --url 'https://free-api-live-football-data.p.rapidapi.com/football-get-all-matches-by-league?leagueid=61' \
  --header 'x-rapidapi-host: free-api-live-football-data.p.rapidapi.com' \
  --header 'x-rapidapi-key: ee524b1393msh0d80966992ba97ep11cf63jsn6686add35168'
```

---

## Leagues

### Get All Leagues
```bash
curl --request GET \
  --url https://free-api-live-football-data.p.rapidapi.com/football-get-all-leagues \
  --header 'x-rapidapi-host: free-api-live-football-data.p.rapidapi.com' \
  --header 'x-rapidapi-key: ee524b1393msh0d80966992ba97ep11cf63jsn6686add35168'
```

### Get League Detail by ID
```bash
curl --request GET \
  --url 'https://free-api-live-football-data.p.rapidapi.com/football-get-league-detail?leagueid=61' \
  --header 'x-rapidapi-host: free-api-live-football-data.p.rapidapi.com' \
  --header 'x-rapidapi-key: ee524b1393msh0d80966992ba97ep11cf63jsn6686add35168'
```

---

## Teams

### Get All Teams by League ID
```bash
curl --request GET \
  --url 'https://free-api-live-football-data.p.rapidapi.com/football-get-list-all-team?leagueid=61' \
  --header 'x-rapidapi-host: free-api-live-football-data.p.rapidapi.com' \
  --header 'x-rapidapi-key: ee524b1393msh0d80966992ba97ep11cf63jsn6686add35168'
```

### Get Team Detail by Team ID (Gil Vicente = 9764)
```bash
curl --request GET \
  --url 'https://free-api-live-football-data.p.rapidapi.com/football-league-team?teamid=9764' \
  --header 'x-rapidapi-host: free-api-live-football-data.p.rapidapi.com' \
  --header 'x-rapidapi-key: ee524b1393msh0d80966992ba97ep11cf63jsn6686add35168'
```

---

## Match Statistics

### Get Match All Stats by Event ID
```bash
curl --request GET \
  --url 'https://free-api-live-football-data.p.rapidapi.com/football-get-match-all-stats?eventid=4621624' \
  --header 'x-rapidapi-host: free-api-live-football-data.p.rapidapi.com' \
  --header 'x-rapidapi-key: ee524b1393msh0d80966992ba97ep11cf63jsn6686add35168'
```

### Get Match First Half Stats
```bash
curl --request GET \
  --url 'https://free-api-live-football-data.p.rapidapi.com/football-get-match-firstHalf-stats?eventid=4621624' \
  --header 'x-rapidapi-host: free-api-live-football-data.p.rapidapi.com' \
  --header 'x-rapidapi-key: ee524b1393msh0d80966992ba97ep11cf63jsn6686add35168'
```

---

## Standings

### Get Standing All by League ID
```bash
curl --request GET \
  --url 'https://free-api-live-football-data.p.rapidapi.com/football-get-standing-all?leagueid=61' \
  --header 'x-rapidapi-host: free-api-live-football-data.p.rapidapi.com' \
  --header 'x-rapidapi-key: ee524b1393msh0d80966992ba97ep11cf63jsn6686add35168'
```

---

## 🔄 Fallback Example

If primary key fails, use backup:

```bash
# Primary key hits 429 - Try backup
curl --request GET \
  --url 'https://free-api-live-football-data.p.rapidapi.com/football-get-all-matches-by-league?leagueid=61' \
  --header 'x-rapidapi-host: free-api-live-football-data.p.rapidapi.com' \
  --header 'x-rapidapi-key: 0783b704d5msh4c7f1c835680fccp1bdf77jsn28306145b1f3'
```

---

## 📝 Important IDs

- **Liga Portugal:** 61
- **Gil Vicente:** 9764
- **Arouca:** 158085

---

## ⚡ System Behavior

The backend automatically:
1. Tries PRIMARY key first
2. If 429/401/403 error → switches to BACKUP key
3. Logs which key is being used
4. Resets to PRIMARY every hour (configurable)

Check logs: `docker logs gil_vicente_backend --tail 50`
