import tkinter as tk
import requests
import numpy as np
import pickle
from datetime import datetime
from recommend import recommend_for_high_pollution

def get_weather_and_pollution():
    API_KEY = "907734b8c2d588f413d73787458f3919"
    lat = "28.7041"
    lon = "77.1025"
    p_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    p_j = requests.get(p_url).json()

    # Check if API call was successful
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

def predict_aqi(model):
    d = get_weather_and_pollution()
    now = datetime.now()
    f = np.array([[
        d["PM25"], d["PM10"], d["O3"], d["NO2"], d["SO2"], d["CO"],
        d["temp"], d["humidity"], d["wind_speed"],
        0.0,  # precipitation (API doesn't provide)
        now.month, now.day, 0  # is_festive (simple version, always 0)
    ]])
    p = model.predict(f)[0]
    return p, d

def run_prediction():
    age = int(age_entry.get())
    p, d = predict_aqi(model)
    output_text.set(
        "PM2.5: " + str(d["PM25"]) + "\n" +
        "PM10: " + str(d["PM10"]) + "\n" +
        "NO2: " + str(d["NO2"]) + "\n" +
        "SO2: " + str(d["SO2"]) + "\n" +
        "CO: " + str(d["CO"]) + "\n" +
        "O3: " + str(d["O3"]) + "\n" +
        "Temp: " + str(d["temp"]) + "\n" +
        "Humidity: " + str(d["humidity"]) + "\n" +
        "Pressure: " + str(d["pressure"]) + "\n" +
        "Wind: " + str(d["wind_speed"]) + "\n\n" +
        "Predicted AQI: " + str(int(p)) + "\n\n" +
        recommend_for_high_pollution(age, p)
    )

model = pickle.load(open("aqi_model.pkl", "rb"))

root = tk.Tk()
root.title("Delhi AQI Predictor")

tk.Label(root, text="Enter Age:").pack()
age_entry = tk.Entry(root)
age_entry.pack()

tk.Button(root, text="Predict AQI", command=run_prediction).pack()

output_text = tk.StringVar()
tk.Label(root, textvariable=output_text, justify="left").pack()

root.mainloop()
