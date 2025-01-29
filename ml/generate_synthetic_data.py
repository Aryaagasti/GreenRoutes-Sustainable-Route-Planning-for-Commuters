import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# Function to generate random traffic data
def generate_traffic():
    return random.randint(50, 100)

# Function to generate random weather data
def generate_weather():
    weather_conditions = ['Clear', 'Cloudy', 'Rain']
    return random.choice(weather_conditions)

# Function to generate random public transportation usage
def generate_public_transport():
    return random.randint(50, 100)

# Function to calculate synthetic carbon emission based on other features
def calculate_carbon_emission(traffic, weather, public_transport):
    base_emission = 5.0
    traffic_factor = traffic / 100
    weather_factor = 1.2 if weather == 'Rain' else 1.0
    public_transport_factor = (100 - public_transport) / 100
    return round(base_emission * traffic_factor * weather_factor * public_transport_factor, 2)

# Generate synthetic data
def generate_synthetic_data(num_days=30):
    data = []
    start_date = datetime.now() - timedelta(days=num_days)
    
    for i in range(num_days):
        date = (start_date + timedelta(days=i)).strftime('%Y-%m-%d')
        traffic = generate_traffic()
        weather = generate_weather()
        public_transport = generate_public_transport()
        carbon_emission = calculate_carbon_emission(traffic, weather, public_transport)
        
        data.append([date, traffic, weather, public_transport, carbon_emission])
    
    df = pd.DataFrame(data, columns=['date', 'traffic', 'weather', 'public_transport', 'carbon_emission'])
    df.to_csv('backend/data.csv', index=False)

# Generate data for 30 days
generate_synthetic_data(30)
