import sqlite3
import os

# Путь к базе данных


class Database:
    def __init__(self):
        """Инициализация подключения к базе данных"""
        db_path = 'weather_app\db\database.db'
        self.conn = sqlite3.connect(db_path)
        self.conn.text_factory = str
        self.cursor = self.conn.cursor()
        
    def __to_ascii_equivalent(self, char):
        """Для корректной работы sqlite3 с кирилицей"""
        return char.encode().decode('utf-8').upper()

    def create_tables(self):
        """Создание таблиц в базе данных"""
        # Создание таблицы для городов
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cities (
                id INTEGER PRIMARY KEY,
                country TEXT,
                city TEXT,
                lat REAL,
                lon REAL,
                favorite BOOLEAN DEFAULT 0
            )
        ''')

        # Создание таблицы для настроек приложения
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_name TEXT UNIQUE,
                setting_value TEXT
            )
        ''')

        # Сохраняем изменения
        self.conn.commit()

    def add_city(self, country, city, lat, lon, favorite=False):
        """Добавление города в таблицу"""
        self.cursor.execute('''
            INSERT INTO cities (country, city, lat, lon, favorite) 
            VALUES (?, ?, ?, ?, ?)
        ''', (country, city, lat, lon, favorite))
        self.conn.commit()

    def get_cities(self, country=None, ru_name=None, fields=None):
        """Получение городов из базы данных с возможностью фильтрации и выбора нужных полей."""
        query = 'SELECT '
        
        # Если поля не указаны, выбираем все
        if fields:
            query += ', '.join(fields)
        else:
            query += '*'

        query += ' FROM cities WHERE 1=1'
        params = []

        # Фильтрация по стране (если указана)
        if country:
            query += ' AND country = ?'
            params.append(country)

        # Фильтрация по ru_name (если указано)
        if ru_name:
            query += ' AND ru_name COLLATE NOCASE LIKE ?'  # Нечувствительность к регистру
            params.append(f'%{self.__to_ascii_equivalent(ru_name)}%')  # Приведение параметра к верхнему регистру

        # Сортировка, чтобы города с favorite=True шли первыми
        query += ' ORDER BY favorite DESC'

        # Выполнение запроса
        self.cursor.execute(query, params)
        return self.cursor.fetchall()
    
    def is_city_favorite(self, city_id):
        """Проверка, находится ли город в избранном (favorite == true)."""
        query = 'SELECT favorite FROM cities WHERE id = ?'
        self.cursor.execute(query, (city_id,))
        result = self.cursor.fetchone()

        # Если город найден и его значение favorite = 1, возвращаем True, иначе False
        if result:
            return result[0] == 1
        return False

    def set_setting(self, name, value):
        """Установка значения для настройки"""
        self.cursor.execute('''
            INSERT INTO settings (setting_name, setting_value) 
            VALUES (?, ?)
            ON CONFLICT(setting_name) 
            DO UPDATE SET setting_value=?
        ''', (name, value, value))
        self.conn.commit()

    def get_setting(self, name):
        """Получение значения настройки"""
        self.cursor.execute('SELECT setting_value FROM settings WHERE setting_name = ?', (name,))
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None
    
    def update_city_favorite(self, city_id, is_favorite):
        """Обновление значения favorite для города по его ID."""
        query = '''
            UPDATE cities
            SET favorite = ?
            WHERE id = ?
        '''
        self.cursor.execute(query, (is_favorite, city_id))
        self.conn.commit()

    def close(self):
        """Закрытие соединения с базой данных"""
        self.conn.close()

