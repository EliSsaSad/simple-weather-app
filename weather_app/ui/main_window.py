from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow

from weather_app.ui.menu import Menu
from weather_app.ui.pages.home_page import HomePage


class MainWindow(QMainWindow):
    """Главное окно программы."""

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Центральный виджет
        self.centralwidget = QtWidgets.QWidget(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)

        # Видимое окно
        self.visible_window = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayout.addWidget(self.visible_window)

        self.visible_window.setStyleSheet(
            """
            QWidget {
                border: 0px; 
                border-radius: 8px; 
                background-color: qlineargradient(
                    spread: pad, x1: 0, y1: 0, x2: 1, y2: 0, 
                    stop: 0 #ffe600, stop: 1 #ffe600
                );
            }
            QLineEdit {
                background: white;
                border: 2px solid #B3B3B3;
                font-family: 'Microsoft YaHei';
                border-radius: 5px;
                font-size: 20px;
                font-weight: bold;
            }
            QLineEdit:hover {
                border: 3px solid #66A3FF;
            }
            QLineEdit:focus {
                border: 3px solid #E680BD;
            }
            QLabel {
                text-align: right;
                font-family: 'Microsoft YaHei';
                font-size: 30px;
                font-weight: bold;
            }
            QPushButton {
                border: 0px;
                height: 30px;
                border-radius: 15px;
                font-family: 'Microsoft YaHei';
                font-size: 20px;
                color: white;
                background-color: qlineargradient(
                    spread: pad, x1: 0, y1: 0, x2: 1, y2: 0, 
                    stop: 0 #fbc2eb, stop: 1 #a6c1ee
                );
            }
            QPushButton:hover {
                background-color: qlineargradient(
                    spread: pad, x1: 0, y1: 0, x2: 1, y2: 0, 
                    stop: 0 #ffd2f0, stop: 1 #b0cbf8
                );
            }
            QPushButton:pressed {
                background-color: qlineargradient(
                    spread: pad, x1: 0, y1: 0, x2: 1, y2: 0, 
                    stop: 0 #e1aad2, stop: 1 #92adda
                );
            }
            """
        )

        # Страницы приложения
        page_settings = QtWidgets.QLabel(
            "Настройки", alignment=QtCore.Qt.AlignCenter
        )
        page_home = HomePage(self.visible_window)

        # Стек виджетов
        stacked_widget = QtWidgets.QStackedWidget(self.visible_window)
        stacked_widget.setContentsMargins(0, 0, 0, 0)

        # Меню
        self.menubar = Menu(self.visible_window)
        self.menubar.minimize_button.clicked.connect(self.minimize)
        self.menubar.expand_button.clicked.connect(self.maximize)
        self.menubar.exit_button.clicked.connect(self.close)
        self.menubar.installEventFilter(self)

        # Группа кнопок для управления страницами
        self.button_group = QtWidgets.QButtonGroup(self.visible_window)
        self.button_group.buttonClicked[int].connect(
            stacked_widget.setCurrentIndex
        )

        # Кнопки управления
        self.button_group.addButton(self.menubar.check_box_start)
        self.button_group.addButton(
            self.menubar.push_button_home,
            stacked_widget.addWidget(page_home),
        )
        self.button_group.addButton(
            self.menubar.push_button_settings,
            stacked_widget.addWidget(page_settings),
        )

        # Основной макет
        self.window_layout = QtWidgets.QVBoxLayout(self.visible_window)
        self.window_layout.setContentsMargins(5, 5, 5, 5)
        self.window_layout.addWidget(self.menubar)
        self.window_layout.addWidget(stacked_widget)

        # Тень для окна
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(0, 0)
        self.shadow.setBlurRadius(25)
        self.shadow.setColor(QColor(0, 0, 0))
        self.visible_window.setGraphicsEffect(self.shadow)

        # Установка центрального виджета
        self.setCentralWidget(self.centralwidget)

    def minimize(self):
        """Свернуть окно."""
        self.showMinimized()

    def maximize(self):
        """Разворачивать и сворачивать окно."""
        if self.isMaximized():
            self.visible_window.setStyleSheet(
                """
                QWidget {
                    border: 0px; 
                    border-radius: 10px; 
                    background-color: qlineargradient(
                        spread: pad, x1: 0, y1: 0, x2: 1, y2: 0, 
                        stop: 0 #ffe600, stop: 1 #ffe600
                    ); 
                    padding: 0px;
                }
                """
            )
            self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
            self.showNormal()
        else:
            self.visible_window.setStyleSheet(
                """
                QWidget {
                    border: 0px; 
                    border-radius: 0px; 
                    background-color: qlineargradient(
                        spread: pad, x1: 0, y1: 0, x2: 1, y2: 0, 
                        stop: 0 #ffe600, stop: 1 #ffe600
                    ); 
                    padding: 0px;
                }
                """
            )
            self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
            self.showMaximized()

    def eventFilter(self, obj, event):
        """Перемещение окна."""
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.dragPos = event.globalPos()
        if event.type() == QtCore.QEvent.MouseMove:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
        return True
