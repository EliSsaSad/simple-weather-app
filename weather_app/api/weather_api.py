import requests
from weather_app.db.database import Database
from datetime import datetime, timedelta, timezone
from PyQt5.QtGui import QPixmap
from io import BytesIO
from typing import Any, Dict, List, Optional


class WeatherAPI:
    """
    Класс для взаимодействия с API OpenWeatherMap
    для получения текущей погоды и прогноза погоды.

    Attributes:
        database (Database):
            Экземпляр базы данных для получения настроек,
            таких как API-ключ.
        api_key (str): API-ключ OpenWeatherMap.
        base_url (str): Базовый URL для API текущей погоды.
        forecast_url (str): Базовый URL для API прогноза погоды.
        default_params (dict): Параметры по умолчанию для запросов к API.
    """

    def __init__(self, database: Database, parent: Optional[Any] = None):
        """
        Инициализирует экземпляр WeatherAPI с подключением к базе данных.

        Args:
            database (Database):
                Экземпляр базы данных для получения настроек.
            parent (Optional[Any]):
                Необязательный родительский объект для интеграции с PyQt.
        """
        self.database: Database = database
        self.api_key: str = self.database.get_setting(
            'OPEN_WEATHER_MAP_API_KEY'
        )
        self.base_url: str = (
            "https://api.openweathermap.org/data/2.5/weather"
        )
        self.forecast_url: str = (
            "https://api.openweathermap.org/data/2.5/forecast"
        )
        self.default_params: Dict[str, str] = {
            "units": "metric",
            "lang": "ru",
            "appid": self.api_key,
        }

    def fetch_weather_by_city_id(self, city_id: int) -> Dict[str, Any]:
        """
        Получает текущие данные о погоде для заданного города по его ID.

        Args:
            city_id (int): ID города.

        Return:
            dict:
                Данные о погоде, включая температуру,
                ветер, время восхода/заката,
                а также иконку в формате QPixmap.

        Exception:
            RuntimeError:
                Если запрос к API или обработка данных завершились с ошибкой.
        """
        params = self.default_params.copy()
        params["id"] = city_id

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            weather_info: Dict[str, Any] = {
                "city": data.get("name", "Неизвестный город"),
                "country": data["sys"].get("country", "Неизвестная страна"),
                "temperature": data["main"].get("temp", None),
                "feels_like": data["main"].get("feels_like", None),
                "temp_min": data["main"].get("temp_min", None),
                "temp_max": data["main"].get("temp_max", None),
                "pressure": data["main"].get("pressure", None),
                "humidity": data["main"].get("humidity", None),
                "visibility": data.get("visibility", None),
                "wind_speed": data["wind"].get("speed", None),
                "wind_deg": data["wind"].get("deg", None),
                "wind_gust": data["wind"].get("gust", None),
                "description": data["weather"][0].get(
                    "description", "Описание не найдено"
                ),
                "icon": data["weather"][0].get("icon", ""),
                "clouds": data["clouds"].get("all", None),
                "sunrise": datetime.fromtimestamp(
                    data["sys"]["sunrise"], tz=timezone.utc
                ).strftime('%H:%M:%S'),
                "sunset": datetime.fromtimestamp(
                    data["sys"]["sunset"], tz=timezone.utc
                ).strftime('%H:%M:%S'),
                "timezone": data.get("timezone", None),
            }

            icon_url = (
                f"https://openweathermap.org/img/wn/"
                f"{weather_info['icon']}@2x.png"
            )
            icon_response = requests.get(icon_url)
            icon_response.raise_for_status()
            image_data = BytesIO(icon_response.content)
            pixmap = QPixmap()
            pixmap.loadFromData(image_data.read())
            weather_info["pixmap"] = pixmap

            return weather_info

        except requests.RequestException as e:
            raise RuntimeError(f"Ошибка при выполнении запроса к API: {e}")
        except KeyError as e:
            raise RuntimeError(f"Ошибка обработки данных о погоде: {e}")

    def fetch_forecast_by_city_id(self, city_id: int) -> List[Dict[str, Any]]:
        """
        Получает прогноз погоды на 3 дня для заданного города по его ID.

        Args:
            city_id (int): ID города.

        Return:
            list:
                Список словарей, содержащих данные прогноза,
                включая дату, минимальную/максимальную температуру,
                описание и иконку в формате QPixmap.

        Exception:
            RuntimeError:
                Если запрос к API или обработка данных завершились с ошибкой.
        """
        params = self.default_params.copy()
        params["id"] = city_id

        try:
            response = requests.get(self.forecast_url, params=params)
            response.raise_for_status()
            data = response.json()

            forecast: List[Dict[str, Any]] = []
            current_date = datetime.now(timezone.utc).date()
            target_dates = [
                (current_date + timedelta(days=i)).strftime("%Y-%m-%d")
                for i in range(1, 4)
            ]

            for target_date in target_dates:
                min_temp = float('inf')
                max_temp = float('-inf')
                description = ""
                icon_url = ""

                for entry in data["list"]:
                    entry_date = entry["dt_txt"].split()[0]
                    if entry_date == target_date:
                        min_temp = min(min_temp, entry["main"]["temp_min"])
                        max_temp = max(max_temp, entry["main"]["temp_max"])

                        if entry["dt_txt"].endswith("12:00:00"):
                            description = entry["weather"][0]["description"]
                            icon_url = (
                                f"https://openweathermap.org/img/wn/"
                                f"{entry['weather'][0]['icon']}@2x.png"
                            )

                icon_response = requests.get(icon_url)
                icon_response.raise_for_status()
                image_data = BytesIO(icon_response.content)
                pixmap = QPixmap()
                pixmap.loadFromData(image_data.read())

                forecast.append({
                    "date": target_date,
                    "temp_min": min_temp,
                    "temp_max": max_temp,
                    "description": description,
                    "pixmap": pixmap,
                })

            return forecast

        except requests.RequestException as e:
            raise RuntimeError(f"Ошибка при выполнении запроса к API: {e}")
        except KeyError as e:
            raise RuntimeError(f"Ошибка обработки данных прогноза: {e}")
