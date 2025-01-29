import pandas as pd

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
