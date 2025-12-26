import tkinter as tk
import requests
import numpy as np
import pickle
from datetime import datetime
from recommend import recommend_for_high_pollution, generate_advice_by_concern
from health_risk_predictor import predict_health_risks

def get_weather_and_pollution():
    API_KEY = "907734b8c2d588f413d73787458f3919"
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

def predict_aqi(model):
    d = get_weather_and_pollution()
    now = datetime.now()
    f = np.array([[
        d["PM25"], d["PM10"], d["O3"], d["NO2"], d["SO2"], d["CO"],
        d["temp"], d["humidity"], d["wind_speed"],
        0.0,
        now.month, now.day, 0
    ]])
    p = model.predict(f)[0]
    return p, d

def run_prediction():
    try:
        age = int(age_entry.get())
        concern = int(concern_slider.get())

        # Get AQI prediction
        p, d = predict_aqi(model)

        # Build basic output
        output = f"PM2.5: {d['PM25']}\n"
        output += f"PM10: {d['PM10']}\n"
        output += f"NO2: {d['NO2']}\n"
        output += f"Temperature: {d['temp']}\n"
        output += f"Humidity: {d['humidity']}\n\n"
        output += f"Predicted AQI: {int(p)}\n\n"

        # Health Risk Predictions (Model 2)
        try:
            health_risks = predict_health_risks(age, p)
            output += "--- Health Risk Assessment ---\n"

            for symptom, data in health_risks.items():
                display_name = symptom.replace('_', ' ').title()
                prob = data['probability']
                risk = data['risk_level']

                # Color-code risk levels with symbols
                if risk == "HIGH":
                    symbol = "[!!!]"
                elif risk == "MODERATE":
                    symbol = "[!!]"
                else:
                    symbol = "[!]"

                output += f"{display_name}: {symbol} {risk} ({prob:.0%})\n"

            output += "\n"
        except Exception as e:
            output += f"[Health risk model unavailable: {str(e)}]\n\n"

        # AQI-based recommendations
        output += recommend_for_high_pollution(age, p)

        # Add concern-based insights
        output += f"\n\n--- Your Concern Level: {concern}/10 ---\n"
        if concern < 4 and p > 200:
            output += "\n⚠️ WARNING: Air quality is actually UNHEALTHY, but your concern is low.\n"
            output += "You should take this seriously and follow the recommendations above!"
        elif concern > 7 and p < 100:
            output += "\n✅ Good news: Air quality is better than you think!\n"
            output += "Your concern is high, but today's air is moderate. You can relax a bit."

        # Additional personalized advice if they have health issues
        if has_respiratory.get():
            output += "\n\n🏥 RESPIRATORY HEALTH ALERT:\n"
            output += "- Keep your inhaler with you at all times\n"
            output += "- Avoid outdoor exercise completely\n"
            output += "- Use air purifier indoors if available"

        # Update Text widget
        output_text.delete(1.0, tk.END)
        output_text.insert(1.0, output)

    except ValueError:
        output_text.delete(1.0, tk.END)
        output_text.insert(1.0, "Please enter a valid age!")

# Load models
model = pickle.load(open("aqi_model.pkl", "rb"))

# Try to load health risk model (optional)
try:
    health_model = pickle.load(open("health_risk_model.pkl", "rb"))
    print("Health risk model loaded successfully!")
except FileNotFoundError:
    health_model = None
    print("Health risk model not found - will run without health predictions")

# Create GUI
root = tk.Tk()
root.title("Enhanced Delhi AQI Predictor")
root.geometry("600x700")

# Age input
tk.Label(root, text="Enter Age:", font=("Arial", 12)).pack(pady=5)
age_entry = tk.Entry(root, font=("Arial", 12))
age_entry.pack()

# Concern level slider
tk.Label(root, text="How concerned are you about air pollution? (0-10):", font=("Arial", 12)).pack(pady=10)
concern_slider = tk.Scale(root, from_=0, to=10, orient=tk.HORIZONTAL, length=300, font=("Arial", 10))
concern_slider.set(5)
concern_slider.pack()

# Health checkbox
has_respiratory = tk.BooleanVar()
tk.Checkbutton(root, text="I have respiratory difficulties (asthma, COPD, etc.)",
               variable=has_respiratory, font=("Arial", 10)).pack(pady=10)

# Predict button
tk.Button(root, text="Predict AQI & Get Recommendations",
          command=run_prediction, font=("Arial", 12), bg="#4CAF50", fg="white").pack(pady=10)

# Output area with scrollbar
output_frame = tk.Frame(root)
output_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

output_text = tk.Text(output_frame, height=20, width=70, font=("Courier", 10),
                      wrap=tk.WORD, yscrollcommand=scrollbar.set)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar.config(command=output_text.yview)

root.mainloop()
