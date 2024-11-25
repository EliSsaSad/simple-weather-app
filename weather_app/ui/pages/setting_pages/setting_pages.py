"""Страница настроек приложения."""

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)
from weather_app.db.database import Database


class SettingPage(QtWidgets.QWidget):
    """
    Класс страницы настроек приложения.

    Attributes:
        database (Database):
            Экземпляр класса для взаимодействия с базой данных.
        layout (QVBoxLayout):
            Основной вертикальный компоновщик страницы.
        title (QLabel):
            Заголовок страницы настроек.
        api_key_label (QLabel):
            Метка для поля ввода API Key.
        api_key_input (QLineEdit):
            Поле ввода API Key.
        save_button (QPushButton):
            Кнопка сохранения API Key.
    """

    def __init__(self, parent: QtWidgets.QWidget):
        """
        Инициализация страницы настроек.

        Args:
            parent (QtWidgets.QWidget):
                Родительский объект (основное окно приложения).
        """
        super().__init__(parent)
        self.database: Database = Database()

        # Основной layout
        self.layout: QVBoxLayout = QVBoxLayout(self)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(2)
        self.layout.setAlignment(QtCore.Qt.AlignTop)

        # Заголовок
        self.title: QLabel = QLabel("Настройки")
        self.title.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.layout.addWidget(self.title)

        # Секция для редактирования API Key
        self.create_api_key_section()

    def create_api_key_section(self) -> None:
        """
        Создает секцию для отображения и изменения API Key.

        Эта секция содержит:
        - Поле ввода API Key.
        - Кнопку для сохранения изменений.
        """
        # Контейнер для секции (с закругленными углами и белым фоном)
        api_key_container: QtWidgets.QWidget = QtWidgets.QWidget()
        api_key_container.setStyleSheet(
            """
            QWidget {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                margin-top: 20px;
            }
            """
        )

        # Layout для этой секции
        api_key_layout: QHBoxLayout = QHBoxLayout(api_key_container)
        api_key_layout.setContentsMargins(5, 5, 5, 5)
        api_key_layout.setSpacing(10)

        # Метка для API Key
        self.api_key_label: QLabel = QLabel("API Key:")
        self.api_key_label.setStyleSheet("font-size: 16px;")
        api_key_layout.addWidget(self.api_key_label)

        # Поле ввода для API Key
        self.api_key_input: QLineEdit = QLineEdit()
        self.api_key_input.setPlaceholderText("Введите API Key")
        self.api_key_input.setText(
            self.database.get_setting('OPEN_WEATHER_MAP_API_KEY') or ""
        )
        api_key_layout.addWidget(self.api_key_input)

        # Кнопка сохранения
        self.save_button: QPushButton = QPushButton("Сохранить")
        self.save_button.setStyleSheet(
            """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 6px 12px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            """
        )
        self.save_button.clicked.connect(self.save_api_key)
        api_key_layout.addWidget(self.save_button)

        # Добавляем этот контейнер в основной layout
        self.layout.addWidget(api_key_container)

    def save_api_key(self) -> None:
        """
        Сохраняет введённый API Key в базу данных.

        Если поле ввода пустое, отображает предупреждение.
        При успешном сохранении отображает сообщение об успешной операции.
        """
        new_api_key: str = self.api_key_input.text().strip()
        if new_api_key:
            self.database.set_setting('OPEN_WEATHER_MAP_API_KEY', new_api_key)

            # Создаём QMessageBox и настраиваем его стиль
            msg_box = QtWidgets.QMessageBox()
            msg_box.setIcon(QtWidgets.QMessageBox.Information)
            msg_box.setWindowTitle("Сохранено")
            msg_box.setText("API Key успешно сохранён.")

            msg_box.exec_()
        else:
            # Аналогично для предупреждения
            msg_box = QtWidgets.QMessageBox(self)
            msg_box.setIcon(QtWidgets.QMessageBox.Warning)
            msg_box.setWindowTitle("Ошибка")
            msg_box.setText("API Key не может быть пустым.")
            msg_box.setStyleSheet(
                """
                QMessageBox {
                    background-color: #f9f9f9;
                }
                QPushButton {
                    background-color: #FF6347;
                    color: white;
                    border: none;
                    padding: 6px 12px;
                    border-radius: 4px;
                    font-size: 14px;
                }
                QPushButton:hover {
                    background-color: #FF4500;
                }
                """
            )
            msg_box.exec_()
