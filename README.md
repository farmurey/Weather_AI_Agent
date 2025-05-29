# Weather Activity Agent

A smart weather application that not only provides weather information but also suggests activities based on current weather conditions. The application uses both the National Weather Service (NWS) API for US locations and OpenWeatherMap API for global locations.

## Features

- 🌍 Global weather coverage
- 🌡️ Temperature in both Fahrenheit and Celsius
- 💨 Detailed weather conditions with icons
- 🎯 Activity suggestions based on weather
- ⭐ Favorite cities management
- 🔍 Smart city name capitalization
- 🎨 Modern, responsive UI with glass-morphism design
- 🔍 Error handling for unsupported or invalid cities

## Technologies Used

- Python
- Flask
- OpenWeatherMap API
- National Weather Service API
- Tailwind CSS
- Font Awesome Icons
- JavaScript

## Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/Weather_AI_Agent.git
cd Weather_AI_Agent
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the root directory and add your API keys:
```
OPENWEATHER_API_KEY=your_openweather_api_key
```

5. Run the application:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## API Keys

- OpenWeatherMap API: Get your free API key from [OpenWeatherMap](https://openweathermap.org/api)
- National Weather Service API: No API key required

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- OpenWeatherMap for their weather API
- National Weather Service for their US weather data
- Font Awesome for the weather icons
- Tailwind CSS for the styling framework # Weather_AI_Agent
