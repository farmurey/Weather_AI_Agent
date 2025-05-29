from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class WeatherCondition(str, Enum):
    """Enum for weather conditions."""
    CLEAR = "Clear"
    SUNNY = "Sunny"
    PARTLY_CLOUDY = "Partly Cloudy"
    CLOUDY = "Cloudy"
    RAINY = "Rainy"
    SNOWY = "Snowy"
    THUNDERSTORM = "Thunderstorm"
    FOGGY = "Foggy"
    WINDY = "Windy"
    UNKNOWN = "Unknown"

class WeatherData(BaseModel):
    """Model for current weather data."""
    temperature: float = Field(..., description="Temperature in Fahrenheit")
    conditions: WeatherCondition = Field(..., description="Weather conditions")
    humidity: Optional[float] = Field(None, description="Humidity percentage")
    wind_speed: float = Field(..., description="Wind speed")
    description: str = Field(..., description="Detailed weather description")

class ForecastData(BaseModel):
    """Model for forecast data."""
    date_time: datetime = Field(..., description="Date and time of the forecast")
    temperature: float = Field(..., description="Temperature in Fahrenheit")
    conditions: WeatherCondition = Field(..., description="Weather conditions")
    humidity: Optional[float] = Field(None, description="Humidity percentage")
    wind_speed: float = Field(..., description="Wind speed")
    description: str = Field(..., description="Detailed weather description")

class WeatherResponse(BaseModel):
    """Model for the complete weather response."""
    location: str = Field(..., description="Location name")
    current_weather: WeatherData = Field(..., description="Current weather data")
    forecast: List[ForecastData] = Field(..., description="Weather forecast data")
    suggested_activities: List[str] = Field(..., description="List of suggested activities") 