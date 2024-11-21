import requests
from weather_app.db.database import Database

class WeatherAPI:
    def __init__(self, database: Database, parent=None):
        """Инициализация WeatherAPI с подключением к базе данных."""
        self.database = database
        self.api_key = self.database.get_setting('OPEN_WEATHER_MAP_API_KEY')
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.default_params = {
            "units": "metric",
            "lang": "ru",
            "appid": self.api_key,
        }

    def fetch_weather_by_city_id(self, city_id: int) -> dict:
        """Получить данные о погоде для заданного города по его ID."""
        params = self.default_params.copy()
        params["id"] = city_id

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Ошибка при выполнении запроса к API: {e}")

    def fetch_weather_by_coordinates(self, lat: float, lon: float) -> dict:
        """Получить данные о погоде для заданных координат (широта, долгота)."""
        params = self.default_params.copy()
        params["lat"] = lat
        params["lon"] = lon

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise RuntimeError(f"Ошибка при выполнении запроса к API: {e}")
