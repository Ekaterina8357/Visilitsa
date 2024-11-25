import sys
from PyQt5.QtWidgets import QApplication
from gui import HangmanGUI

# Основная точка входа для запуска игры Виселица
if __name__ == '__main__':
    app = QApplication(sys.argv)  # Создание экземпляра приложения
    window = HangmanGUI()  # Создание главного окна игры
    window.show()  # Отображение главного окна
    sys.exit(app.exec_())  # Запуск основного цикла приложения
