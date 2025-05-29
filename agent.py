from weather_service import WeatherService
from models import WeatherData, ForecastData, WeatherResponse, WeatherCondition
from typing import List, Dict
import random

class WeatherAgent:
    def __init__(self):
        self.weather_service = WeatherService()
        self.activities = {
            WeatherCondition.SUNNY: [
                'Go for a hike',
                'Have a picnic',
                'Visit a beach',
                'Play outdoor sports',
                'Go cycling',
                'Visit a botanical garden',
                'Have a barbecue',
                'Go bird watching'
            ],
            WeatherCondition.RAINY: [
                'Visit a museum',
                'Watch a movie',
                'Go shopping',
                'Visit a library',
                'Cook a new recipe',
                'Play board games',
                'Visit an indoor pool',
                'Go to a café'
            ],
            WeatherCondition.SNOWY: [
                'Build a snowman',
                'Go sledding',
                'Have a snowball fight',
                'Go skiing',
                'Make snow angels',
                'Visit a winter market',
                'Go ice skating',
                'Have a hot chocolate'
            ],
            WeatherCondition.CLOUDY: [
                'Go for a walk',
                'Visit a local market',
                'Take photos',
                'Visit a park',
                'Go window shopping',
                'Visit a local attraction',
                'Have a coffee date',
                'Go to a farmers market'
            ],
            WeatherCondition.PARTLY_CLOUDY: [
                'Go for a walk',
                'Visit a local market',
                'Take photos',
                'Visit a park',
                'Go window shopping',
                'Visit a local attraction',
                'Have a coffee date',
                'Go to a farmers market'
            ],
            WeatherCondition.THUNDERSTORM: [
                'Stay indoors',
                'Watch a movie',
                'Read a book',
                'Play board games',
                'Cook a meal',
                'Work on a hobby',
                'Listen to music',
                'Take a nap'
            ],
            WeatherCondition.FOGGY: [
                'Visit a museum',
                'Go shopping',
                'Visit a café',
                'Go to a library',
                'Watch a movie',
                'Visit an indoor attraction',
                'Go to a spa',
                'Have a coffee date'
            ],
            WeatherCondition.WINDY: [
                'Go kite flying',
                'Visit a wind farm',
                'Go sailing',
                'Take photos of clouds',
                'Visit a museum',
                'Go shopping',
                'Visit a café',
                'Go to a library'
            ],
            WeatherCondition.UNKNOWN: [
                'Visit a museum',
                'Go shopping',
                'Visit a café',
                'Go to a library',
                'Watch a movie',
                'Visit an indoor attraction',
                'Go to a spa',
                'Have a coffee date'
            ]
        }

    def _get_weather_condition(self, weather_data: WeatherData) -> str:
        """Determine the weather condition based on the weather data."""
        conditions = weather_data.conditions.lower()
        if 'rain' in conditions or 'drizzle' in conditions:
            return 'rainy'
        elif 'snow' in conditions or 'sleet' in conditions:
            return 'snowy'
        elif 'cloud' in conditions or 'overcast' in conditions:
            return 'cloudy'
        else:
            return 'sunny'

    def _suggest_activities(self, weather_data: WeatherData) -> List[str]:
        """Suggest activities based on weather conditions."""
        return random.sample(self.activities[weather_data.conditions], 3)

    def get_weather_and_activities(self, location: str) -> WeatherResponse:
        """Get weather data and suggest activities for a location."""
        try:
            # Get current weather
            current_weather = self.weather_service.get_current_weather(location)
            
            # Get forecast
            forecast = self.weather_service.get_forecast(location)
            
            # Suggest activities
            suggested_activities = self._suggest_activities(current_weather)
            
            return WeatherResponse(
                location=location,
                current_weather=current_weather,
                forecast=forecast,
                suggested_activities=suggested_activities
            )
            
        except Exception as e:
            raise Exception(f"Error getting weather and activities: {str(e)}")

    def format_response(self, response: WeatherResponse) -> str:
        """Format the response in a user-friendly way."""
        weather = response.current_weather
        activities = response.suggested_activities
        
        formatted = f"""
Weather in {response.location}:
Temperature: {weather.temperature:.1f}°F
Conditions: {weather.conditions.value}
Humidity: {weather.humidity}%
Wind Speed: {weather.wind_speed} m/s

Suggested Activities:
{chr(10).join(f'- {activity}' for activity in activities)}
"""
        return formatted
