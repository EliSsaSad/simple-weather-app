import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from weather_app.ui.main_window import MainWindow


def main() -> None:
    """
    Точка входа в приложение. Настраивает и запускает главное окно.

     Steps:
        1. Создаёт экземпляр QApplication.
        2. Устанавливает иконку приложения.
        3. Инициализирует и отображает главное окно приложения.
        4. Запускает главный цикл событий.

    Return:
        None
    """
    # Создаем экземпляр приложения
    app = QApplication(sys.argv)

    # Устанавливаем иконку приложения
    app.setWindowIcon(QIcon("weather_app/ui/icons/ui/Home.png"))

    # Создаем и показываем главное окно
    window = MainWindow()
    window.resize(1500, 900)
    window.show()

    # Запускаем главный цикл приложения
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
