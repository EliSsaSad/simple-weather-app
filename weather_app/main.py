import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from weather_app.ui.main_window import MainWindow

def main():
    # Создаем экземпляр приложения
    app = QApplication(sys.argv)
    
		# Устанавливаем иконку приложения
    app.setWindowIcon(QIcon("weather_app/ui/icons/ui/Home.png"))

    # Создаем и показываем главное окно
    window = MainWindow()
    window.resize(1400, 900)
    window.show()

    # Запускаем главный цикл приложения
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()