import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

df = pd.read_csv('dolo_650_consumption_5years.csv')

season_mapping = {'Winter': 1, 'Spring': 2, 'Summer': 3, 'Fall': 4}
df['Season_num'] = df['Season'].map(season_mapping)

X = df[['Year', 'Season_num']]
y = df['Consumption']

polynomial_features = PolynomialFeatures(degree=3)
model = make_pipeline(polynomial_features, LinearRegression())
model.fit(X, y)

future_years = np.arange(2025, 2030)
future_seasons = np.array([1, 2, 3, 4] * 5).reshape(-1, 1)
future_X = np.column_stack((np.repeat(future_years, 4), future_seasons.flatten()))

future_predictions = model.predict(future_X)

current_data = df.copy()
current_data['Prediction'] = np.nan

future_data = pd.DataFrame({
    'Year': np.repeat(future_years, 4),
    'Season': ['Winter', 'Spring', 'Summer', 'Fall'] * 5,
    'Consumption': future_predictions,
    'Prediction': future_predictions
})

plot_data = pd.concat([current_data, future_data], ignore_index=True)

plt.figure(figsize=(14, 8))

for season in ['Winter', 'Spring', 'Summer', 'Fall']:
    season_data = plot_data[plot_data['Season'] == season]
    current = season_data[season_data['Prediction'].isna()]
    predicted = season_data[~season_data['Prediction'].isna()]

    plt.plot(current['Year'], current['Consumption'], marker='o', linestyle='-', label=f'Current {season}')
    plt.plot(predicted['Year'], predicted['Prediction'], marker='x', linestyle='--', label=f'Predicted {season}')

plt.xlabel('Year')
plt.ylabel('Consumption')
plt.title('Current and Predicted Dolo 650mg Consumption by Season')
plt.legend(title='Season and Type')
plt.grid(True)
plt.show()
