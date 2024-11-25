import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtWidgets import QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from game_logic import Hangman


class HangmanGUI(QWidget):
    """
    Класс HangmanGUI представляет графический интерфейс для игры Виселица.

    Атрибуты:
        game (Hangman): Экземпляр класса Hangman, содержащий игровую логику.
    """
    def __init__(self):
        """
        Инициализация интерфейса пользователя и создание объектов игры.
        """
        super().__init__()
        self.game = Hangman()  # Создание объекта игры
        self.initUI()

    def initUI(self):
        """
        Метод для инициализации пользовательского интерфейса.
        Устанавливает элементы управления и компоновку интерфейса.
        """
        # Устанавливаем заголовок окна
        self.setWindowTitle('Игра Виселица')
        self.setFixedSize(1200, 600)  # Устанавливаем фиксированный размер окна

        # Метка для отображения слова, которое необходимо угадать
        self.word_label = QLabel(self.game.get_guessed_word(), self)
        self.word_label.setAlignment(Qt.AlignCenter)
        self.word_label.setStyleSheet("font-size: 20px; font-weight: bold;")

        # Поле для ввода одной буквы
        self.input_line = QLineEdit(self)
        self.input_line.setMaxLength(1)  # Максимальная длина поля — одна буква
        self.input_line.setFixedHeight(40)
        self.input_line.setStyleSheet("font-size: 18px;")

        # Кнопка для подтверждения буквы
        self.guess_button = QPushButton('Угадать', self)
        self.guess_button.setFixedHeight(40)
        self.guess_button.setStyleSheet("font-size: 16px;")

        # Кнопка для начала новой игры
        self.new_game_button = QPushButton('Новая игра', self)
        self.new_game_button.setFixedHeight(40)
        self.new_game_button.setStyleSheet("font-size: 16px;")

        # Кнопка для выхода из игры
        self.quit_button = QPushButton('Выйти из игры', self)
        self.quit_button.setFixedHeight(40)
        self.quit_button.setStyleSheet("font-size: 16px;")

        # Метка для отображения изображения виселицы
        self.hangman_image = QLabel(self)
        self.update_hangman_image()  # Начальная настройка изображения
        self.hangman_image.setFixedSize(200, 200)
        self.hangman_image.setAlignment(Qt.AlignCenter)

        # Метка для отображения статуса игры (сообщения для игрока)
        self.status_label = QLabel("", self)
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 16px; color: green;")

        # Настройка компоновки элементов интерфейса
        vbox = QVBoxLayout()
        vbox.addWidget(self.word_label)
        vbox.addWidget(self.hangman_image)
        vbox.addWidget(self.input_line)
        vbox.addWidget(self.status_label)  # Добавляем метку статуса
        vbox.addWidget(self.guess_button)
        vbox.addWidget(self.new_game_button)
        vbox.addWidget(self.quit_button)
        self.setLayout(vbox)

        # Подключение сигналов к соответствующим методам
        # Кнопка "Угадать" вызывает метод make_guess
        self.guess_button.clicked.connect(self.make_guess)
        # Кнопка "Новая игра" вызывает метод start_new_game
        self.new_game_button.clicked.connect(self.start_new_game)
        # Кнопка "Выйти из игры" вызывает метод quit_game
        self.quit_button.clicked.connect(self.quit_game)

    def make_guess(self):
        """
        Метод для обработки введенной пользователем буквы.
        Проверяет, правильная ли буква, обновляет состояние игры и отображение.
        """
        letter = self.input_line.text().upper()  # Получение буквы из поля ввода
        if not letter.isalpha():  # Проверка, что введена буква
            title = 'Предупреждение!'
            message = 'Пожалуйста, введите допустимую букву.'
            QMessageBox.warning(self, title, message)
            return

        # Проверка буквы и обновление состояния игры
        correct, message = self.game.guess_letter(letter)
        # Обновление отображаемого слова
        self.word_label.setText(self.game.get_guessed_word())
        self.input_line.clear()  # Очистка поля ввода
        self.update_hangman_image()  # Обновление изображения виселицы

        # Обновляем метку статуса вместо всплывающего окна
        self.status_label.setText(message)

        # Проверка, закончилась ли игра
        if self.game.is_game_over():
            if self.game.is_word_guessed():
                self.status_label.setText('Поздравляем! Вы угадали слово!')
            else:
                self.status_label.setText(f'Вы проиграли! Загаданное слово было: {self.game.get_word()}')
            self.start_new_game()  # Начало новой игры после окончания текущей

    def start_new_game(self):
        """
        Метод для начала новой игры.
        Сбрасывает текущее состояние игры и обновляет интерфейс.
        """
        self.game = Hangman()  # Создание нового экземпляра игры
        # Сброс слова на новое
        self.word_label.setText(self.game.get_guessed_word())
        self.input_line.clear()  # Очистка поля ввода
        self.status_label.clear()  # Очистка метки статуса
        self.update_hangman_image()  # Сброс изображения виселицы

    def quit_game(self):
        """
        Метод для выхода из игры с запросом у пользователя.
        Спрашивает, хочет ли пользователь увидеть загаданное слово перед выходом.
        """
        reply = QMessageBox.question(self, 'Выход из игры', 'Вы уверены, что хотите выйти из игры? Хотите увидеть загаданное слово?', QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel, QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, 'Загаданное слово', f'Загаданное слово было: {self.game.get_word()}')
            self.close()  # Закрытие приложения
        elif reply == QMessageBox.No:
            self.close()  # Закрытие приложения без показа слова

    def update_hangman_image(self):
        """
        Метод для обновления изображения виселицы в зависимости от оставшихся попыток.
        Загружает соответствующее изображение и обновляет метку.
        """
        attempts = self.game.attempts_left  # Количество оставшихся попыток
        current_directory = os.path.dirname(os.path.abspath(__file__))  # Текущая директория
        image_path = os.path.join(current_directory, f'hangman_images/hangman_stage_{6 - attempts}.png')  # Путь к изображению
        pixmap = QPixmap(image_path)
        if not pixmap.isNull():  # Проверяем, удалось ли загрузить изображение
            self.hangman_image.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.hangman_image.setText("Изображение не найдено")  # Сообщение, если изображение не найдено
        self.hangman_image.setAlignment(Qt.AlignCenter)

if __name__ == "__main__":
    # Основная точка входа в приложение
    app = QApplication([])
    window = HangmanGUI()
    window.show()
    app.exec_()  # Запуск основного цикла обработки событий приложения
