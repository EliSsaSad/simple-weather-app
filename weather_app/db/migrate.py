import sqlite3
import requests
import time

API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "5f7a8ae5e2671e8b0617894e46c9a358"

def get_cities_with_empty_ru_name(cursor):
    """Выбирает из БД все строки, где ru_name пустое (NULL)."""
    cursor.execute("SELECT id FROM cities WHERE ru_name IS NULL AND country = 'RU'")
    return cursor.fetchall()

def to_ascii_equivalent(char):
    return char.encode().decode('utf-8').upper()

def update_city_ru_name(cursor, city_id, ru_name):
    """Обновляет поле ru_name для города с заданным id."""
    cursor.execute("UPDATE cities SET ru_name = ? WHERE id = ?", (to_ascii_equivalent(ru_name), city_id))

def fetch_city_name(city_id):
    """Отправляет запрос к API и возвращает русское название города."""
    try:
        response = requests.get(API_URL, params={
            "id": city_id,
            "units": "metric",
            "lang": "ru",
            "appid": API_KEY
        })
        response.raise_for_status()  # Проверяет наличие HTTP ошибок
        data = response.json()
        return data.get("name")
    except requests.RequestException as e:
        print(f"Ошибка при запросе для города {city_id}: {e}")
        return None

def main():
    conn = sqlite3.connect("weather_app\db\database.db")  # Укажите путь к вашей БД
    cursor = conn.cursor()

    while True:
        cities = get_cities_with_empty_ru_name(cursor)
        if not cities:
            print("Все города обработаны!")
            break

        for city_id_tuple in cities:
            city_id = city_id_tuple[0]
            ru_name = fetch_city_name(city_id)
            if ru_name:
                update_city_ru_name(cursor, city_id, ru_name)
                conn.commit()
                print(f"Обновлено: {city_id} -> {ru_name}")
            else:
                print(f"Не удалось обновить: {city_id}")
            
            time.sleep(5)  # Пауза между запросами

    conn.close()

if __name__ == "__main__":
    main()
