import sys
import requests
import json
import os
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, 
                             QMessageBox, QGridLayout, QComboBox, QTableWidget, QTableWidgetItem, 
                             QFrame, QHBoxLayout, QProgressBar)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from io import BytesIO
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

API_KEY = "3f8deb03a7a6bb6159cd1b0223a30763"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
GEO_API = "https://ipinfo.io/json"
CACHE_FILE = "weather_cache.json"

class WeatherThread(QThread):
    data_fetched = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, url, params):
        super().__init__()
        self.url = url
        self.params = params

    def run(self):
        try:
            response = requests.get(self.url, params=self.params)
            if response.status_code == 200:
                self.data_fetched.emit(response.json())
            else:
                self.error_occurred.emit("Failed to retrieve data!")
        except Exception as e:
            self.error_occurred.emit(str(e))

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.load_cache()

    def initUI(self):
        self.setWindowTitle("Weather App")
        self.setGeometry(100, 100, 600, 700)
        self.setStyleSheet("background-color: #2c3e50; color: white; font-size: 14px;")

        layout = QVBoxLayout()

        # Header
        header = QLabel("Weather App", self)
        header.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        # Input Section
        input_frame = QFrame(self)
        input_frame.setStyleSheet("background-color: #34495e; border-radius: 10px;")
        input_layout = QGridLayout()

        self.city_input = QLineEdit(self)
        self.city_input.setPlaceholderText("Enter city name")
        self.city_input.setStyleSheet("padding: 8px; border-radius: 5px;")
        input_layout.addWidget(self.city_input, 0, 0, 1, 2)

        self.search_button = QPushButton("Get Weather", self)
        self.search_button.setStyleSheet("background-color: #1abc9c; padding: 10px; border-radius: 5px;")
        self.search_button.clicked.connect(self.get_weather)
        input_layout.addWidget(self.search_button, 0, 2)

        self.unit_selector = QComboBox(self)
        self.unit_selector.addItems(["Celsius", "Fahrenheit", "Kelvin"])
        self.unit_selector.setStyleSheet("padding: 8px; border-radius: 5px;")
        input_layout.addWidget(self.unit_selector, 1, 0, 1, 3)

        input_frame.setLayout(input_layout)
        layout.addWidget(input_frame)
        
        # Weather Info
        self.weather_info = QLabel("Weather details will appear here", self)
        self.weather_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.weather_info.setStyleSheet("background-color: #34495e; padding: 10px; border-radius: 10px;")
        layout.addWidget(self.weather_info)

        self.weather_icon = QLabel(self)
        self.weather_icon.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.weather_icon)
        
        # Progress Bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setStyleSheet("background-color: #95a5a6; border-radius: 5px;")
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
        # Forecast Chart
        self.chart = FigureCanvas(plt.figure())
        layout.addWidget(self.chart)
        
        self.setLayout(layout)

    def load_cache(self):
        if os.path.exists(CACHE_FILE):
            try:
                with open(CACHE_FILE, "r") as f:
                    self.cache = json.load(f)
            except json.JSONDecodeError:
                self.cache = {}
        else:
            self.cache = {}

    def save_cache(self):
        with open(CACHE_FILE, "w") as f:
            json.dump(self.cache, f)

    def get_weather(self):
        city = self.city_input.text()
        if not city:
            QMessageBox.warning(self, "Input Error", "Please enter a city name!")
            return

        self.progress_bar.show()

        unit = self.unit_selector.currentText()
        units_map = {"Celsius": "metric", "Fahrenheit": "imperial", "Kelvin": "standard"}
        units = units_map[unit]
        
        self.thread = WeatherThread(BASE_URL, {"q": city, "appid": API_KEY, "units": units})
        self.thread.data_fetched.connect(self.display_weather)
        self.thread.error_occurred.connect(lambda msg: QMessageBox.critical(self, "Error", msg))
        self.thread.start()
    
    def display_weather(self, data):
        self.progress_bar.hide()
        
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        description = data['weather'][0]['description']
        icon_code = data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        
        weather_text = f"Temperature: {temp}°\nHumidity: {humidity}%\nWind Speed: {wind_speed} m/s\nDescription: {description.title()}"
        self.weather_info.setText(weather_text)
        
        icon_response = requests.get(icon_url)
        pixmap = QPixmap()
        pixmap.loadFromData(BytesIO(icon_response.content).read())
        self.weather_icon.setPixmap(pixmap)
        
        self.plot_forecast()

    def plot_forecast(self):
        plt.clf()
        ax = self.chart.figure.add_subplot(111)
        ax.plot([1, 2, 3, 4, 5], [22, 24, 20, 23, 25], marker='o', linestyle='-', color='b')
        ax.set_title("Temperature Trend")
        ax.set_xlabel("Days")
        ax.set_ylabel("Temperature (°C)")
        self.chart.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec())
