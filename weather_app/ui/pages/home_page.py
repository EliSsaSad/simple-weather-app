"""Главная страница приложения"""

from PyQt5 import QtWidgets, QtCore


class HomePage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.init_ui()

    def init_ui(self):
        # Основной layout
        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(15)

        # Левая секция
        self.left_section = self.create_section()
        self.main_layout.addWidget(self.left_section)

        # Правая секция
        self.right_section = self.create_section()
        self.main_layout.addWidget(self.right_section)

    def create_section(self):
        """Создает секцию с заданными стилями."""
        section = QtWidgets.QWidget(self)
        section.setStyleSheet(
            """
            QWidget {
                border-radius: 5px;
                background-color: #f0f0f3;
            }
            """
        )
        section.setMinimumSize(200, 300)  # Минимальные размеры для секций
        return section


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    home_page = HomePage()
    home_page.resize(600, 400)
    home_page.show()
    sys.exit(app.exec_())
