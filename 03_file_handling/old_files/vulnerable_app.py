# 03_file_handling/vulnerable_app.py
import os
import sys

# Базовая директория, где приложение "должно" искать файлы
BASE_DIR = "user_files"

# Функция для чтения файла
def read_user_file(filename):
    # УЯЗВИМОСТЬ: Прямое соединение пути без санации
    # Позволяет использовать "../" для выхода из BASE_DIR
    file_path = os.path.join(BASE_DIR, filename)
    print(f"Попытка чтения файла: {file_path}")

    try:
        # Используем abspath для наглядности, но уязвимость остается
        abs_path = os.path.abspath(file_path)
        print(f"Абсолютный путь: {abs_path}")

        # Проверяем, существует ли файл перед чтением
        if not os.path.exists(abs_path):
             print(f"Ошибка: Файл не найден по пути {abs_path}")
             return None
        # Дополнительная проверка на то, что это файл, а не директория
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
    # Создаем директорию и тестовый файл, если их нет
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
        print(f"Создана директория: {BASE_DIR}")
    if not os.path.exists(os.path.join(BASE_DIR, "welcome.txt")):
        with open(os.path.join(BASE_DIR, "welcome.txt"), "w") as f:
            f.write("Это безопасный файл внутри user_files.")
        print(f"Создан тестовый файл: {os.path.join(BASE_DIR, 'welcome.txt')}")

    if len(sys.argv) != 2:
        print(f"\nИспользование: python vulnerable_app.py <имя_файла_внутри_{BASE_DIR}>")
        print(f"Пример (безопасный): python vulnerable_app.py welcome.txt")
        # Примеры для Windows (могут потребовать прав)
        print(f"Пример (Path Traversal Windows): python vulnerable_app.py ../../../../../Windows/System32/drivers/etc/hosts")
        # Примеры для Linux/macOS
        print(f"Пример (Path Traversal Linux): python vulnerable_app.py ../../../../../etc/passwd")
        sys.exit(1)

    requested_file = sys.argv[1]
    read_user_file(requested_file) 