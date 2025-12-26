import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

df = pd.read_csv('pollutant_model_features.csv')

features = ['temp', 'humidity', 'windspeedmean', 'month', 'is_festive']
X = df[features]
y = df['AQI']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(x_train, y_train)

pred = model.predict(x_test)

r2 = r2_score(y_test, pred)

n = x_test.shape[0]
p = x_test.shape[1]
adj_r2 = 1 - (1 - r2) * (n - 1) / (n - p - 1)

print("R² Score:", r2)
print("Adjusted R² Score:", adj_r2)
