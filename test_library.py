import os
import tempfile
import unittest
from io import StringIO
import sys

from library import Library
from library import validate_year



class TestLibrarySystem(unittest.TestCase):

    def setUp(self):
        # Создаем временный файл для каждого теста
        self.temp_file = tempfile.mktemp(suffix='.json')
        self.library = Library(filename=self.temp_file)
        self.library.books = []  # Начинаем с пустой библиотеки

    def tearDown(self):
        # Удаляем временный файл
        try:
            if os.path.exists(self.temp_file):
                os.remove(self.temp_file)
        except Exception as e:
            print(f"Ошибка при удалении файла: {e}")

    def test_add_book_valid(self):
        self.library.add_book("Задание", "Никита Шидогубов", 2024)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Задание")

    def test_add_book_invalid_year(self):
        with self.assertRaises(ValueError):
            validate_year("1700")

        with self.assertRaises(ValueError):
            validate_year("2050")

        with self.assertRaises(ValueError):
            validate_year("abc")

    def test_remove_book(self):
        self.library.add_book("Задание", "Никита Шидогубов", 2024)
        book_id = self.library.books[0].id
        self.library.remove_book(book_id)
        self.assertEqual(len(self.library.books), 0)

    def test_remove_book_not_found(self):
        output = StringIO()
        sys.stdout = output
        self.library.remove_book(999)  # Удаляем книгу с несуществующим ID
        sys.stdout = sys.__stdout__
        self.assertIn("Книга с таким ID не найдена.", output.getvalue())

    def test_search_books(self):
        self.library.add_book("Задание", "Никита Шидогубов", 2024)
        results = self.library.search_books("2024")
        self.assertEqual(len(results), 1)

        results = self.library.search_books("Никита Шидогубов")
        self.assertEqual(len(results), 1)

        results = self.library.search_books("2000")
        self.assertEqual(len(results), 0)

    def test_change_status(self):
        self.library.add_book("Задание", "Никита Шидогубов", 2024)
        book_id = self.library.books[0].id
        self.library.change_status(book_id, 1)
        self.assertEqual(self.library.books[0].status, "в наличии")

    def test_change_status_invalid(self):
        self.library.add_book("Задание", "Никита Шидогубов", 2024)
        book_id = self.library.books[0].id
        output = StringIO()
        sys.stdout = output
        self.library.change_status(book_id, 3)  # Некорректный статус
        sys.stdout = sys.__stdout__
        self.assertIn("Некорректный статус. Доступные статусы: 1 - в наличии, 2 - выдана.", output.getvalue())

    def test_display_books(self):
        output = StringIO()
        sys.stdout = output
        self.library.add_book("Задание", "Никита Шидогубов", 2024)
        self.library.display_books()
        sys.stdout = sys.__stdout__
        self.assertIn("ID: ", output.getvalue())  # Проверяем, что вывод содержит ID книги


if __name__ == '__main__':
    unittest.main()
