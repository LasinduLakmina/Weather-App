# Weather-App

This is an advanced weather app built with PyQt6 and the OpenWeatherMap API. The app allows users to get the current weather details of a city, including temperature, humidity, wind speed, and description. Additionally, it displays a weather icon and a temperature trend chart over several days.

## Features

- **City Search**: Enter the name of a city to get its current weather details.
- **Units**: Choose the temperature unit (Celsius, Fahrenheit, Kelvin).
- **Weather Details**: View the temperature, humidity, wind speed, and a weather description.
- **Weather Icon**: Displays an icon representing the current weather condition.
- **Progress Bar**: Shows a progress bar while fetching data.
- **Temperature Trend Chart**: Visualizes the temperature trends for several days (dummy data for now).
- **Caching**: Saves weather data in a cache file to avoid unnecessary API calls.

## Requirements

- Python 3.x
- PyQt6
- Matplotlib
- Requests

You can install the required packages using `pip`:

```bash
pip install PyQt6 matplotlib requests
```

## Setup

1. Clone the repository:
   
   ```bash
   git clone https://github.com/LAsinduLakmina/Weather-App.git
   cd Weather-App
   ```

2. Replace the `API_KEY` in the script with your own API key from OpenWeatherMap:
   
   - Go to [OpenWeatherMap API](https://openweathermap.org/api) and create an account to obtain your API key.

3. Run the app:

   ```bash
   python app.py
   ```

## How It Works

- The app uses `QThread` for fetching weather data asynchronously from the OpenWeatherMap API.
- The user inputs the city name, and the app retrieves and displays the weather information.
- A progress bar is shown while the data is being fetched.
- The weather icon is loaded and displayed based on the weather conditions.
- A temperature trend chart is plotted using Matplotlib, showing the temperature over a period of several days (currently using dummy data).

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
© 2025 Lasindu Lakmina. All rights reserved.

## Acknowledgements

- OpenWeatherMap API for providing weather data.
- PyQt6 for building the graphical user interface.
- Matplotlib for the temperature trend chart.
