"""Главная страница приложения"""

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QStackedWidget,
    QLineEdit
)
from weather_app.api.weather_api import WeatherAPI
from weather_app.db.database import Database
from typing import Any, Dict, List, Optional
import threading


class HomePage(QtWidgets.QWidget):
    """
    Главная страница приложения для
    отображения информации о погоде.

    Attributes:
        database (Database):
            Объект для работы с базой данных.
        weather_api (WeatherAPI):
            Объект для получения данных о погоде.
        default_city_id (int):
            ID города по умолчанию, полученный из базы данных.
        main_layout (QtWidgets.QHBoxLayout):
            Основной layout для организации интерфейса.
        left_section (QtWidgets.QWidget):
            Левая секция интерфейса.
        right_section (QtWidgets.QWidget):
            Правая секция интерфейса.
        forecast_cards (List[QtWidgets.QWidget]):
            Список карточек прогноза погоды для трех дней.
    """

    def __init__(self, parent: Optional[QtWidgets.QWidget] = None) -> None:
        """
        Инициализация главной страницы приложения.

        Загружает настройки и обновляет данные о погоде для города, который был
        установлен по умолчанию в базе данных.

        Args:
            parent (Optional[QtWidgets.QWidget], optional):
                Родительский объект для текущего виджета (по умолчанию None).
        """
        super().__init__(parent)
        self.database = Database()
        self.weather_api = WeatherAPI(self.database)

        self.init_ui()

        # Изначальный город получаем из БД и обновляем
        self.default_city_id = self.database.get_setting('LAST_SITY_ID')
        self.update_weather(self.default_city_id)

    def degrees_to_compass(self, deg: float) -> str:
        """
        Переводит градусы в направление ветра по компасу.

        Args:
            deg (float): Угол в градусах.

        Return:
            str: Направление ветра.
        """
        directions = [
            "С", "СВ", "В", "ЮВ",
            "Ю", "ЮЗ", "З", "СЗ"
        ]
        index = round(deg / 45) % 8
        return directions[index]

    def init_ui(self) -> None:
        """
        Инициализирует пользовательский
        интерфейс главной страницы.

        Создает основной layout, разделяет
        интерфейс на секции с использованием
        QSplitter.
        """
        # Основной layout
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # Создаем QSplitter для разделения секций
        splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # Левая секция
        self.left_section = self.create_left_section()
        splitter.addWidget(self.left_section)

        # Правая секция
        self.right_section = self.create_right_section()
        splitter.addWidget(self.right_section)

        # Устанавливаем QSplitter в layout
        self.main_layout.addWidget(splitter)

    def create_left_section(self):
        """
        Создает левую секцию с состоянием загрузки,
        отображением данных о текущей погоде
        и прогнозом на 3 дня вперёд.
        """
        section = QtWidgets.QWidget(self)
        section.setFixedWidth(720)
        section_layout = QtWidgets.QVBoxLayout(section)
        section_layout.setContentsMargins(0, 0, 0, 0)
        section_layout.setSpacing(10)

        # Основная секция с загрузкой и текущей погодой
        self.stack_widget = QStackedWidget(section)
        self.stack_widget.setStyleSheet(
            """
            QStackedWidget, QWidget {
                border-radius: 10px;
                background-color: #f0f0f3;
            }
            """
        )
        self.stack_widget.setMinimumSize(200, 300)

        # Экран загрузки
        self.loading_widget = self.create_loading_screen()
        self.stack_widget.addWidget(self.loading_widget)

        # Экран данных о текущей погоде
        self.weather_widget = self.create_weather_screen()
        self.stack_widget.addWidget(self.weather_widget)

        section_layout.addWidget(self.stack_widget)

        # Секция "Прогноз на три дня"
        self.three_days_ahead = self.create_three_days_ahead()
        section_layout.addWidget(self.three_days_ahead)

        return section

    def create_three_days_ahead(self) -> QtWidgets.QWidget:
        """
        Создает секцию для прогноза на три дня в виде карточек.

        Return:
            QtWidgets.QWidget: Виджет с карточками прогноза.
        """
        widget = QtWidgets.QWidget(self)

        layout = QtWidgets.QHBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(1)

        # Инициализируем пустые карточки
        self.forecast_cards = []
        for i in range(3):
            card = self.create_forecast_card(i)
            layout.addWidget(card)
            self.forecast_cards.append(card)

        widget.setStyleSheet(
            """
            QWidget {
                border-radius: 10px;
                background-color: #e9e9ef;
            }
            """
        )

        return widget

    def create_forecast_card(self, index: int) -> QtWidgets.QWidget:
        """
        Создает одну карточку с данными прогноза для одного дня.

        Args:
            index (int): Индекс карточки для уникальной идентификации.

        Return:
            QtWidgets.QWidget: Карточка прогноза для одного дня.
        """
        card_widget = QtWidgets.QWidget(self)
        card_widget.setStyleSheet(
            """
            background-color: #FFFFFF;
            border-radius: 10px;
            """
        )
        card_layout = QtWidgets.QVBoxLayout(card_widget)
        card_layout.setContentsMargins(5, 5, 5, 5)
        card_layout.setSpacing(5)

        # Заголовок карточки (пока пустой, обновится позже)
        date_label = QtWidgets.QLabel("Дата: -")
        date_label.setObjectName(f"date_label_{index}")
        date_label.setAlignment(QtCore.Qt.AlignCenter)
        date_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        card_layout.addWidget(date_label)

        # Иконка погоды (пока пустая)
        icon_label = QtWidgets.QLabel()
        icon_label.setObjectName(f"icon_label_{index}")
        icon_label.setPixmap(QtGui.QPixmap())  # Пустой QPixmap
        icon_label.setFixedSize(100, 100)
        card_layout.addWidget(icon_label, alignment=QtCore.Qt.AlignCenter)

        # Описание (пока пустое)
        desc_label = QtWidgets.QLabel("Описание: -")
        desc_label.setAlignment(QtCore.Qt.AlignCenter)
        desc_label.setObjectName(f"desc_label_{index}")
        desc_label.setStyleSheet("font-size: 14px;")
        card_layout.addWidget(desc_label)

        # Температура (пока пустая)
        temp_min_label = QtWidgets.QLabel("Мин. температура: -°C")
        temp_min_label.setObjectName(f"temp_min_label_{index}")
        temp_max_label = QtWidgets.QLabel("Макс. температура: -°C")
        temp_max_label.setObjectName(f"temp_max_label_{index}")
        temp_min_label.setStyleSheet("font-size: 14px;")
        temp_max_label.setStyleSheet("font-size: 14px;")
        card_layout.addWidget(temp_min_label)
        card_layout.addWidget(temp_max_label)

        # Установим фиксированную ширину и высоту для карточки
        card_widget.setFixedWidth(225)
        card_widget.setFixedHeight(260)

        return card_widget

    def update_forecast(self, forecast_data: list[dict]) -> None:
        """
        Обновляет данные прогноза погоды в карточках.

        Args:
            forecast_data (list[dict]):
                Список данных прогноза для трех дней.
                Каждый элемент списка должен быть словарем с ключами:
                'date', 'pixmap', 'temp_min', 'temp_max', 'description'.
        """
        for i, data in enumerate(forecast_data):
            # Обновляем карточку для каждого дня
            card = self.forecast_cards[i]

            # Обновляем дату
            date_label = card.findChild(QtWidgets.QLabel, f"date_label_{i}")
            date_label.setText(data['date'])

            # Обновляем иконку
            icon_label = card.findChild(QtWidgets.QLabel, f"icon_label_{i}")
            icon_label.setPixmap(data['pixmap'])

            # Обновляем температуру
            temp_min_label = card.findChild(
                QtWidgets.QLabel,
                f"temp_min_label_{i}"
            )
            temp_max_label = card.findChild(
                QtWidgets.QLabel,
                f"temp_max_label_{i}"
            )
            temp_min_label.setText(f"Мин. температура: {data['temp_min']}°C")
            temp_max_label.setText(f"Макс. температура: {data['temp_max']}°C")

            # Обновляем описание
            desc_label = card.findChild(QtWidgets.QLabel, f"desc_label_{i}")
            desc_label.setText(f"{data['description']}")

    def create_loading_screen(self) -> QtWidgets.QWidget:
        """
        Создает экран загрузки с текстом "Загрузка данных...".

        Return:
            QtWidgets.QWidget: Виджет с экраном загрузки.
        """
        widget = QtWidgets.QWidget(self)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        label = QLabel("Загрузка данных...")
        label.setStyleSheet(
            """
            font-size: 18px;
            font-weight: bold;
            text-align: center;
            """
        )
        layout.addWidget(label, alignment=QtCore.Qt.AlignCenter)

        return widget

    def create_weather_screen(self) -> QtWidgets.QWidget:
        """
        Создает экран с данными о текущей погоде в городе.

        Этот метод создает виджет, который отображает текущую погоду, включая:
        - Иконку погоды
        - Температуру
        - Описание
        - Ощущаемую температуру
        - Дополнительные параметры (давление, влажность, ветер)

        Returns:
            QtWidgets.QWidget:
                Виджет, содержащий все элементы прогноза погоды.
        """
        widget = QtWidgets.QWidget(self)
        self.weather_layout = QVBoxLayout(widget)
        self.weather_layout.setAlignment(QtCore.Qt.AlignTop)
        self.weather_layout.setContentsMargins(10, 10, 10, 10)
        self.weather_layout.setSpacing(10)

        # Заголовок
        self.weather_title = QLabel("Текущая погода в городе -")
        self.weather_title.setAlignment(QtCore.Qt.AlignCenter)
        self.weather_title.setStyleSheet(
            """
            font-size: 20px; font-weight: bold;
            """)
        self.weather_layout.addWidget(self.weather_title)

        # Основной горизонтальный компоновщик
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(20)

        # Левая часть (основные данные о погоде)
        left_layout = QVBoxLayout()
        left_layout.setSpacing(10)

        # Строка с иконкой погоды и температурой
        weather_row_layout = QHBoxLayout()
        weather_row_layout.setSpacing(10)

        # Иконка погоды
        self.weather_icon_label = QLabel()
        self.weather_icon_label.setStyleSheet(
            """
            background-color: white;
            border-radius: 10px;
            """
        )
        self.weather_icon_label.setPixmap(QtGui.QPixmap())  # Пустой QPixmap
        self.weather_icon_label.setFixedSize(160, 160)
        self.weather_icon_label.setScaledContents(True)
        weather_row_layout.addWidget(self.weather_icon_label)

        # Температура
        self.temp_label = QLabel("Температура: -")
        self.temp_label.setStyleSheet("font-size: 65px;")
        weather_row_layout.addWidget(self.temp_label)

        left_layout.addLayout(weather_row_layout)

        # Описание погоды
        self.desc_label = QLabel("Описание: -")
        self.desc_label.setStyleSheet("font-size: 35px; font-weight: normal;")
        left_layout.addWidget(self.desc_label)

        # Ощущаемая температура
        self.feels_like_label = QLabel("Ощущаемая температура: -")
        self.feels_like_label.setStyleSheet(
            """
            font-size: 22px;
            font-weight: normal;
            """
        )
        left_layout.addWidget(self.feels_like_label)

        # Правая часть (дополнительные параметры)
        right_layout = QVBoxLayout()
        right_layout.setContentsMargins(40, 20, 0, 0)
        right_layout.setSpacing(10)
        right_layout.setAlignment(QtCore.Qt.AlignTop)

        # Строка с давлением
        pressure_row_layout = QHBoxLayout()
        pressure_row_layout.setSpacing(10)

        # Иконка давления
        pressure_icon_label = QLabel()
        pressure_pixmap = QtGui.QPixmap("weather_app/ui/icons/ui/pressure.png")
        pressure_icon_label.setPixmap(pressure_pixmap)
        pressure_icon_label.setFixedSize(40, 40)
        pressure_icon_label.setScaledContents(True)
        pressure_row_layout.addWidget(pressure_icon_label)

        # Лейбл давления
        self.pressure_label = QLabel("Давление: -")
        self.pressure_label.setStyleSheet("font-size: 20px;")
        pressure_row_layout.addWidget(self.pressure_label)

        right_layout.addLayout(pressure_row_layout)

        # Строка с влажностью
        humidity_row_layout = QHBoxLayout()
        humidity_row_layout.setSpacing(10)

        # Иконка влажности
        humidity_icon_label = QLabel()
        humidity_pixmap = QtGui.QPixmap("weather_app/ui/icons/ui/humidity.png")
        humidity_icon_label.setPixmap(humidity_pixmap)
        humidity_icon_label.setFixedSize(40, 40)
        humidity_icon_label.setScaledContents(True)
        humidity_row_layout.addWidget(humidity_icon_label)

        # Лейбл влажности
        self.humidity_label = QLabel("- %")
        self.humidity_label.setStyleSheet("font-size: 20px;")
        humidity_row_layout.addWidget(self.humidity_label)

        right_layout.addLayout(humidity_row_layout)

        # Строка с ветром
        wind_row_layout = QHBoxLayout()
        wind_row_layout.setSpacing(10)

        # Иконка ветра
        wind_icon_label = QLabel()
        humidity_pixmap = QtGui.QPixmap("weather_app/ui/icons/ui/wind.png")
        wind_icon_label.setPixmap(humidity_pixmap)
        wind_icon_label.setFixedSize(40, 40)
        wind_icon_label.setScaledContents(True)
        wind_row_layout.addWidget(wind_icon_label)

        # Лейбл ветра
        self.wind_label = QLabel("- М/С")
        self.wind_label.setStyleSheet("font-size: 20px;")
        wind_row_layout.addWidget(self.wind_label)

        right_layout.addLayout(wind_row_layout)

        # Добавление секций в основной компоновщик
        main_layout.addLayout(left_layout)
        main_layout.addLayout(right_layout)

        # Добавляем основной компоновщик в общий
        self.weather_layout.addLayout(main_layout)

        self.desc_label.raise_()
        return widget

    def create_right_section(self):
        """Создает правую секцию с кнопками для выбора города и поиск."""
        section = QtWidgets.QWidget(self)
        section.setStyleSheet(
            """
            QWidget {
                border-radius: 10px;
                background-color: #f0f0f3;
            }
            """
        )
        section.setMinimumSize(200, 300)

        layout = QVBoxLayout(section)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Секция поиска
        search_widget = QtWidgets.QWidget()
        search_widget.setStyleSheet(
            """
            QWidget {
                background-color: white;
                border-radius: 8px;
                border: 0;
                margin: 10px;
                margin-bottom: 15px;
            }
            """
        )

        search_icon = QLabel(self)
        search_icon.setPixmap(
            QtGui.QPixmap("weather_app/ui/icons/ui/Search.png")
        )
        search_icon.setStyleSheet(
            """
            padding: 0px;
            margin: 0px;
            margin-right: 10px;
            margin-bottom: 5px;
            """
        )

        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(10, 15, 10, 15)
        search_layout.setSpacing(5)

        search_input = QLineEdit(self)
        search_input.setPlaceholderText("Введите название города...")
        search_input.textChanged.connect(self.update_city_list)
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_icon)

        # Полоска (граница)
        line_widget = QtWidgets.QWidget(self)
        line_widget.setFixedHeight(1)
        line_widget.setStyleSheet("background-color: #d3d3d3;")

        layout.addWidget(search_widget)
        layout.addWidget(line_widget, alignment=QtCore.Qt.AlignBottom)

        # Прокручиваемая область для кнопок
        scroll_area = QScrollArea(section)
        scroll_area.setStyleSheet(
            """
            QScrollArea {
                padding-left: 5px;
                padding-right: 5px;
            }

            QScrollBar:vertical, QScrollBar:horizontal {
                background-color: transparent;
                width: 30px;
                margin: 5px;
                margin-right: 0;
                height: 12px;
            }

            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background-color: gray;
                border-radius: 5px;
                min-height: 30px;
            }

            QScrollBar::handle:vertical:hover,
            QScrollBar::handle:horizontal:hover {
                background-color: darkgray;
            }

            QScrollBar::add-line, QScrollBar::sub-line {
                border: none;
                width: 0;
                margin: 0;
            }

            QScrollBar::up-arrow, QScrollBar::down-arrow,
            QScrollBar::left-arrow, QScrollBar::right-arrow {
                border: none;
                width: 0;
                margin: 0;
            }
            """
        )
        scroll_area.setWidgetResizable(True)
        scroll_content = QtWidgets.QWidget()
        scroll_content.setStyleSheet("border-radius: 10px;")
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_layout.setSpacing(0)
        scroll_layout.setAlignment(QtCore.Qt.AlignTop)

        # Изначальное получение списка городов
        self.city_buttons_layout = scroll_layout
        self.update_city_list()

        scroll_content.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_content)
        layout.addWidget(scroll_area)

        return section

    def update_city_list(self, query: str = "") -> None:
        """
        Обновляет список городов на основе поискового запроса.

        Эта функция очищает старые карточки
        городов и добавляет новые карточки
        с данными о городах, соответствующих запросу.
        Максимум добавляется 100 городов.

        Args:
            query (str, optional):
                Строка поискового запроса для фильтрации городов.
                По умолчанию пустая строка.

        Returns:
            None
        """

        # TODO: Реализовать lazy loading списка городов.

        cities = self.database.get_cities(
            fields=['id', 'ru_name', 'lat', 'lon', 'country', 'favorite'],
            ru_name=query
        )

        # Очищаем старые карточки
        for i in range(self.city_buttons_layout.count()):
            widget = self.city_buttons_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Добавляем новые карточки, максимум 100
        for city_id, city_name, lat, lon, country, favorite in cities[:100]:
            if city_name:
                # Создаем контейнер для карточки города
                card_widget = QtWidgets.QWidget()
                card_widget.setCursor(
                    QtGui.QCursor(QtCore.Qt.PointingHandCursor)
                )
                card_widget.setStyleSheet(
                    """
                    QWidget {
                        background-color: white;
                        border-radius: 10px;
                        margin-top: 6px;
                        margin-bottom: 6px;
                    }

                    QWidget:hover {
                        border: 1px solid #969696;
                    }

                    QLabel:hover {
                        border: 0px solid transparent;
                    }
                    """
                )
                card_widget.setFixedHeight(120)
                card_layout = QtWidgets.QHBoxLayout(card_widget)
                card_layout.setContentsMargins(10, 5, 10, 5)
                card_layout.setSpacing(10)

                # Создаем вертикальный layout для названия города и координат
                city_info_layout = QtWidgets.QVBoxLayout()
                city_info_layout.setContentsMargins(0, 0, 0, 0)
                city_info_layout.setSpacing(2)

                # Метка с названием города
                city_label = QtWidgets.QLabel(f"{city_name} ({country})")
                city_label.setStyleSheet("font-size: 18px; font-weight: bold;")
                city_info_layout.addWidget(city_label)

                # Метка с широтой и долготой
                coords_label = QtWidgets.QLabel(
                    f"Широта: {lat:.4f}, Долгота: {lon:.4f}"
                )
                coords_label.setStyleSheet("font-size: 14px; color: #555;")
                city_info_layout.addWidget(coords_label)

                card_layout.addLayout(city_info_layout)

                # Создаем spacer (будет занимать оставшееся пространство)
                spacer = QtWidgets.QSpacerItem(
                    40,
                    20,
                    QtWidgets.QSizePolicy.Expanding,
                    QtWidgets.QSizePolicy.Minimum
                )
                card_layout.addItem(spacer)

                # Создаем метку для отображения иконки сердца
                heart_icon = QtWidgets.QLabel()
                if favorite:
                    heart_icon.setPixmap(
                        QtGui.QPixmap("weather_app/ui/icons/ui/Heart.png")
                    )
                    heart_icon.setStyleSheet("margin-right: 10px;")
                else:
                    heart_icon.setPixmap(
                        QtGui.QPixmap("weather_app/ui/icons/ui/NoHeart.png")
                    )
                    heart_icon.setStyleSheet("margin-right: 15px;")

                heart_icon.mousePressEvent = (
                    lambda event, city_id=city_id, heart_icon=heart_icon: (
                        self.toggle_favorite(city_id, heart_icon)
                    )
                )
                card_layout.addWidget(heart_icon)

                # Обработчик клика по карточке (по всей карточке)
                card_widget.mousePressEvent = (
                    lambda event, city_id=city_id: (
                        self.on_card_click(city_id)
                    )
                )

                self.city_buttons_layout.addWidget(card_widget)

    def toggle_favorite(
            self,
            city_id: int,
            heart_icon: QtWidgets.QLabel
    ) -> None:
        """
        Обработчик клика по иконке сердца для
        добавления/удаления города из избранного.

        Args:
            city_id (int):
                ID города, который нужно
                добавить или удалить из избранного.
            heart_icon (QtWidgets.QLabel):
                Иконка сердца, которую нужно обновить
                в зависимости от состояния избранного города.

        Return:
            None
        """
        # Получаем текущее состояние города из базы данных
        is_favorite = self.database.is_city_favorite(city_id)

        # Обновить информацию о городе в базе данных
        self.database.update_city_favorite(city_id, not is_favorite)

        # После обновления в базе данных, получаем новое состояние
        new_favorite_state = not is_favorite
        # Обновляем иконку в зависимости от нового состояния
        if new_favorite_state:
            heart_icon.setPixmap(
                QtGui.QPixmap("weather_app/ui/icons/ui/Heart.png")
            )
            heart_icon.setStyleSheet("margin-right: 10px;")
        else:
            heart_icon.setPixmap(
                QtGui.QPixmap("weather_app/ui/icons/ui/NoHeart.png")
            )
            heart_icon.setStyleSheet("margin-right: 15px;")

    def on_card_click(self, city_id: int) -> None:
        """
        Обработчик клика по карточке города.

        Этот метод сохраняет выбранный city_id
        в базе данных как последний выбранный город,
        и обновляет данные о погоде.

        Args:
            city_id (int): ID выбранного города.
        """
        self.database.set_setting('LAST_SITY_ID', city_id)
        self.update_weather(city_id)

    def get_weather_data(self, city_id: int) -> Optional[Dict[str, Any]]:
        """
        Получает данные о погоде для заданного города.

        Этот метод запрашивает данные о
        погоде для города с помощью API и Return
        данные в виде словаря.

        Args:
            city_id (int): ID города для получения данных о погоде.

        Return:
            Optional[Dict[str, Any]]:
                Данные о погоде в формате
                словаря или None в случае ошибки.
        """
        try:
            return self.weather_api.fetch_weather_by_city_id(city_id)
        except Exception as e:
            print(f"Ошибка получения данных о погоде: {e}")
            return None

    def update_weather(self, city_id: int) -> None:
        """
        Обновляет данные о погоде в левой секции для выбранного города.

        Этот метод обновляет интерфейс
        с прогнозом погоды, отображая экран загрузки
        и обновляя карточки для прогноза на три дня.

        Args:
            city_id (int):
                ID города для получения и
                отображения данных о погоде.
        """
        # Показать экран загрузки текущей погоды
        self.stack_widget.setCurrentWidget(self.loading_widget)

        # Показать загрузку для карточек прогноза на 3 дня
        for i in range(0, 3):
            # Обновляем карточку для каждого дня
            card = self.forecast_cards[i]

            # Обновляем дату
            date_label = card.findChild(QtWidgets.QLabel, f"date_label_{i}")
            date_label.setText("")

            # Обновляем иконку
            icon_label = card.findChild(QtWidgets.QLabel, f"icon_label_{i}")
            icon_label.setPixmap(QtGui.QPixmap())

            # Обновляем температуру
            temp_min_label = card.findChild(
                QtWidgets.QLabel,
                f"temp_min_label_{i}"
            )
            temp_max_label = card.findChild(
                QtWidgets.QLabel,
                f"temp_max_label_{i}"
            )
            temp_min_label.setText("")
            temp_max_label.setText("")

            # Обновляем описание
            desc_label = card.findChild(QtWidgets.QLabel, f"desc_label_{i}")
            desc_label.setText("Загрузка...")

        def fetch_and_update():
            weather_data = self.weather_api.fetch_weather_by_city_id(city_id)
            forecast_data = self.weather_api.fetch_forecast_by_city_id(city_id)
            QtCore.QMetaObject.invokeMethod(
                self,
                "update_weather_ui",
                QtCore.Qt.QueuedConnection,
                QtCore.Q_ARG(dict, weather_data),
                QtCore.Q_ARG(list, forecast_data),
            )

        threading.Thread(target=fetch_and_update, daemon=True).start()

    @QtCore.pyqtSlot(dict, list)
    def update_weather_ui(
        self,
        weather_data: Dict[str, str],
        forecast_data: List[Dict[str, str]]
    ) -> None:
        """
        Обновляет интерфейс левой секции данными о
        текущей погоде и прогнозе на несколько дней.

        Args:
            weather_data (dict):
                Словарь с данными о текущей погоде.
                Ожидаемые ключи:
                    'city',
                    'temperature',
                    'description',
                    'pressure',
                    'feels_like',
                    'humidity',
                    'wind_speed',
                    'wind_deg',
                    'pixmap'.
            forecast_data (list):
                Список словарей с данными
                прогноза погоды на несколько дней.
                Каждый элемент списка должен быть
                словарем с ключами:
                    'date',
                    'pixmap',
                    'temp_min',
                    'temp_max',
                    'description'.

        Return:
            None
        """
        # Обновляем данные о текущей погоде
        city_name = weather_data["city"]
        temp = weather_data["temperature"]
        description = weather_data["description"]
        pressure = weather_data["pressure"]
        feels_like = weather_data["feels_like"]
        humidity = weather_data["humidity"]
        wind = (
            f"{weather_data['wind_speed']} м/с, "
            f"{self.degrees_to_compass(weather_data['wind_deg'])}"
        )

        self.weather_title.setText(f"Текущая погода в: {city_name}")
        self.temp_label.setText(f"{temp} ℃")
        self.desc_label.setText(f"{description}")
        # переводим из гПа в мм рт. ст.
        self.pressure_label.setText(
            f"{round(pressure * 0.750063755)} мм рт. ст. "
        )
        self.weather_icon_label.setPixmap(weather_data['pixmap'])
        self.feels_like_label.setText(f"Ощущается как {feels_like} ℃")
        self.humidity_label.setText(f"{humidity}% ")
        self.wind_label.setText(wind)

        # Обновляем данные прогноза
        self.update_forecast(forecast_data)

        # Показать экран с погодой
        self.stack_widget.setCurrentWidget(self.weather_widget)
