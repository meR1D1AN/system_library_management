 # Система управления библиотекой

## Описание

Это консольное приложение для управления библиотекой книг. Оно позволяет добавлять, удалять, искать и отображать книги, а также изменять их статус.

## Функционал

1. **Добавление книги**: Пользователь вводит название, автора и год издания книги. Книга добавляется в библиотеку с уникальным id и статусом "в наличии".
2. **Удаление книги**: Пользователь вводит id книги, которую нужно удалить.
3. **Поиск книги**: Пользователь может искать книги по названию, автору или году издания.
4. **Отображение всех книг**: Приложение выводит список всех книг с их id, названием, автором, годом издания и статусом.
5. **Изменение статуса книги**: Пользователь вводит id книги и новый статус 1 = в наличии, 2 = выдана.

## Установка и запуск

1. Склонируйте репозиторий:
   ```sh
   git clone https://github.com/meR1D1AN/system_library_management.git

2. Перейдите в директорию проекта:
   ```sh
   cd library_management
3. Запустите приложение
   ```sh
   python main.py
   
## Документация

### Классы и методы

**Book**: Класс, представляющий книгу.

 - __init__(self, title, author, year, status="в наличии"): Инициализация книги.
 - to_dict(): Преобразование книги в словарь.  

**Library**: Класс, представляющий библиотеку.
 
 - __init__(self, file_path="books.json"): Инициализация библиотеки.
 - load_books(): Загрузка книг из файла.
 - save_books(): Сохранение книг в файл.
 - add_book(): Добавление книги.
 - delete_book(): Удаление книги.
 - search_books(): Поиск книг.
 - display_books(): Отображение всех книг.
 - change_status(): Изменение статуса книги.

# Тестирование
   ```sh
   python -m unittest test_library.py
