import requests
from config import (
    NWS_BASE_URL, OPENWEATHER_BASE_URL, 
    NWS_USER_AGENT, OPENWEATHER_API_KEY,
    WEATHER_CONDITIONS
)
from models import WeatherData, ForecastData, WeatherResponse, WeatherCondition
import ssl
import certifi
from datetime import datetime
from typing import List
from cache_utils import coordinates_cache, weather_cache, forecast_cache


class WeatherService:
    def __init__(self):
        self.headers = {
            'User-Agent': NWS_USER_AGENT
        }
        # Create a session with SSL verification
        self.session = requests.Session()
        self.session.verify = certifi.where()
        
        if not OPENWEATHER_API_KEY:
            raise ValueError("OpenWeather API key not found in environment variables")

    def _is_us_location(self, lat: float, lon: float) -> bool:
        """Check if the coordinates are within the United States."""
        # Rough boundaries of the continental US
        return (24.396308 <= lat <= 49.384358 and 
                -125.000000 <= lon <= -66.934570)

    @coordinates_cache
    def _get_coordinates(self, location: str) -> tuple:
        """Convert location name to coordinates using OpenStreetMap Nominatim API."""
        try:
            # Format the location for the API
            formatted_location = location.replace(' ', '+')
            url = f"https://nominatim.openstreetmap.org/search?q={formatted_location}&format=json&limit=1"
            
            # Make the request with proper headers and SSL verification
            response = self.session.get(url, headers=self.headers)
            response.raise_for_status()
            
            data = response.json()
            if not data:
                raise ValueError(f"Could not find coordinates for {location}")
            
            return float(data[0]['lat']), float(data[0]['lon'])
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error getting coordinates: {str(e)}")

    def _map_weather_condition(self, condition: str) -> WeatherCondition:
        """Map API weather condition to our WeatherCondition enum."""
        condition = condition.lower()
        
        if any(word in condition for word in ['clear', 'sunny']):
            return WeatherCondition.SUNNY
        elif 'partly cloudy' in condition:
            return WeatherCondition.PARTLY_CLOUDY
        elif any(word in condition for word in ['cloudy', 'overcast']):
            return WeatherCondition.CLOUDY
        elif any(word in condition for word in ['rain', 'drizzle', 'shower']):
            return WeatherCondition.RAINY
        elif any(word in condition for word in ['snow', 'sleet', 'flurries']):
            return WeatherCondition.SNOWY
        elif any(word in condition for word in ['thunder', 'storm']):
            return WeatherCondition.THUNDERSTORM
        elif any(word in condition for word in ['fog', 'mist', 'haze']):
            return WeatherCondition.FOGGY
        elif any(word in condition for word in ['wind', 'breeze']):
            return WeatherCondition.WINDY
        else:
            return WeatherCondition.UNKNOWN

    @weather_cache
    def _get_nws_weather(self, lat: float, lon: float) -> WeatherData:
        """Get weather data from National Weather Service API."""
        try:
            points_url = f"{NWS_BASE_URL}/points/{lat},{lon}"
            response = self.session.get(points_url, headers=self.headers)
            response.raise_for_status()
            
            forecast_url = response.json()['properties']['forecast']
            response = self.session.get(forecast_url, headers=self.headers)
            response.raise_for_status()
            
            current = response.json()['properties']['periods'][0]
            return WeatherData(
                temperature=current['temperature'],
                conditions=self._map_weather_condition(current['shortForecast']),
                humidity=None,
                wind_speed=float(current['windSpeed'].split()[0]),
                description=current['detailedForecast']
            )
        except requests.exceptions.RequestException as e:
            if e.response and e.response.status_code == 404:
                raise ValueError("Location not supported by NWS API")
            raise Exception(f"Error fetching NWS weather data: {str(e)}")

    @weather_cache
    def _get_openweather_weather(self, location: str) -> WeatherData:
        """Get weather data from OpenWeatherMap API."""
        try:
            url = f"{OPENWEATHER_BASE_URL}/weather"
            params = {
                'q': location,
                'appid': OPENWEATHER_API_KEY,
                'units': 'imperial'  # Use Fahrenheit
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            return WeatherData(
                temperature=data['main']['temp'],
                conditions=self._map_weather_condition(data['weather'][0]['main']),
                humidity=data['main']['humidity'],
                wind_speed=data['wind']['speed'],
                description=data['weather'][0]['description']
            )
        except requests.exceptions.RequestException as e:
            if e.response and e.response.status_code == 404:
                raise ValueError(f"Could not find weather data for {location}")
            raise Exception(f"Error fetching OpenWeather data: {str(e)}")

    @weather_cache
    def get_current_weather(self, location: str) -> WeatherData:
        """Get current weather for a location."""
        try:
            # Get coordinates for the location
            lat, lon = self._get_coordinates(location)
            
            # Try NWS API first for US locations
            if self._is_us_location(lat, lon):
                try:
                    return self._get_nws_weather(lat, lon)
                except ValueError:
                    # If NWS fails, fall back to OpenWeatherMap
                    pass
            
            # Use OpenWeatherMap for non-US locations or if NWS fails
            return self._get_openweather_weather(location)
            
        except Exception as e:
            raise Exception(f"Error getting weather data: {str(e)}")

    @forecast_cache
    def get_forecast(self, location: str, days: int = 3) -> List[ForecastData]:
        """Get weather forecast for specified number of days."""
        try:
            # For now, we'll only use OpenWeatherMap for forecasts
            # as it's more reliable for global locations
            url = f"{OPENWEATHER_BASE_URL}/forecast"
            params = {
                'q': location,
                'appid': OPENWEATHER_API_KEY,
                'units': 'imperial',
                'cnt': days * 8  # Get data for every 3 hours
            }
            
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            forecast = []
            for item in data['list']:
                forecast.append(ForecastData(
                    date_time=datetime.strptime(item['dt_txt'], '%Y-%m-%d %H:%M:%S'),
                    temperature=item['main']['temp'],
                    conditions=self._map_weather_condition(item['weather'][0]['main']),
                    humidity=item['main']['humidity'],
                    wind_speed=item['wind']['speed'],
                    description=item['weather'][0]['description']
                ))
            
            return forecast
            
        except Exception as e:
            raise Exception(f"Error getting forecast data: {str(e)}") 