# Delhi AQI Predictor - Frontend

Modern web interface for the Delhi AQI Prediction system.

## Quick Start

### 1. Start the Backend Server

Open a terminal and run:
```bash
cd backend
pip install -r requirements.txt
python api.py
```

The API will start at `http://localhost:5000`

### 2. Start the Frontend

Open another terminal and run:
```bash
cd frontend
python -m http.server 8080
```

Or use VS Code Live Server extension (right-click `index.html` → Open with Live Server)

### 3. Open in Browser

Navigate to `http://localhost:8080`

## Features

- Real-time AQI prediction for Delhi
- Personalized health risk assessment (4 symptoms)
- Age-specific recommendations
- Clean, modern UI with color-coded AQI levels
- Mobile-responsive design

## Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Backend**: Flask REST API
- **ML Models**: Random Forest (AQI) + XGBoost (Health Risks)

## Usage

1. Enter your age (1-120)
2. Click "Predict AQI & Health Risks"
3. View results:
   - Current AQI level (color-coded)
   - Pollution levels (PM2.5, PM10, etc.)
   - Weather conditions
   - Health risk assessment
   - Personalized recommendations

## Troubleshooting

**"Error: Failed to fetch"**
- Make sure backend server is running at `http://localhost:5000`
- Check that you installed dependencies: `pip install -r requirements.txt`

**API returns error**
- Check your internet connection (needs OpenWeatherMap API access)
- Verify API key in `backend/api.py` is valid

## File Structure

```
frontend/
├── index.html      # Main page structure
├── style.css       # Styling and layout
├── script.js       # API calls and UI logic
└── README.md       # This file
```

## API Endpoint

**POST** `http://localhost:5000/predict`

Request body:
```json
{
  "age": 35
}
```

Response:
```json
{
  "aqi": 198,
  "pollutants": { "PM25": 85.3, ... },
  "weather": { "temp": 28.5, ... },
  "health_risks": {
    "Respiratory_difficulties": { "probability": 0.14, "risk_level": "LOW" },
    ...
  },
  "recommendations": "..."
}
```

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

Built with ❤️ for Machine Learning coursework
