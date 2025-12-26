# The Daily Breath — Delhi Air Quality Predictor

A machine learning-powered web application that predicts air quality index (AQI) for Delhi and provides personalized health risk assessments based on user demographics and real-time pollution data.

## Features

- **Real-time AQI Prediction**: Uses live OpenWeatherMap API data for accurate predictions
- **Personalized Health Assessment**: Predicts individual health risks including respiratory issues, cough, headache, and work/school absence
- **Multiple ML Models**:
  - **Random Forest**: For AQI prediction (13 features)
  - **XGBoost**: For health risk prediction (binary classifiers for 4 symptoms)
- **Vintage Newspaper UI**: Editorial-style interface with sepia tones and classic typography
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices
- **Age-Specific Recommendations**: Tailored advice based on user age groups

## Tech Stack

### Frontend
- **HTML5/CSS3/JavaScript** (Vanilla, no frameworks)
- **Vintage Typography**: UnifrakturMaguntia, Playfair Display, Crimson Pro
- **Responsive Design**: Mobile-first CSS with media queries

### Backend
- **Flask 3.0.0**: REST API server
- **Flask-CORS 4.0.0**: Cross-origin request handling
- **scikit-learn 1.3.2**: Random Forest AQI model
- **XGBoost 2.0.3**: Health risk prediction
- **NumPy/Pandas**: Data processing
- **Requests 2.31.0**: API calls to OpenWeatherMap

### ML Models
- **AQI Model** (aqi_model.pkl): Trained Random Forest Regressor
- **Health Risk Model** (health_risk_model.pkl): Trained XGBoost classifiers

## Project Structure

```
final week/
├── frontend/                    # Web Interface
│   ├── index.html              # Main HTML
│   ├── style.css               # Newspaper styling
│   ├── script.js               # Frontend logic
│   ├── config.js               # Environment configuration
│   └── README.md               # Frontend docs
├── backend/                     # REST API & ML
│   ├── api.py                  # Flask server
│   ├── final.py                # CLI application
│   ├── health_risk_predictor.py # Health risk models
│   ├── recommend.py            # Recommendations engine
│   ├── main.py                 # AQI model training
│   ├── requirements.txt        # Python dependencies
│   ├── Procfile                # Heroku deployment
│   ├── aqi_model.pkl           # Trained AQI model
│   ├── health_risk_model.pkl   # Trained health models
│   └── [data files]            # Training datasets
├── .gitignore                  # Git configuration
├── .env.example                # Environment template
├── .env.local                  # Dev environment (not in git)
├── .env.production             # Production template
├── vercel.json                 # Vercel deployment config
├── DEPLOYMENT.md               # Deployment guide
└── README.md                   # This file
```

## Quick Start

### Prerequisites
- Python 3.8+ (for backend)
- pip (Python package manager)
- Node.js (optional, for Vercel CLI)

### Local Development

1. **Clone and navigate**:
   ```bash
   cd "D:\5th sem\Machine learning\Project\final week"
   ```

2. **Set up environment**:
   ```bash
   # Copy template
   copy .env.example .env.local

   # Edit .env.local with your API key
   # OPENWEATHER_API_KEY=your_key_here
   ```

3. **Install backend dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

4. **Start backend** (Terminal 1):
   ```bash
   cd backend
   set OPENWEATHER_API_KEY=your_api_key_here
   python api.py
   # Server runs on http://localhost:5000
   ```

5. **Start frontend** (Terminal 2):
   ```bash
   cd frontend
   python -m http.server 8080
   # Open http://localhost:8080
   ```

### Using Batch Files (Windows)

```bash
# Terminal 1
START_BACKEND.bat

# Terminal 2
START_FRONTEND.bat
```

## API Usage

### Health Check
```bash
curl http://localhost:5000/health
```

### Predict AQI & Health Risks
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "age": 30,
    "gender_enc": 1,
    "parent_enc": 0
  }'
