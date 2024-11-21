"""Главная страница приложения"""

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QStackedWidget, QLineEdit
from weather_app.api.weather_api import WeatherAPI
from weather_app.db.database import Database
import threading


class HomePage(QtWidgets.QWidget):
    def __init__(self, parent):
        """
        Инициализация главной страницы.

        :param parent: Родительский объект (например, основное окно приложения).
        :param db_path: Путь к базе данных.
        """
        super().__init__(parent)
        self.database = Database()
        self.weather_api = WeatherAPI(self.database)

        self.init_ui()

        # Изначальный город (Москва)
        self.default_city_id = 524894
        self.update_weather(self.default_city_id)

    def init_ui(self):
        """Инициализация пользовательского интерфейса."""
        # Основной layout
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # Левая секция
        self.left_section = self.create_left_section()
        self.main_layout.addWidget(self.left_section)

        # Правая секция
        self.right_section = self.create_right_section()
        self.main_layout.addWidget(self.right_section)

    def create_left_section(self):
        """Создает левую секцию с состоянием загрузки и отображением данных."""
        section = QStackedWidget(self)
        section.setStyleSheet(
            """
            QStackedWidget, QWidget {
                border-radius: 10px;
                background-color: #f0f0f3;
            }
            """
        )
        section.setMinimumSize(200, 300)

        # Экран загрузки
        self.loading_widget = self.create_loading_screen()
        section.addWidget(self.loading_widget)

        # Экран данных о погоде
        self.weather_widget = self.create_weather_screen()
        section.addWidget(self.weather_widget)

        return section

    def create_loading_screen(self):
        """Создает экран загрузки."""
        widget = QtWidgets.QWidget(self)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        label = QLabel("Загрузка данных...")
        label.setStyleSheet("font-size: 18px; font-weight: bold; text-align: center;")
        layout.addWidget(label, alignment=QtCore.Qt.AlignCenter)

        return widget

    def create_weather_screen(self):
        """Создает экран с данными о погоде."""
        widget = QtWidgets.QWidget(self)
        self.weather_layout = QVBoxLayout(widget)
        self.weather_layout.setContentsMargins(10, 10, 10, 10)
        self.weather_layout.setSpacing(10)

        self.weather_title = QLabel("Текущая погода")
        self.weather_title.setStyleSheet(
            """
            font-size: 16px; font-weight: bold;
            """)
        self.weather_layout.addWidget(self.weather_title)

        self.city_label = QLabel("Город: -")

        self.temp_label = QLabel("Температура: -")
        self.desc_label = QLabel("Описание: -")
        self.weather_layout.addWidget(self.city_label)
        self.weather_layout.addWidget(self.temp_label)
        self.weather_layout.addWidget(self.desc_label)

        return widget
    
    def create_right_section(self):
        """Создает правую секцию с кнопками для выбора города и поиск."""
        section = QtWidgets.QWidget(self)
        section.setStyleSheet(
            """
            QWidget {
                border-radius: 10px;
                padding-left: 5px;
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
        search_icon.setPixmap(QtGui.QPixmap("weather_app/ui/icons/ui/Search.png"))
        search_icon.setStyleSheet("padding: 0px; margin: 0px; margin-right: 10px; margin-bottom: 5px;")  # Убираем лишние отступы

        search_layout = QHBoxLayout(search_widget)
        search_layout.setContentsMargins(10, 15, 10, 15)  # Внутренние отступы внутри белого прямоугольника
        search_layout.setSpacing(5)

        search_input = QLineEdit(self)  # Поле для ввода поискового запроса
        search_input.setPlaceholderText("Введите название города...")
        search_input.textChanged.connect(self.update_city_list)  # Подключаем сигнал изменения текста
        search_layout.addWidget(search_input)
        search_layout.addWidget(search_icon)

        # Полоска (граница)
        line_widget = QtWidgets.QWidget(self)
        line_widget.setFixedHeight(1) 
        line_widget.setStyleSheet("background-color: #d3d3d3;")  # Цвет полоски

        layout.addWidget(search_widget)
        layout.addWidget(line_widget, alignment=QtCore.Qt.AlignBottom)

        # Прокручиваемая область для кнопок
        scroll_area = QScrollArea(section)
        scroll_area.setStyleSheet("""
            QScrollBar:vertical, QScrollBar:horizontal {
                background-color: transparent;
                width: 30px;
                margin: 5px;
                height: 12px;
            }
            
            QScrollBar::handle:vertical, QScrollBar::handle:horizontal {
                background-color: gray;
                border-radius: 5px;
            }
            
            QScrollBar::handle:vertical:hover, QScrollBar::handle:horizontal:hover {
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
        """)
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


    def update_city_list(self, query=""):
        """Обновляет список городов на основе поискового запроса."""
        cities = self.database.get_cities(fields=['id', 'ru_name', 'favorite'], ru_name=query.lower())

        # Очищаем старые карточки
        for i in range(self.city_buttons_layout.count()):
            widget = self.city_buttons_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Добавляем новые карточки
        for city_id, city_name, favorite in cities:
            if city_name:  # Пропускаем города с пустым названием
                # Создаем контейнер для карточки города
                card_widget = QtWidgets.QWidget()
                card_widget.setStyleSheet(
                    """
                    QWidget {
                        background-color: white;
                        border-radius: 10px;
                        margin: 6px;
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

                # Метка с названием города
                city_label = QtWidgets.QLabel(city_name)
                card_layout.addWidget(city_label)

                # Создаем spacer, который будет занимать оставшееся пространство
                spacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
                card_layout.addItem(spacer)

                # Создаем метку для отображения иконки сердца
                heart_icon = QtWidgets.QLabel()
                if favorite:
                    heart_icon.setPixmap(QtGui.QPixmap("weather_app/ui/icons/ui/Heart.png"))
                    heart_icon.setStyleSheet("margin-right: 10px;")
                else:
                    heart_icon.setPixmap(QtGui.QPixmap("weather_app/ui/icons/ui/NoHeart.png"))
                    heart_icon.setStyleSheet("margin-right: 15px;")
               

                heart_icon.mousePressEvent = lambda event, \
                    city_id=city_id, \
                    heart_icon=heart_icon: self.toggle_favorite( city_id, heart_icon)
                card_layout.addWidget(heart_icon)

                # Обработчик клика по карточке (по всей карточке)
                card_widget.mousePressEvent = lambda event, \
                    city_id=city_id, \
                    card_widget=card_widget: self.on_card_click(city_id, card_widget)

                self.city_buttons_layout.addWidget(card_widget)

    def toggle_favorite(self, city_id, heart_icon):
        """Обработчик клика по иконке сердца для добавления/удаления города из избранного."""
        # Получаем текущее состояние города из базы данных
        is_favorite = self.database.is_city_favorite(city_id)

        # Обновить информацию о городе в базе данных
        self.database.update_city_favorite(city_id, not is_favorite)

        # После обновления в базе данных, получаем новое состояние
        new_favorite_state = not is_favorite
        # Обновляем иконку в зависимости от нового состояния
        if new_favorite_state:
            heart_icon.setPixmap(QtGui.QPixmap("weather_app/ui/icons/ui/Heart.png"))
            heart_icon.setStyleSheet("margin-right: 10px;")
        else:
            heart_icon.setPixmap(QtGui.QPixmap("weather_app/ui/icons/ui/NoHeart.png"))
            heart_icon.setStyleSheet("margin-right: 15px;")
        
        # Принудительно обновляем виджет
        heart_icon.update()  # или heart_icon.repaint()


    def on_card_click(self, city_id, card_widget):
        """Обработчик клика по карточке города."""
        # Здесь можно добавить дополнительную логику, например, обновить погоду для выбранного города
        self.update_weather(city_id)

    def get_weather_data(self, city_id: int) -> dict:
        """Получает данные о погоде для заданного города."""
        try:
            return self.weather_api.fetch_weather_by_city_id(city_id)
        except Exception as e:
            print(f"Ошибка получения данных о погоде: {e}")
            return None

    def get_cities(self):
        """Получение всех городов из базы данных с заполненным ru_name."""
        return self.database.get_cities(fields=['id', 'ru_name'], ru_name=True)




    def update_weather(self, city_id: int):
        """Обновляет данные о погоде в левой секции для выбранного города."""
        # Показать экран загрузки
        self.left_section.setCurrentWidget(self.loading_widget)

        def fetch_and_update():
            weather_data = self.get_weather_data(city_id)
            QtCore.QMetaObject.invokeMethod(
                self, "update_weather_ui", QtCore.Qt.QueuedConnection, QtCore.Q_ARG(dict, weather_data)
            )

        threading.Thread(target=fetch_and_update, daemon=True).start()

    @QtCore.pyqtSlot(dict)
    def update_weather_ui(self, weather_data):
        """Обновляет UI с данными о погоде."""
        if weather_data:
            city_name = weather_data.get("name", "N/A")
            temp = weather_data.get("main", {}).get("temp", "N/A")
            description = weather_data.get("weather", [{}])[0].get("description", "N/A")

            self.city_label.setText(f"Город: {city_name}")
            self.temp_label.setText(f"Температура: {temp}°C")
            self.desc_label.setText(f"Описание: {description}")
        else:
            self.city_label.setText("Город: -")
            self.temp_label.setText("Температура: -")
            self.desc_label.setText("Описание: Не удалось загрузить данные.")

        # Показать экран с погодой
        self.left_section.setCurrentWidget(self.weather_widget)
