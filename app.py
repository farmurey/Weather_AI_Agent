from flask import Flask, render_template, request, jsonify
from agent import WeatherAgent
from models import WeatherResponse
import json
from datetime import datetime

app = Flask(__name__)
agent = WeatherAgent()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_weather', methods=['POST'])
def get_weather():
    try:
        # Try to get location from JSON data first
        if request.is_json:
            location = request.json.get('location')
        else:
            # Fall back to form data
            location = request.form.get('location')
            
        if not location:
            return jsonify({'error': 'Location is required'}), 400

        response = agent.get_weather_and_activities(location)
        
        # Convert the Pydantic model to a dictionary
        response_dict = response.model_dump()
        
        # Convert datetime objects to strings
        for forecast in response_dict['forecast']:
            forecast['date_time'] = forecast['date_time'].strftime('%Y-%m-%d %H:%M:%S')
        
        return jsonify(response_dict)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True) 