```

**Gender Encoding**:
- `0` = Female
- `1` = Male
- `2` = Other

**Parent Status**:
- `0` = No
- `1` = Yes

**Response**:
```json
{
  "aqi": 150,
  "pollutants": {
    "PM25": 95.5,
    "PM10": 235.2,
    "NO2": 120.3,
    "SO2": 45.2,
    "CO": 1500.0,
    "O3": 50.1
  },
  "weather": {
    "temp": 28.5,
    "humidity": 65,
    "pressure": 1013,
    "wind_speed": 3.2
  },
  "health_risks": {
    "respiratory_difficulties": {
      "probability": 0.75,
      "risk_level": "HIGH"
    },
    ...
  },
  "recommendations": "..."
}
```

## Environment Variables

### Required
- `OPENWEATHER_API_KEY`: OpenWeatherMap API key

### Optional
- `FLASK_ENV`: `development` or `production` (default: `development`)
- `FLASK_DEBUG`: `1` or `0` (default: `0`)
- `API_PORT`: Backend port (default: `5000`)
- `REACT_APP_API_URL`: Frontend API endpoint (default: `http://localhost:5000`)

Get a free API key: https://openweathermap.org/api

## Deployment

See [DEPLOYMENT.md](./DEPLOYMENT.md) for comprehensive deployment instructions.

### Quick Deploy to Vercel (Frontend)

```bash
npm install -g vercel
vercel
```

### Deploy Backend to Heroku

```bash
heroku login
cd backend
heroku create your-app-name
heroku config:set OPENWEATHER_API_KEY=your_key
git push heroku main
```

## ML Models Details

### AQI Prediction Model
- **Algorithm**: Random Forest Regressor
- **Input Features** (13):
  - PM2.5, PM10, O3, NO2, SO2, CO (pollutants)
  - Temperature, Humidity, Wind Speed (weather)
  - Precipitation, Month, Day, Festive Flag (temporal)
- **Output**: AQI value (0-500+)
- **Training Data**: Air pollution dataset with 1000+ samples

### Health Risk Models
- **Algorithm**: XGBoost Binary Classifiers (4 models)
- **Symptoms Predicted**:
  1. Respiratory difficulties
  2. Cough
  3. Headache
  4. Missed school/work days
- **Input Features** (6):
  - Age, AQI category, Gender, Income level, Parent status, Pollution concern
- **Output**: Probability (0-1) and Risk level (LOW/MODERATE/HIGH)

## Data Files

- `Cleaned_Air_Pollution.csv`: Preprocessed pollution dataset (1000+ samples)
- `Original_Dataset.csv`: Raw pollution data
- `health_risk_training.csv`: Health risk symptom data
- `pollutant_model_features.csv`: Feature matrix for AQI training

## AQI Categories

| AQI Range | Category | Description |
|-----------|----------|-------------|
| 0-50 | Good | Safe for all activities |
| 51-100 | Moderate | Acceptable air quality |
| 101-150 | Unhealthy for Sensitive Groups | Exercise caution |
| 151-200 | Unhealthy | Health effects for all |
| 201-300 | Very Unhealthy | Health alert |
| 300+ | Hazardous | Emergency conditions |

## Configuration Files

- **`.gitignore`**: Excludes environment files and dependencies
- **`vercel.json`**: Vercel deployment configuration
- **`.env.example`**: Template for environment variables
- **`.env.local`**: Development environment (not tracked)
- **`Procfile`**: Heroku deployment configuration

## Error Handling

### API Key Not Found
- Check `.env.local` file exists
- Verify `OPENWEATHER_API_KEY` is set
- Restart server after setting environment variable

### CORS Error
- Backend has CORS enabled for all origins in development
- For production, update CORS settings in `api.py`

### Connection Refused
- Ensure backend server is running on port 5000
- Check firewall settings
- Verify API URL in frontend config

## Performance Notes

- Frontend is vanilla JS (no build step needed)
- ML predictions take 1-2 seconds (includes API calls)
- Caching can be added for real-time data
- Consider rate limiting for production API

## Security Considerations

- API keys stored in environment variables only
- CORS configured for production domain
- Input validation on all API endpoints
- Error messages sanitized before sending to client

## Contributing

1. Create feature branch: `git checkout -b feature/feature-name`
2. Commit changes: `git commit -am 'Add feature'`
3. Push to branch: `git push origin feature/feature-name`
4. Submit pull request

## License

© 2024 The Daily Breath. All atmospheric rights reserved.

## Support

For issues or questions:
1. Check API response status
2. Verify environment variables
3. Test API endpoints directly
4. Check deployment logs

---

**Version**: 1.0.0
**Last Updated**: December 2024
**Maintained By**: ML Team
