from datetime import datetime
import json
import os


class Book:
    """
    Инициализирует книгу.
    :param title: Название книги
    :type title: str
    :param author: автор книги
    :type author: str
    :param year: год издания
    :type year: int
    :param status: статус книги (по умолчанию "в наличии"), может быть "в наличии" или "выдана"
    :type status: str
    :param book_id: ID книги, может быть None, если книга не была добавлена в библиотеку
    :type book_id: int or None
    """

    def __init__(self, title: str, author: str, year: int, status="в наличии", book_id=None):
        self.id = book_id if book_id is not None else None
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self):
        """
        Возвращает словарь, содержащий информацию о книге.

        :return: словарь, содержащий информацию о книге
        :rtype: dict[str, str | int]
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }


class Library:
    def __init__(self, filename='library.json'):
        """
        Инициализирует библиотеку.
        :param filename: имя файла для хранения данных библиотеки
        :type filename: str
        """
        self.filename = filename
        self.books = self.load_books()

    def load_books(self):
        """
        Загружает книги из JSON файла.
        :return: список книг
        :rtype: list[Book]
        """
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    books_data = json.load(f)
                    return [Book(
                        title=book['title'],
                        author=book['author'],
                        year=book['year'],
                        status=book['status'],
                        book_id=book['id']
                    ) for book in books_data]
            except (json.JSONDecodeError, KeyError) as e:
                print(f"{Color.RED}Ошибка при загрузке данных: {e}{Color.END}")
                # Если файл пустой или поврежден, возвращаем пустой список
                return []
        return []

    def save_books(self):
        """
        Сохраняет книги в файл.
        :return: None
        """
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump([book.to_dict() for book in self.books], f, ensure_ascii=False, indent=4)

    def add_book(self, title: str, author: str, year: int):
        """
        Добавляет книгу в библиотеку.
        :param title: Название книги
        :type title: str
        :param author: автор книги
        :type author: str
        :param year: год издания
        :type year: int
        :return: None
        """
        # Находим максимальный существующий ID или используем 1, если книг нет
        book_id = max([book.id for book in self.books], default=0) + 1
        new_book = Book(title=title, author=author, year=year, book_id=book_id)
        self.books.append(new_book)
        self.save_books()
        print(f"{Color.GREEN}Книга добавлена с ID {book_id}{Color.END}")

    def remove_book(self, book_id: int):
        """
        Удаляет книгу из библиотеки по заданному ID.
        :param book_id: ID книги, которую нужно удалить
        :type book_id: int
        :return: None
        """
        for book in self.books:
            if book.id == book_id:
                self.books.remove(book)
                self.save_books()
                print(f"{Color.GREEN}Книга с ID {book_id} удалена.{Color.END}")
                return
        print(f"{Color.RED}Книга с таким ID не найдена.{Color.END}")

    def search_books(self, query):
        """
        Ищет книги по заданной строке.
        :param query: строка, которую нужно найти в книге
        :type query: str
        :return: список книг, удовлетворяющих запросу
        :rtype: list[Book]
        """
        query = query.lower()
        results = [book for book in self.books if
                   query in book.title.lower() or
                   query in book.author.lower() or
                   query == str(book.year)]
        return results

    def display_books(self):
        """
        Отображает все книги в библиотеке.
        :return: None
        """
        if not self.books:
            print(f"{Color.RED}Библиотека пуста.{Color.END}")
            return
        for book in self.books:
            print(
                f"ID: {Color.GREEN}{book.id}{Color.END}, "
                f"Название: {Color.GREEN}{book.title}{Color.END}, "
                f"Автор: {Color.GREEN}{book.author}{Color.END}, "
                f"Год: {Color.GREEN}{book.year}{Color.END}, "
                f"Статус: {Color.GREEN}{book.status}{Color.END}"
            )

    def change_status(self, book_id: int, new_status: str):
        """
        Изменяет статус книги по ее ID.
        :param book_id: ID книги, статус которой нужно изменить
        :type book_id: int
        :param new_status: новый статус книги (1 - в наличии, 2 - выдана)
        :type new_status: str
        :return: None
        """
        # Преобразование числового ввода в текстовый статус
        status_map = {
            "1": "в наличии",
            "2": "выдана"
        }

        for book in self.books:
            if book.id == book_id:
                # Проверяем, является ли введенный статус допустимым
                if new_status in status_map:
                    # Преобразуем числовой статус в текстовый
                    text_status = status_map[new_status]
                    book.status = text_status
                    self.save_books()
                    print(
                        f"Статус книги с ID {Color.GREEN}{book_id}{Color.END} изменен на {Color.GREEN}{text_status}{Color.END}.")
                    return
                else:
                    print(f"{Color.RED}Некорректный статус. Доступные статусы: 1 - в наличии, 2 - выдана.{Color.END}")
                    return
        print(f"{Color.RED}Книга с таким ID не найдена.{Color.END}")


class Color:
    """
    Класс для изменения цвета текста в консоли и подчеркивания
    """
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'
    U = '\033[4m'
    U_ = '\033[0m'


def validate_year(year: str) -> int:
    """
    Проверяет корректность введенного года.
    :param year: Год в виде строки
    :type year: str
    :return: Валидный год
    :rtype: int
    :raises ValueError: Если год некорректен
    """
    MIN_YEAR = 1800
    MAX_YEAR = datetime.now().year

    try:
        # Преобразуем год в целое число
        year_int = int(year)
        # Проверки:
        # 1. Год должен быть положительным числом и не может быть меньше 1800 года
        # 2. Год не должен превышать текущий год
        if year_int < MIN_YEAR:
            raise ValueError(f"{Color.RED}Год не может быть меньше {MIN_YEAR}!{Color.END}")

        if year_int > MAX_YEAR:
            raise ValueError(f"{Color.RED}Год не может быть больше текущего ({MAX_YEAR})!{Color.END}")

        return year_int

    except ValueError as e:
        # Перехватываем ошибки преобразования или наши собственные
        if "invalid literal" in str(e):
            raise ValueError(f"{Color.RED}Год должен быть числом!{Color.END}")
        raise
