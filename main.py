from src.library import Library, validate_year, Color


def main():
    library = Library()
    while True:
        print("\n--- Система управления библиотекой ---")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        try:
            choice = input("Выберите действие (1-6): ")

            if choice == '1':
                title = input("Введите название книги: ").strip()
                author = input("Введите автора книги: ").strip()
                # Функция валидации года
                while True:
                    year_str = input("Введите год издания: ").strip()

                    try:
                        # Валидация года
                        year = validate_year(year_str)
                        break
                    except ValueError as e:
                        print(e)

                if not all([title, author]):
                    print(f"{Color.RED}Название и автор должны быть заполнены!{Color.END}")
                    continue

                library.add_book(title, author, year)

            elif choice == '2':
                try:
                    book_id = int(input("Введите ID книги для удаления: "))
                    library.remove_book(book_id)
                except ValueError:
                    print(f"{Color.RED}ID должен быть числом!{Color.END}")

            elif choice == '3':
                query = input("Введите название, автора или год для поиска: ")
                results = library.search_books(query)
                if results:
                    for book in results:
                        print(
                            f"ID: {Color.GREEN}{book.id}{Color.END}, "
                            f"Название: {Color.GREEN}{book.title}{Color.END}, "
                            f"Автор: {Color.GREEN}{book.author}{Color.END}, "
                            f"Год: {Color.GREEN}{book.year}{Color.END}, "
                            f"Статус: {Color.GREEN}{book.status}{Color.END}")
                else:
                    print(f"{Color.RED}Книги не найдены.{Color.END}")

            elif choice == '4':
                library.display_books()

            elif choice == '5':
                try:
                    book_id = int(input("Введите ID книги для изменения статуса: "))
                    new_status = input(f"Введите новый статус, {Color.U}{Color.GREEN}1{Color.END}{Color.U_} = в наличии, {Color.U}{Color.GREEN}2{Color.END}{Color.U_} = выдана: ")
                    library.change_status(book_id, new_status)
                except ValueError:
                    print(f"{Color.RED}ID должен быть числом!{Color.END}")

            elif choice == '6':
                print(f"{Color.GREEN}{Color.U}Завершение работы...{Color.U_}{Color.END}")
                break

            else:
                print(f"{Color.RED}Некорректный выбор. Пожалуйста, выберите действие от 1 до 6{Color.END}")

        except Exception as e:
            print(f"{Color.RED}Произошла ошибка: {e}{Color.END}")


if __name__ == "__main__":
    main()
