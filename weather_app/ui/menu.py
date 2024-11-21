from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSize


class Menu(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.dragPos = QtCore.QPoint()
        self.setContentsMargins(0, 0, 0, 0)

        self.horizontal_layout = QtWidgets.QHBoxLayout(self)
        self.horizontal_layout.setContentsMargins(0, 0, 0, 0)

        self.central_widget = QtWidgets.QWidget(self)
        self.central_widget.setStyleSheet(
            """
            QWidget {
                border: 0px;
                border-radius: 5px;
                background-color: qlineargradient(
                    spread: pad, x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffffff, stop: 1 #ffffff
                );
            }
            """
        )
        self.central_widget.setContentsMargins(5, 5, 15, 5)
        self.horizontal_layout.addWidget(self.central_widget)

        self.menu_bar = QtWidgets.QGridLayout(self.central_widget)
        self.menu_bar.setSpacing(5)
        self.menu_bar.setContentsMargins(0, 0, 0, 0)

        # Кнопка "Домой"
        self.push_button_home = self.create_button(
            "weather_app/ui/icons/ui/Home.png",
            "Домой",
            50,
            50,
            "rgba(0, 255, 51, 100)"
        )
        self.menu_bar.addWidget(self.push_button_home, 1, 1, 1, 1)

        # Кнопка "Настройки"
        self.push_button_settings = self.create_button(
            "weather_app/ui/icons/ui/Setings.png",
            "Настройки",
            50,
            50,
            "rgba(0, 255, 51, 100)"
        )
        self.menu_bar.addWidget(self.push_button_settings, 1, 2, 1, 1, QtCore.Qt.AlignLeft)


        # Кнопка "Закрыть"
        self.exit_button = self.create_icon_button(
            "weather_app/ui/icons/ui/exit.png", 20, 20, "#000000", "#b4b2d6"
        )
        self.menu_bar.addWidget(self.exit_button, 1, 6, 1, 1)
        

        # Кнопка "Во весь экран"
        self.expand_button = self.create_icon_button(
            "weather_app/ui/icons/ui/unfold-more.png", 20, 20, "#ffe600", "#b4b2d6"
        )
        self.menu_bar.addWidget(self.expand_button, 1, 5, 1, 1)

        # Кнопка "Свернуть"
        self.minimize_button = self.create_icon_button(
            "weather_app/ui/icons/ui/minimize.png", 20, 20, "#8a8a80", "#b4b2d6"
        )
        self.menu_bar.addWidget(self.minimize_button, 1, 4, 1, 1)

    def create_button(self, icon_path, tooltip, width, height, hover_color):
        """Создать кнопку с заданным стилем."""
        button = QtWidgets.QPushButton()
        button.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        button.setIcon(QtGui.QIcon(icon_path))
        button.setIconSize(QtCore.QSize(width, height))
        button.setToolTip(tooltip)
        button.setStyleSheet(
            f"""
            QPushButton {{
                height: {height}px;
                width: {width}px;
                padding: -4px;
                background: None;
                border: None;
                border-radius: 10px;
            }}
            QPushButton::hover {{
                background-color: {hover_color};
                border-radius: 5px;
            }}
            """
        )
        return button

    def create_icon_button(self, icon_path, width, height, default_color, hover_color):
        """Создать кнопку с иконкой, которая отображается только при наведении."""
        button = QPushButton(self)
        button.setFixedSize(width, height)
        button.setStyleSheet(
            f"""
            QPushButton {{
                background-color: {default_color};
                border: none;
                border-radius: 10px;
                background-image: none;
            }}
            QPushButton::hover {{
                background-color: {hover_color};
                border-radius: 10px;
                background-image: url({icon_path});
                background-repeat: no-repeat;
                background-position: center;
                
            }}
            """
        )
        return button

