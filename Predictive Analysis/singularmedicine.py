import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

years = np.array([2021, 2022, 2023]).reshape(-1, 1)
consumption = np.array([670, 510, 598])

poly = PolynomialFeatures(degree=2) 
years_poly = poly.fit_transform(years)

model = LinearRegression()
model.fit(years_poly, consumption)

future_years = np.array([2024, 2025, 2026, 2027, 2028]).reshape(-1, 1)
future_years_poly = poly.transform(future_years)
predicted_consumption = model.predict(future_years_poly)

all_years = np.concatenate([years, future_years])
all_consumption = np.concatenate([consumption, predicted_consumption])

plt.figure(figsize=(10, 6))
plt.plot(years, consumption, label='Past Data', marker='o')
plt.plot(future_years, predicted_consumption, label='Predicted Data', marker='o', linestyle='--')
plt.plot(all_years, all_consumption, linestyle='-', color='gray', alpha=0.5)

plt.xlabel('Year')
plt.ylabel('Consumption')
plt.title('Medicine Consumption Prediction')
plt.legend()
plt.grid(True)
plt.show()
