import pandas as pd
import requests
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS

# Your Google Gemini API key
GEMINI_API_KEY = 'AIzaSyDFOCRlZ0LeO7cdR77oNUg9k-mNL0BvwRs'

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Load the dataset
df = pd.read_csv('backend/data.csv')

def calculate_route(input_data, df):
    start = input_data['start']
    end = input_data['end']
    travel_date = pd.to_datetime(input_data.get('date', pd.to_datetime('today').strftime('%Y-%m-%d')))

    # Find the closest date in the dataset to the travel date
    df['date'] = pd.to_datetime(df['date'])
    closest_date = df.iloc[(df['date'] - travel_date).abs().argsort()[:1]]

    # Extract relevant data
    traffic = int(closest_date['traffic'].values[0])
    weather = closest_date['weather'].values[0]
    public_transport = int(closest_date['public_transport'].values[0])
    carbon_emission = float(closest_date['carbon_emission'].values[0])

    # Generate a suggestion based on traffic, weather, and public transport
    if traffic > 80:
        suggestion = 'Traffic is heavy. Consider using public transportation.'
    elif weather == 'Rain':
        suggestion = 'It\'s rainy. Drive carefully or consider staying indoors.'
    elif public_transport > 80:
        suggestion = 'Public transport is highly available. Consider using it.'
    else:
        suggestion = 'Conditions are good for driving. Enjoy your trip!'

    # Create the route dictionary
    route = {
        'start': start,
        'end': end,
        'distance': f'{traffic} km',
        'suggestion': suggestion,
        'weather': weather,
        'public_transport': public_transport,
        'carbon_emission': carbon_emission
    }

    return route

def generate_input_text(input_data, df):
    travel_date = pd.to_datetime(input_data.get('date', pd.to_datetime('today').strftime('%Y-%m-%d')))

    # Find the closest date in the dataset to the travel date
    df['date'] = pd.to_datetime(df['date'])
    closest_date = df.iloc[(df['date'] - travel_date).abs().argsort()[:1]]

    # Extract relevant data
    traffic = int(closest_date['traffic'].values[0])
    weather = closest_date['weather'].values[0]
    public_transport = int(closest_date['public_transport'].values[0])
    carbon_emission = float(closest_date['carbon_emission'].values[0])

    input_text = f"On {closest_date['date'].values[0]}, the weather is {weather}. Traffic is at {traffic}%, and public transportation availability is {public_transport}%. Carbon emission is measured at {carbon_emission} kg CO2."

    return input_text

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/route_planner')
def route_planner():
    return render_template('route_planner.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/visualization_insights')
def visualization_insights():
    return render_template('visualization_insights.html')

@app.route('/route', methods=['POST'])
def get_route():
    data = request.json
    route = calculate_route(data, df)
    return jsonify(route)

@app.route('/generate_ai', methods=['POST'])
def generate_ai():
    data = request.json
    input_text = generate_input_text(data, df)  # Generate input text based on dataset
    response = requests.post(
        f'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}',
        headers={'Content-Type': 'application/json'},
        json={
            'contents': [{
                'parts': [{'text': input_text}]
            }]
        }
    )
    
    # Debug the response
    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

    if response.status_code == 200:
        return jsonify(response.json())
    else:
        return jsonify({"error": "Failed to generate AI content"}), 500

if __name__ == '__main__':
    app.run(debug=True)
