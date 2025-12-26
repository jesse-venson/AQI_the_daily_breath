# The Daily Breath

**Air Quality Prediction and Health Risk Assessment System for Delhi, India**

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Overview

The Daily Breath is a machine learning-powered web application that provides real-time Air Quality Index (AQI) predictions and personalized health risk assessments for Delhi. The application features a unique newspaper-themed interface that presents critical air quality data in an engaging, accessible format.

## Features

- **Real-Time AQI Prediction**: Machine learning model trained on historical pollution data provides current AQI estimates
- **Personalized Health Risk Analysis**: Tailored health risk assessments based on user demographics (age, gender, parent status)
- **Comprehensive Pollutant Tracking**: Monitors PM2.5, PM10, NO₂, SO₂, CO, and O₃ levels
- **Weather Integration**: Live weather data from OpenWeatherMap API
- **Health Recommendations**: Actionable advice based on current air quality conditions
- **Responsive Design**: Newspaper-themed UI optimized for all devices

## Technology Stack

### Backend
- **Framework**: Flask 3.0.0
- **Machine Learning**:
  - Random Forest (AQI Prediction)
  - XGBoost (Health Risk Classification)
  - scikit-learn 1.4.0+
- **APIs**: OpenWeatherMap Air Pollution API
- **Deployment**: Railway (Python 3.13)

### Frontend
- **Core**: Vanilla JavaScript, HTML5, CSS3
- **Design**: Custom newspaper-themed responsive layout
- **Deployment**: Vercel

## System Architecture

```
┌─────────────┐      HTTPS      ┌──────────────┐
│   Vercel    │ ◄────────────► │   Railway    │
│  (Frontend) │                 │  (Backend)   │
└─────────────┘                 └──────────────┘
                                       │
                                       ▼
                                ┌──────────────┐
                                │ OpenWeather  │
                                │     API      │
                                └──────────────┘
```

## Live Application

- **Frontend**: https://aqi-the-daily-breath-delhi.vercel.app
- **Backend API**: https://aqithedailybreath-production.up.railway.app

## Machine Learning Models

### AQI Prediction Model
- **Algorithm**: Random Forest Regressor
- **Features**: PM2.5, PM10, NO₂, SO₂, CO, O₃, temperature, humidity, pressure, wind speed, temporal features
- **Performance**: Trained on historical Delhi pollution data

### Health Risk Model
- **Algorithm**: XGBoost Classifier
- **Features**: Age, AQI category, gender, income level, parent status, concern level
- **Predictions**: 8 health risk categories including respiratory symptoms, cardiovascular effects, and eye irritation

## API Endpoints

### `POST /predict`
Generates AQI prediction and health risk assessment

**Request Body:**
```json
{
  "age": 30,
  "gender_enc": 1,
  "parent_enc": 0
}
```

**Response:**
```json
{
  "aqi": 245,
  "pollutants": {...},
  "weather": {...},
  "health_risks": {...},
  "recommendations": "..."
}
```

### `GET /health`
Health check endpoint

## Data Sources

- **Air Pollution Data**: OpenWeatherMap Air Pollution API
- **Weather Data**: OpenWeatherMap Current Weather API
- **Training Data**: Historical Delhi AQI records

## Security

- Environment variables for sensitive data
- CORS enabled for secure cross-origin requests
- API key authentication for external services

## Performance

- **Frontend**: Static file serving via Vercel CDN
- **Backend**: Gunicorn WSGI server with 4 workers
- **Model Loading**: Pre-trained models cached in memory
- **Response Time**: < 2s for predictions

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Contributing

This project was developed as part of a Machine Learning course project.

## License

MIT License - See LICENSE file for details

## Acknowledgments

- OpenWeatherMap for providing air quality and weather data
- Delhi Pollution Control Committee for historical AQI data
- Machine Learning community for open-source libraries

---

**Developed with ❤️ for cleaner air in Delhi**

*Version 1.0.0 | © 2024 The Daily Breath*
