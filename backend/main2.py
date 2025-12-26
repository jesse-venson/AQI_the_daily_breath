import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error


def adjusted_r2(r2, n, k):
    return 1 - ((1 - r2) * (n - 1)) / (n - k - 1)

df = pd.read_csv("pollutant_model_features.csv")

# Drop pollutant columns
pollutants = ['pm25', 'pm10', 'so2', 'co', 'no2', 'o3']
x = df.drop(['AQI', 'AQHI'] + pollutants, axis=1)

y_aqi = df['AQI']
y_aqhi = df['AQHI']

x_train, x_test, y_aqi_train, y_aqi_test = train_test_split(x, y_aqi, test_size=0.3, random_state=42)
X_train2, X_test2, y_aqhi_train, y_aqhi_test = train_test_split(x, y_aqhi, test_size=0.3, random_state=42)

# using random forest for aqi prediction
rf_aqi = RandomForestRegressor(n_estimators=1000, random_state=42)
rf_aqi.fit(x_train, y_aqi_train)
y_aqi_pred = rf_aqi.predict(x_test)

# using random forest for aqhi prediction
rf_aqhi = RandomForestRegressor(n_estimators=1000, random_state=42)
rf_aqhi.fit(X_train2, y_aqhi_train)
y_aqhi_pred = rf_aqhi.predict(X_test2)

# Evaluation AQI
print("AQI Prediction Results:")
r2_aqi = r2_score(y_aqi_test, y_aqi_pred)
adj_r2_aqi = adjusted_r2(r2_aqi, len(y_aqi_test), x_test.shape[1])
print("Adjusted R² value for AQI:", adj_r2_aqi)

# Evaluation AQHI
print("\nAQHI Prediction Results:")
print("R² Score:", r2_score(y_aqhi_test, y_aqhi_pred))
