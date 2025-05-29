import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
if not OPENWEATHER_API_KEY:
    print("Warning: OPENWEATHER_API_KEY not found in .env file")
else:
    print("OpenWeatherMap API key loaded successfully")

# API Endpoints
NWS_BASE_URL = "https://api.weather.gov"
OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
NWS_USER_AGENT = "WeatherActivityAgent/1.0 (your@email.com)"  # Replace with your email

# Temperature thresholds (in Fahrenheit)
TEMP_THRESHOLDS = {
    'COLD': 50,
    'COOL': 70,
    'WARM': 70
}

# Weather condition mappings
WEATHER_CONDITIONS = {
    'Clear': 'sunny',
    'Mostly Clear': 'sunny',
    'Partly Cloudy': 'cloudy',
    'Mostly Cloudy': 'cloudy',
    'Cloudy': 'cloudy',
    'Rain': 'rainy',
    'Rain Showers': 'rainy',
    'Snow': 'snowy',
    'Thunderstorm': 'stormy',
    'Drizzle': 'rainy',
    'Fog': 'foggy',
    'Mist': 'foggy',
    # OpenWeatherMap conditions
    'clear sky': 'sunny',
    'few clouds': 'cloudy',
    'scattered clouds': 'cloudy',
    'broken clouds': 'cloudy',
    'shower rain': 'rainy',
    'rain': 'rainy',
    'thunderstorm': 'stormy',
    'snow': 'snowy',
    'mist': 'foggy'
} 