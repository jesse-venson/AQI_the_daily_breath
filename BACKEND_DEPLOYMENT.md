# Backend Deployment Guide

Deploy your Flask API to production. Choose one of these platforms:

## Option 1: Railway.app (Recommended - Easiest)

### Step 1: Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Click "Login with GitHub"
3. Authorize Railway to access your repositories

### Step 2: Deploy Backend
1. Click "New Project"
2. Select "Deploy from GitHub"
3. Choose your repository: `AQI_the_daily_breath`
4. Railway will auto-detect the Python project
5. Set root directory to `backend/` (if needed)

### Step 3: Configure Environment Variables
1. Go to "Variables" tab
2. Add:
   ```
   OPENWEATHER_API_KEY = 907734b8c2d588f413d73787458f3919
   FLASK_ENV = production
   FLASK_DEBUG = 0
   ```
3. Deploy

### Step 4: Get Your Backend URL
- Railway assigns a URL automatically (e.g., `https://aqi-backend-prod.railway.app`)
- Copy this URL

### Step 5: Update Frontend
Update your frontend to use this URL:

**Option A: Update config.js directly**
```javascript
// frontend/config.js
const config = {
    API_URL: 'https://your-railway-url.railway.app',
    // ...
};
```

**Option B: Set Vercel environment variable**
1. Go to Vercel Dashboard
2. Project Settings → Environment Variables
3. Add: `REACT_APP_API_URL = https://your-railway-url.railway.app`
4. Redeploy

---

## Option 2: Render.com

### Step 1: Create Render Account
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Authorize Render

### Step 2: Deploy
1. Click "New +"
2. Select "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `aqi-backend` (or any name)
   - **Root Directory**: `backend`
   - **Runtime**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT api:app`
   - **Plan**: Free tier available

### Step 3: Add Environment Variables
1. Go to "Environment" tab
2. Add:
   ```
   OPENWEATHER_API_KEY=907734b8c2d588f413d73787458f3919
   FLASK_ENV=production
   FLASK_DEBUG=0
   ```

### Step 4: Deploy
- Click "Create Web Service"
- Wait for deployment (2-3 minutes)
- Get your URL (e.g., `https://aqi-backend.onrender.com`)

### Step 5: Update Frontend
Follow same steps as Railway (Option A or B above)

---

## Option 3: Heroku (Legacy - Paid Tier)

*Note: Heroku free tier was discontinued. Minimum $5/month.*

If you still want to use Heroku:

### Step 1: Install Heroku CLI
```bash
npm install -g heroku
# or download from heroku.com/download
```

### Step 2: Login
```bash
heroku login
```

### Step 3: Create App
```bash
cd backend
heroku create your-app-name
```

### Step 4: Set Environment Variables
```bash
heroku config:set OPENWEATHER_API_KEY=907734b8c2d588f413d73787458f3919
heroku config:set FLASK_ENV=production
heroku config:set FLASK_DEBUG=0
```

### Step 5: Deploy
```bash
git push heroku main
```

### Step 6: Check Logs
```bash
heroku logs --tail
```

### Step 7: Get URL
```bash
heroku apps:info
```

---

## Recommended Approach: Railway + Vercel

**Most seamless integration:**

1. Deploy backend to Railway.app
2. Deploy frontend to Vercel (already done)
3. Connect them via environment variable

### Complete Workflow

```bash
# Backend on Railway
# 1. Push to GitHub (already done)
# 2. Go to railway.app → Deploy from GitHub
# 3. Get URL (e.g., https://aqi-backend-prod.railway.app)

# Frontend on Vercel
# 1. Go to Vercel Dashboard
# 2. Project Settings → Environment Variables
# 3. Add: REACT_APP_API_URL = https://aqi-backend-prod.railway.app
# 4. Redeploy
```

---

## Verify Deployment

Once deployed, test your backend:

### Test Health Check
```bash
curl https://your-backend-url/health
```

Expected response:
```json
{"status": "ok", "message": "Delhi AQI Predictor API is running"}
```

### Test Prediction Endpoint
```bash
curl -X POST https://your-backend-url/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 30, "gender_enc": 1, "parent_enc": 0}'
```

Expected response includes AQI, pollutants, weather, health risks, recommendations.

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
- Platform didn't install requirements
- Check `requirements.txt` is in correct directory
- Verify platform's build command runs `pip install -r requirements.txt`

### "OPENWEATHER_API_KEY not set"
- Environment variable not added to platform
- Check spelling (case-sensitive)
- Restart deployment after adding

### "Port 5000 already in use"
- Platform uses dynamic port (set via `$PORT` environment variable)
- Procfile/start command already handles this

### "Models not loading" (ImportError)
- `.pkl` files not in repository
- Check files are committed to GitHub
- Use `git lfs` if files > 100MB

### "Connection refused" on frontend
- Backend URL not updated in frontend
- Check `REACT_APP_API_URL` is set correctly
- Verify backend is actually deployed and running

---

## Cost Comparison

| Platform | Free Tier | Startup Time | Sleep Time |
|----------|-----------|--------------|-----------|
| **Railway** | $5 credit/month | Instant | Never sleeps |
| **Render** | Free (with limits) | ~30s | Spins down after 15min |
| **Heroku** | Discontinued | Instant | No free tier |

**Recommendation**: Use Railway for best experience.

---

## Next Steps

1. Choose Railway or Render
2. Deploy your backend
3. Get the backend URL
4. Update Vercel environment variable
5. Test full application flow

Your live app will be at: `https://aqi-the-daily-breath.vercel.app` (or your custom domain)

---

**Backend Status: Ready to Deploy! 🚀**
