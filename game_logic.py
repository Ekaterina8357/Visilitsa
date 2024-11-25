import random
from typing import List, Tuple

# Слова для игры
WORDS = ["разработчик", "слон", "питон", "клавиатура", "монитор", "виселица"]

class Hangman:
    """
    Класс для представления игры Виселица.
    
    Атрибуты:
        word (str): Загаданное слово.
        guessed (List[str]): Угаданные игроком символы.
        attempts_left (int): Оставшиеся неверные попытки.
    """
    def __init__(self):
        self.word: str = random.choice(WORDS).upper()
        self.guessed: List[str] = ['_' for _ in self.word]
        self.attempts_left: int = 6
        self.incorrect_guesses: List[str] = []

    def guess_letter(self, letter: str) -> Tuple[bool, str]:
        """
        Обрабатывает букву, угаданную игроком.
        Проверяет, содержится ли буква в слове и обновляет состояние игры.

        Args:
            letter (str): Буква, которую ввел пользователь.

        Returns:
            Tuple[bool, str]: Результат попытки и сообщение.
        """
        letter = letter.upper()
        if letter in self.guessed or letter in self.incorrect_guesses:
            return False, "Эта буква уже была угадана."
    
        if letter in self.word:
            for idx, char in enumerate(self.word):
                if char == letter:
                    self.guessed[idx] = letter
            return True, "Правильная буква!"
        else:
            self.attempts_left -= 1
            self.incorrect_guesses.append(letter)
            return False, f"Неправильная буква. Осталось попыток: {self.attempts_left}"

    def is_game_over(self) -> bool:
        """Проверяет, закончилась ли игра."""
        return self.attempts_left <= 0 or '_' not in self.guessed

    def is_word_guessed(self) -> bool:
        """Проверяет, угадано ли слово полностью."""
        return '_' not in self.guessed

    def get_word(self) -> str:
        """Возвращает загаданное слово."""
        return self.word

    def get_guessed_word(self) -> str:
        """Возвращает текущее состояние угаданного слова с пробелами между буквами."""
        return ' '.join(self.guessed)
