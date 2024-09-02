import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

file_path = 'medicine_consumption_3years.csv'
data = pd.read_csv(file_path)

print(data.head())

data['Year'] = pd.to_numeric(data['Year'])

season_mapping = {season: idx+1 for idx, season in enumerate(data['Season'].unique())}
data['Season_num'] = data['Season'].map(season_mapping)

X = data[['Year', 'Season_num']]
y = data['Medicine_Consumption']

degree = 45
polynomial_features = PolynomialFeatures(degree=degree)
model = make_pipeline(polynomial_features, LinearRegression())
model.fit(X, y)

future_years = [2024, 2025, 2026]
future_seasons = ['Winter', 'Spring', 'Summer', 'Fall']
future_data = []

for medicine in data['Medicine'].unique():
    for season in future_seasons:
        for year in future_years:
            X_future = pd.DataFrame({
                'Year': [year],
                'Season_num': [season_mapping[season]]
            })
            predicted_consumption = model.predict(X_future)[0]
            future_data.append({
                'Medicine': medicine,
                'Season': season,
                'Year': year,
                'Predicted_Consumption': predicted_consumption
            })
            
future_df = pd.DataFrame(future_data)

combined_df = pd.concat([data[['Year', 'Season', 'Medicine', 'Medicine_Consumption']], 
                         future_df[['Year', 'Season', 'Medicine', 'Predicted_Consumption']]], 
                         ignore_index=True, sort=False)
combined_df = combined_df.melt(id_vars=['Year', 'Season', 'Medicine'], value_vars=['Medicine_Consumption', 'Predicted_Consumption'],
                               var_name='Consumption_Type', value_name='Consumption')

for medicine in combined_df['Medicine'].unique():
    plt.figure(figsize=(14, 8))
    subset = combined_df[combined_df['Medicine'] == medicine]
    for season in subset['Season'].unique():
        season_data = subset[subset['Season'] == season]
        plt.plot(season_data[season_data['Consumption_Type'] == 'Medicine_Consumption']['Year'],
                 season_data[season_data['Consumption_Type'] == 'Medicine_Consumption']['Consumption'],
                 label=f'{season} - Current', linestyle='-', marker='o')
        plt.plot(season_data[season_data['Consumption_Type'] == 'Predicted_Consumption']['Year'],
                 season_data[season_data['Consumption_Type'] == 'Predicted_Consumption']['Consumption'],
                 label=f'{season} - Predicted', linestyle='--', marker='x')

    plt.xlabel('Year')
    plt.ylabel('Consumption')
    plt.title(f'current vs predicted consumption for {medicine}')
    plt.legend(title='Season')
    plt.grid(True)
    plt.savefig(f'{medicine}.png')
    plt.show()

print("Graphs saved as separate images for each medicine.")
