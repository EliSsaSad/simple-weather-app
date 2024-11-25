"""Главное окно программы"""

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QMainWindow
from weather_app.ui.menu import Menu
from weather_app.ui.pages.home_page.home_page import HomePage
from weather_app.ui.pages.setting_pages.setting_pages import SettingPage


class MainWindow(QMainWindow):
    """
    Главное окно программы.

    Attributes:
        centralwidget (QtWidgets.QWidget):
            Центральный виджет окна.
        horizontalLayout (QtWidgets.QHBoxLayout):
            Главный горизонтальный макет.
        visible_window (QtWidgets.QWidget):
            Видимое окно программы.
        menubar (Menu):
            Главное меню программы.
        button_group (QtWidgets.QButtonGroup):
            Группа кнопок для переключения страниц.
        shadow (QtWidgets.QGraphicsDropShadowEffect):
            Эффект тени для окна.
        window_layout (QtWidgets.QVBoxLayout):
            Основной вертикальный макет для меню и контента.
    """

    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        """
        Инициализирует главное окно программы.

        Args:
            parent (QtWidgets.QWidget | None):
                Родительский виджет (по умолчанию None).
        """
        super().__init__(parent)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Центральный виджет
        self.centralwidget: QtWidgets.QWidget = QtWidgets.QWidget(self)
        self.horizontalLayout: QtWidgets.QHBoxLayout = (
            QtWidgets.QHBoxLayout(self.centralwidget)
        )

        # Видимое окно
        self.visible_window: QtWidgets.QWidget = (
            QtWidgets.QWidget(self.centralwidget)
        )
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
        page_settings: SettingPage = SettingPage(self.visible_window)
        page_home: HomePage = HomePage(self.visible_window)

        # Стек виджетов
        stacked_widget: QtWidgets.QStackedWidget = (
            QtWidgets.QStackedWidget(self.visible_window)
        )
        stacked_widget.setContentsMargins(0, 0, 0, 0)

        # Меню
        self.menubar: Menu = Menu(self.visible_window)
        self.menubar.minimize_button.clicked.connect(self.minimize)
        self.menubar.expand_button.clicked.connect(self.maximize)
        self.menubar.exit_button.clicked.connect(self.close)
        self.menubar.installEventFilter(self)

        # Группа кнопок для управления страницами
        self.button_group: QtWidgets.QButtonGroup = (
            QtWidgets.QButtonGroup(self.visible_window)
        )
        self.button_group.buttonClicked[int].connect(
            stacked_widget.setCurrentIndex
        )

        # Кнопки управления
        self.button_group.addButton(
            self.menubar.push_button_home,
            stacked_widget.addWidget(page_home),
        )
        self.button_group.addButton(
            self.menubar.push_button_settings,
            stacked_widget.addWidget(page_settings),
        )

        # Основной макет
        self.window_layout: QtWidgets.QVBoxLayout = (
            QtWidgets.QVBoxLayout(self.visible_window)
        )
        self.window_layout.setContentsMargins(5, 5, 5, 5)
        self.window_layout.addWidget(self.menubar)
        self.window_layout.addWidget(stacked_widget)

        # Тень для окна
        self.shadow: QtWidgets.QGraphicsDropShadowEffect = (
            QtWidgets.QGraphicsDropShadowEffect(self)
        )
        self.shadow.setOffset(0, 0)
        self.shadow.setBlurRadius(25)
        self.shadow.setColor(QColor(0, 0, 0))
        self.visible_window.setGraphicsEffect(self.shadow)

        # Установка центрального виджета
        self.setCentralWidget(self.centralwidget)

    def minimize(self) -> None:
        """Свернуть окно."""
        self.showMinimized()

    def maximize(self) -> None:
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

    def eventFilter(self, obj: QtCore.QObject, event: QtCore.QEvent) -> bool:
        """Перемещение окна.

        Args:
            obj (QtCore.QObject): Объект, к которому применяется фильтр.
            event (QtCore.QEvent): Событие.

        Returns:
            bool: True, если событие обработано.
        """
        if event.type() == QtCore.QEvent.MouseButtonPress:
            self.dragPos = event.globalPos()
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

                # Сохраняем относительную позицию курсора внутри окна
                cursor_offset = self.dragPos - self.frameGeometry().topLeft()

                # Возвращаем окно в нормальное состояние
                self.showNormal()

                # Перемещаем окно под текущий курсор
                self.move(self.dragPos - cursor_offset)

        if event.type() == QtCore.QEvent.MouseMove:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()
        return True
