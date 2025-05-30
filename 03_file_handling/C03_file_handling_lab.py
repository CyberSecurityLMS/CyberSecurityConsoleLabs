# Уязвимое приложение - лабораторная работа по Path Traversal
# Студенту нужно исправить этот файл, добавив проверку пути к файлу

import os
import sys

# Базовая директория, где приложение "должно" искать файлы
BASE_DIR = "user_files"

def read_user_file(filename):
    """
    Уязвимая функция чтения файла.
    
    ЗАДАНИЕ ДЛЯ СТУДЕНТА:
    Эта функция не проверяет, что итоговый путь находится внутри BASE_DIR.
    Тебе нужно:
    1. Получить абсолютный путь к BASE_DIR (os.path.abspath)
    2. Получить абсолютный путь к запрошенному файлу
    3. Проверить, что итоговый путь начинается с BASE_DIR
    4. Возвращать ошибку, если путь выходит за пределы BASE_DIR
    
    После исправления тесты из test_file_handling.py должны пройти успешно.
    """
    # TODO: Добавьте проверку пути здесь
    file_path = os.path.join(BASE_DIR, filename)
    print(f"Попытка чтения файла: {file_path}")

    try:
        abs_path = os.path.abspath(file_path)
        print(f"Абсолютный путь: {abs_path}")

        if not os.path.exists(abs_path):
            print(f"Ошибка: Файл не найден по пути {abs_path}")
            return None
        if not os.path.isfile(abs_path):
            print(f"Ошибка: Путь {abs_path} не является файлом.")
            return None

        with open(abs_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            print("\nСодержимое файла:")
            print("-" * 20)
            print(content)
            print("-" * 20)
            return content
    except Exception as e:
        print(f"\nОшибка при чтении файла {file_path}: {e}")
        return None

if __name__ == "__main__":
    # Создаем тестовую директорию и файл
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
        print(f"Создана директория: {BASE_DIR}")
    if not os.path.exists(os.path.join(BASE_DIR, "welcome.txt")):
        with open(os.path.join(BASE_DIR, "welcome.txt"), "w") as f:
            f.write("Это безопасный файл внутри user_files.")
        print(f"Создан тестовый файл: {os.path.join(BASE_DIR, 'welcome.txt')}")

    if len(sys.argv) != 2:
        print(f"\nИспользование: python vulnerable_app.py <имя_файла>")
        print(f"Пример (безопасный): python vulnerable_app.py welcome.txt")
        print(f"Пример (уязвимость): python vulnerable_app.py ../../../../etc/passwd")
        sys.exit(1)

    requested_file = sys.argv[1]
    read_user_file(requested_file)