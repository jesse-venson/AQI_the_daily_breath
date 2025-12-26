from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import numpy as np
import requests
from datetime import datetime
import os
from dotenv import load_dotenv
from health_risk_predictor import predict_health_risks
from recommend import recommend_for_high_pollution
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="../.env.local")


# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

aqi_model = pickle.load(open("aqi_model.pkl", "rb"))
health_model = pickle.load(open("health_risk_model.pkl", "rb"))

def get_weather_and_pollution():
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    if not API_KEY:
        raise Exception("OPENWEATHER_API_KEY not set in environment variables")
    lat = "28.7041"
    lon = "77.1025"

    p_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    p_j = requests.get(p_url).json()

    if "list" not in p_j:
        raise Exception(f"API Error: {p_j.get('message', 'Unknown error')}")

    c = p_j["list"][0]["components"]

    w_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    w_j = requests.get(w_url).json()
    m = w_j["main"]
    wd = w_j["wind"]

    return {
        "PM25": c["pm2_5"],
        "PM10": c["pm10"],
        "NO2": c["no2"],
        "SO2": c["so2"],
        "CO": c["co"],
        "O3": c["o3"],
        "temp": m["temp"],
        "humidity": m["humidity"],
        "pressure": m["pressure"],
        "wind_speed": wd["speed"]
    }

def predict_aqi(model, data):
    now = datetime.now()
    features = np.array([[
        data["PM25"], data["PM10"], data["O3"], data["NO2"], data["SO2"], data["CO"],
        data["temp"], data["humidity"], data["wind_speed"],
        0.0,
        now.month, now.day, 0
    ]])
    return model.predict(features)[0]

@app.route('/predict', methods=['POST'])
def predict():
    try:
        age = request.json.get('age')
        gender_enc = request.json.get('gender_enc')
        parent_enc = request.json.get('parent_enc')

        if not age or age < 1 or age > 120:
            return jsonify({'error': 'Invalid age. Must be between 1 and 120'}), 400

        if gender_enc is None or gender_enc not in [0, 1, 2]:
            return jsonify({'error': 'Invalid gender. Must be 0 (Female), 1 (Male), or 2 (Other)'}), 400

        if parent_enc is None or parent_enc not in [0, 1]:
            return jsonify({'error': 'Invalid parent status. Must be 0 (No) or 1 (Yes)'}), 400

        weather_data = get_weather_and_pollution()
        predicted_aqi = predict_aqi(aqi_model, weather_data)
        health_risks = predict_health_risks(age, predicted_aqi, gender_enc, parent_enc, health_model)
        recommendations = recommend_for_high_pollution(age, predicted_aqi)

        return jsonify({
            'aqi': int(predicted_aqi),
            'pollutants': {
                'PM25': round(weather_data['PM25'], 2),
                'PM10': round(weather_data['PM10'], 2),
                'NO2': round(weather_data['NO2'], 2),
                'SO2': round(weather_data['SO2'], 2),
                'CO': round(weather_data['CO'], 2),
                'O3': round(weather_data['O3'], 2)
            },
            'weather': {
                'temp': round(weather_data['temp'], 1),
                'humidity': weather_data['humidity'],
                'pressure': weather_data['pressure'],
                'wind_speed': round(weather_data['wind_speed'], 1)
            },
            'health_risks': health_risks,
            'recommendations': recommendations
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok', 'message': 'Delhi AQI Predictor API is running'})

if __name__ == '__main__':
    print("Starting Delhi AQI Predictor API...")
    print("API will be available at: http://localhost:5000")
    app.run(debug=True, port=5000)
