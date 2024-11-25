import sys
import os
from game_logic import Hangman  # Импортируем игровой класс Hangman для тестирования
import unittest

# Добавляем путь к родительской директории, чтобы Python смог найти game_logic.py
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.insert(0, parent_dir)


class TestHangman(unittest.TestCase):
    """
    Класс для тестирования функциональности игры Виселица.
    Содержит несколько методов для проверки работы игровой логики.
    """

    def setUp(self):
        """
        Метод, выполняющий начальную настройку перед каждым тестом.
        Создает экземпляр класса Hangman и задает определенное слово для тестов.
        """
        self.game = Hangman()
        self.game.word = "ПИТОН"  # Устанавливаем слово, чтобы было предсказуемо для тестов
        self.game.guessed = ['_' for _ in self.game.word]  # Скрываем все буквы для начала игры (соответствует длине слова)
        self.game.attempts_left = 6  # Устанавливаем начальное количество попыток

    def test_correct_guess(self):
        """
        Тестирует случай, когда игрок угадывает правильную букву.
        Проверяет, что состояние слова обновляется правильно.
        """
        result, message = self.game.guess_letter('П')  # Пробуем угадать первую букву
        self.assertTrue(result)  # Проверяем, что результат положительный (буква была в слове)
        self.assertEqual(self.game.get_guessed_word(), 'П _ _ _ _')  # Проверяем состояние слова

    def test_incorrect_guess(self):
        """
        Тестирует случай, когда игрок угадывает неверную букву.
        Проверяет, что количество оставшихся попыток уменьшается на 1.
        """
        result, message = self.game.guess_letter('Х')  # Пробуем угадать букву, которой нет в слове
        self.assertFalse(result)  # Проверяем, что результат отрицательный (буквы нет в слове)
        self.assertEqual(self.game.attempts_left, 5)  # Убедимся, что количество попыток уменьшилось

    def test_game_over(self):
        """
        Тестирует, заканчивается ли игра, когда попытки закончились.
        Проверяет корректность состояния после окончания попыток.
        """
        self.game.attempts_left = 1  # Устанавливаем, что осталась одна попытка
        self.game.guess_letter('Х')  # Пробуем угадать неверную букву
        self.assertTrue(self.game.is_game_over())  # Проверяем, что игра завершена

    def test_multiple_incorrect_guesses(self):
        """
        Тестирует случай нескольких неверных попыток.
        Проверяет, что количество попыток уменьшается корректно после каждой неверной попытки.
        """
        self.game.guess_letter('А')  # Неправильная попытка
        self.game.guess_letter('Б')  # Неправильная попытка
        self.game.guess_letter('В')  # Неправильная попытка
        self.assertEqual(self.game.attempts_left, 3)  # Проверяем, что осталось 3 попытки

    def test_full_word_guess(self):
        """
        Тестирует процесс полного угадывания слова.
        Проверяет, что игра корректно завершает угаданный результат и отображает угаданное слово.
        """
        for letter in "ПИТОН":  # Проходимся по всем буквам в слове "ПИТОН"
            result, message = self.game.guess_letter(letter)
            print(f"Угадываем букву: {letter}")  # Для отладки — отображаем текущую букву
            print(f"Сообщение: {message}")  # Для отладки — отображаем сообщение
            print(f"Текущее состояние слова: {self.game.get_guessed_word()}")  # Для отладки — состояние слова
            self.assertTrue(result)  # Проверяем, что каждая буква правильно угадана
        self.assertTrue(self.game.is_word_guessed())  # Проверяем, что все слово угадано
        self.assertEqual(self.game.get_guessed_word(), 'П И Т О Н')  # Проверяем, что слово полностью угадано

    def test_repeated_guess(self):
        """
        Тестирует повторное угадывание уже угаданной буквы.
        Проверяет, что сообщение правильно отображает, что буква уже была угадана.
        """
        self.game.guess_letter('П')  # Угадываем букву "П"
        result, message = self.game.guess_letter('П')  # Пробуем угадать ту же букву снова
        self.assertFalse(result)  # Проверяем, что результат отрицательный (буква уже угадана)
        self.assertEqual(message, "Эта буква уже была угадана.")  # Проверяем сообщение пользователю

if __name__ == '__main__':
    # Запускаем все тесты
    unittest.main()
