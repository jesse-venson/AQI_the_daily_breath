import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv('pollutant_model_features.csv')

X = df[['temp', 'humidity', 'windspeedmean', 'month', 'is_festive']]
y = df['AQI']

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

rf = RandomForestRegressor(random_state=42)
rf.fit(x_train, y_train)
rf_pred = rf.predict(x_test)

lr = LinearRegression()
lr.fit(x_train, y_train)
lr_pred = lr.predict(x_test)

n = len(y_test)
p = X.shape[1]
r2_rf = r2_score(y_test, rf_pred)
r2_lr = r2_score(y_test, lr_pred)
adj_r2_rf = 1 - (1 - r2_rf) * (n - 1) / (n - p - 1)
adj_r2_lr = 1 - (1 - r2_lr) * (n - 1) / (n - p - 1)

plt.figure(figsize=(8,6))
plt.scatter(y_test, rf_pred, color='green', alpha=0.5, label='Random Forest')
plt.scatter(y_test, lr_pred, color='blue', alpha=0.5, label='Linear Regression')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
plt.xlabel('Actual AQI')
plt.ylabel('Predicted AQI')
plt.title('Actual vs Predicted AQI Comparison')
plt.legend()
plt.show()

plt.figure(figsize=(8,6))
plt.scatter(y_test, y_test - rf_pred, color='green', alpha=0.5, label='Random Forest Residuals')
plt.scatter(y_test, y_test - lr_pred, color='blue', alpha=0.5, label='Linear Regression Residuals')
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('Actual AQI')
plt.ylabel('Residuals')
plt.title('Residuals Comparison')
plt.legend()
plt.show()

models = ['Linear Regression', 'Random Forest']
r2_scores = [r2_lr, r2_rf]
adj_r2_scores = [adj_r2_lr, adj_r2_rf]
x = np.arange(len(models))
width = 0.35

plt.figure(figsize=(8,6))
plt.bar(x - width/2, r2_scores, width, label='R²')
plt.bar(x + width/2, adj_r2_scores, width, label='Adjusted R²')
plt.xticks(x, models)
plt.ylabel('Score')
plt.title('Model Performance Comparison')
plt.legend()
plt.show()

mse_linear = mean_squared_error(y_test, lr_pred)
mse_rf = mean_squared_error(y_test, rf_pred)

print("Linear Regression MSE:", mse_linear)
print("Random Forest MSE:", mse_rf)
