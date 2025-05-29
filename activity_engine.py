from config import TEMP_THRESHOLDS, WEATHER_CONDITIONS

class ActivityEngine:
    def __init__(self):
        self.activities = {
            'sunny_warm': [
                'Visit a park',
                'Go hiking',
                'Beach day',
                'Outdoor sports',
                'Picnic',
                'Outdoor yoga'
            ],
            'sunny_cool': [
                'Walking tour',
                'Sightseeing',
                'Outdoor cafes',
                'Botanical gardens',
                'Bike riding',
                'Outdoor photography'
            ],
            'rainy': [
                'Museums',
                'Shopping malls',
                'Movie theaters',
                'Indoor cafes',
                'Art galleries',
                'Indoor sports'
            ],
            'cold': [
                'Indoor gym',
                'Libraries',
                'Cooking classes',
                'Reading at a cozy cafe',
                'Indoor swimming',
                'Board games'
            ],
            'cloudy': [
                'Flexible outdoor activities',
                'Indoor/outdoor cafes',
                'Shopping',
                'Light hiking',
                'City exploration',
                'Indoor/outdoor sports'
            ]
        }

    def _get_weather_category(self, weather_data: dict) -> str:
        """Determine the weather category based on temperature and conditions."""
        temp = weather_data['temperature']
        condition = WEATHER_CONDITIONS.get(weather_data['conditions'], 'cloudy')

        if condition == 'sunny':
            if temp >= TEMP_THRESHOLDS['WARM']:
                return 'sunny_warm'
            else:
                return 'sunny_cool'
        elif condition == 'rainy':
            return 'rainy'
        elif temp < TEMP_THRESHOLDS['COLD']:
            return 'cold'
        else:
            return 'cloudy'

    def suggest_activities(self, weather_data: dict) -> list:
        """Suggest activities based on weather conditions."""
        category = self._get_weather_category(weather_data)
        return self.activities.get(category, self.activities['cloudy']) 