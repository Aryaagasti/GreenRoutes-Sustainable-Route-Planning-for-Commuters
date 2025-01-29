import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import joblib

# Load dataset
data = pd.read_csv('backend/data.csv')

# Preprocess data
X = data[['traffic', 'weather', 'public_transport']]
y = data['carbon_emission']

# Convert categorical data to numeric
X = pd.get_dummies(X, columns=['weather'])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
predictions = model.predict(X_test)
mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')

# Save model
joblib.dump(model, 'backend/models/route_model.pkl')
