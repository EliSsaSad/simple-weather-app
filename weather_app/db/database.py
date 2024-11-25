import sqlite3
from typing import List, Optional, Tuple


class Database:
    """
    Класс для управления SQLite-базой данных в приложении погоды.

    Attributes:
        conn (sqlite3.Connection):
            Объект соединения с базой данных SQLite.
        cursor (sqlite3.Cursor):
            Курсор для выполнения SQL-запросов.
    """

    def __init__(self):
        """
        Инициализация подключения к базе данных.
        """
        db_path = 'weather_app/db/database.db'
        self.conn: sqlite3.Connection = sqlite3.connect(db_path)
        self.conn.text_factory = str
        self.cursor: sqlite3.Cursor = self.conn.cursor()

    def __to_ascii_equivalent(self, char: str) -> str:
        """
        Преобразует символ в ASCII-эквивалент
        для совместимости SQLite с кириллицей.

        Args:
            char (str): Входной символ.

        Return:
            str: ASCII-эквивалент в верхнем регистре.
        """
        return char.encode().decode('utf-8').upper()

    def create_tables(self) -> None:
        """
        Создаёт необходимые таблицы для работы приложения.
        """
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS cities (
                id       INTEGER PRIMARY KEY,
                country  TEXT,
                name     TEXT,
                ru_name  TEXT,
                lat      REAL,
                lon      REAL,
                favorite BOOLEAN DEFAULT (0) 
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_name TEXT UNIQUE,
                setting_value TEXT
            )
        ''')
        self.conn.commit()

    def get_cities(
        self,
        country: Optional[str] = None,
        ru_name: Optional[str] = None,
        fields: Optional[List[str]] = None
    ) -> List[Tuple]:
        """
        Получает список городов из базы данных
        с возможностью фильтрации и выбора полей.

        Args:
            country (Optional[str], optional):
                Фильтр по стране. По умолчанию None.
            ru_name (Optional[str], optional):
                Фильтр по названию города. По умолчанию None.
            fields (Optional[List[str]], optional):
                Список полей для выборки. По умолчанию None.

        Return:
            List[Tuple]: Список городов, соответствующих критериям.
        """
        query = 'SELECT '

        if fields:
            query += ', '.join(fields)
        else:
            query += '*'

        query += ' FROM cities WHERE ru_name IS NOT NULL'
        params = []

        if country:
            query += ' AND country = ?'
            params.append(country)

        if ru_name:
            query += (
                ' AND (ru_name COLLATE NOCASE LIKE ? '
                'OR ru_name COLLATE NOCASE LIKE ?)'
            )
            params.extend(
                [f'%{self.__to_ascii_equivalent(ru_name)}%', f'%{ru_name}%']
            )

        query += '''
            ORDER BY favorite DESC,
                    CASE WHEN country = 'RU' THEN 0 ELSE 1 END,
                    country
        '''

        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def is_city_favorite(self, city_id: int) -> bool:
        """
        Проверяет, является ли город избранным.

        Args:
            city_id (int): Идентификатор города.

        Return:
            bool: True, если город избранный, иначе False.
        """
        query = 'SELECT favorite FROM cities WHERE id = ?'
        self.cursor.execute(query, (city_id,))
        result = self.cursor.fetchone()
        return bool(result and result[0] == 1)

    def set_setting(self, name: str, value: str) -> None:
        """
        Устанавливает значение для указанной настройки.

        Args:
            name (str): Название настройки.
            value (str): Значение настройки.
        """
        self.cursor.execute('''
            INSERT INTO settings (setting_name, setting_value)
            VALUES (?, ?)
            ON CONFLICT(setting_name)
            DO UPDATE SET setting_value=?
        ''', (name, value, value))
        self.conn.commit()

    def get_setting(self, name: str) -> Optional[str]:
        """
        Получает значение указанной настройки.

        Args:
            name (str): Название настройки.

        Return:
            Optional[str]: Значение настройки или None, если она отсутствует.
        """
        self.cursor.execute(
            'SELECT setting_value FROM settings WHERE setting_name = ?',
            (name,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else None

    def update_city_favorite(self, city_id: int, is_favorite: bool) -> None:
        """
        Обновляет статус избранного для города.

        Args:
            city_id (int): Идентификатор города.
            is_favorite (bool): Новый статус избранного.
        """
        query = '''
            UPDATE cities
            SET favorite = ?
            WHERE id = ?
        '''
        self.cursor.execute(query, (is_favorite, city_id))
        self.conn.commit()

    def close(self) -> None:
        """
        Закрывает соединение с базой данных.
        """
        self.conn.close()
