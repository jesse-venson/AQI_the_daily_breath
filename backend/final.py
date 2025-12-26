import requests
import numpy as np
import pickle
from datetime import datetime
import os
from dotenv import load_dotenv
from recommend import recommend_for_high_pollution

# Load environment variables
load_dotenv()

def get_weather_and_pollution():
    API_KEY = os.getenv("OPENWEATHER_API_KEY")
    if not API_KEY:
        print("\nERROR: OPENWEATHER_API_KEY not set in environment variables")
        print("Please set the API key in .env.local or as an environment variable")
        exit(1)
    lat = "28.7041"
    lon = "77.1025"

    pollution_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    pol_json = requests.get(pollution_url).json()

    # Check if API call was successful
    if "list" not in pol_json:
        print("\nAPI Error Response:", pol_json)
        print("\nThe API key may be invalid or the request failed.")
        print("Please check your OpenWeatherMap API key and internet connection.")
        exit(1)

    comp = pol_json["list"][0]["components"]

    PM25 = comp["pm2_5"]
    PM10 = comp["pm10"]
    NO2  = comp["no2"]
    SO2  = comp["so2"]
    CO   = comp["co"]
    O3   = comp["o3"]

    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    weather_json = requests.get(weather_url).json()

    main = weather_json["main"]
    wind = weather_json["wind"]

    temp = main["temp"]
    humidity = main["humidity"]
    pressure = main["pressure"]
    wind_speed = wind["speed"]

    return {
        "PM25": PM25,
        "PM10": PM10,
        "NO2": NO2,
        "SO2": SO2,
        "CO": CO,
        "O3": O3,
        "temp": temp,
        "humidity": humidity,
        "pressure": pressure,
        "wind_speed": wind_speed
    }

def predict_aqi_from_api(model):
    data = get_weather_and_pollution()
    now = datetime.now()
    features = np.array([[
        data["PM25"], data["PM10"], data["O3"], data["NO2"], data["SO2"], data["CO"],
        data["temp"], data["humidity"], data["wind_speed"],
        0.0,  # precipitation (API doesn't provide)
        now.month, now.day, 0  # is_festive (simple version, always 0)
    ]])
    predicted_aqi = model.predict(features)[0]
    return predicted_aqi, data

if __name__ == "__main__":
    model = pickle.load(open("aqi_model.pkl", "rb"))
    age = int(input("Enter your age: "))

    predicted_aqi, weather_data = predict_aqi_from_api(model)

    print("PM2.5      :", weather_data["PM25"])
    print("PM10       :", weather_data["PM10"])
    print("NO2        :", weather_data["NO2"])
    print("SO2        :", weather_data["SO2"])
    print("CO         :", weather_data["CO"])
    print("O3         :", weather_data["O3"])
    print("Temperature:", weather_data["temp"])
    print("Humidity   :", weather_data["humidity"])
    print("Pressure   :", weather_data["pressure"])
    print("Wind Speed :", weather_data["wind_speed"])

    print("\nPredicted AQI:", predicted_aqi)

    reco = recommend_for_high_pollution(age, predicted_aqi)
    print(reco)
