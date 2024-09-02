import pandas as pd
import numpy as np
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

# Load the data
file_path = 'medicine_consumption_3years.csv'
data = pd.read_csv(file_path)

print(data.head())

# Convert 'Year' to numeric
data['Year'] = pd.to_numeric(data['Year'])

# Map seasons to numeric values
season_mapping = {season: idx+1 for idx, season in enumerate(data['Season'].unique())}
data['Season_num'] = data['Season'].map(season_mapping)

# Prepare the data for polynomial regression
X = data[['Year', 'Season_num']]
y = data['Medicine_Consumption']

# Polynomial regression model
polynomial_features = PolynomialFeatures(degree=3)  # Adjust the degree as needed
model = make_pipeline(polynomial_features, LinearRegression())
model.fit(X, y)

# Predict for the next 3 years
future_years = [2024, 2025, 2026]
future_data = []

for medicine in data['Medicine'].unique():
    for season in data['Season'].unique():
        for year in future_years:
            # Create a DataFrame for prediction
            X_future = pd.DataFrame({
                'Year': [year],
                'Season_num': [season_mapping[season]]
            })
            # Predict using the polynomial regression model
            predicted_consumption = model.predict(X_future)[0]
            future_data.append({
                'Medicine': medicine,
                'Season': season,
                'Year': year,
                'Predicted_Consumption': predicted_consumption
            })

# Convert to DataFrame
future_df = pd.DataFrame(future_data)

print("\nPredicted Medicine Consumption for the Next 3 Years:")
print(future_df)

# Save the predicted data to CSV
future_df.to_csv('predict.csv', index=False)

# Plotting
seasons = future_df['Season'].unique()
for season in seasons:
    plt.figure(figsize=(12, 8))
    
    season_data = future_df[future_df['Season'] == season]
    
    for medicine in season_data['Medicine'].unique():
        medicine_data = season_data[season_data['Medicine'] == medicine]
        plt.plot(medicine_data['Year'], medicine_data['Predicted_Consumption'], 
                 label=medicine, marker='o')

    plt.xlabel('Year')
    plt.ylabel('Predicted Consumption')
    plt.title(f'Predicted Medicinal Consumption in {season} for the Next 3 Years')
    plt.legend(loc='best')
    plt.grid(True)
    plt.savefig(f'predicted_medicine_consumption_{season}.png')
    plt.show()
