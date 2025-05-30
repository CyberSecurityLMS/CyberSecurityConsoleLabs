# 03_file_handling/fixed_app.py
import os
import sys

# Базовая директория, где приложение МОЖЕТ искать файлы
BASE_DIR = "user_files"
# Получаем абсолютный путь к базовой директории
ABS_BASE_DIR = os.path.abspath(BASE_DIR)

# Функция для безопасного чтения файла
def safe_read_user_file(filename):
    print(f"Запрошен файл: {filename}")

    # 1. Соединяем базовую директорию и имя файла
    user_path = os.path.join(ABS_BASE_DIR, filename)
    print(f"Предполагаемый путь: {user_path}")

    # 2. Получаем АБСОЛЮТНЫЙ канонический путь (разрешает '..', '.', симлинки)
    abs_user_path = os.path.abspath(user_path)
    print(f"Абсолютный канонический путь: {abs_user_path}")

    # 3. ИСПРАВЛЕНО: Проверяем, что полученный путь НАЧИНАЕТСЯ с базовой директории
    # os.path.commonpath можно использовать для более надежной проверки в сложных случаях
    if not abs_user_path.startswith(ABS_BASE_DIR + os.sep):
         # Доп. проверка на случай, если запрошен сам BASE_DIR
         if abs_user_path != ABS_BASE_DIR:
            print(f"Ошибка доступа: Попытка чтения файла вне '{BASE_DIR}'. Путь: {abs_user_path}")
            return None

    # 4. Проверяем, что это существующий ФАЙЛ (не директория, не ссылка и т.д.)
    if not os.path.exists(abs_user_path):
        print(f"Ошибка: Файл не найден по пути {abs_user_path}")
        return None
    if not os.path.isfile(abs_user_path):
        print(f"Ошибка: Путь {abs_user_path} не является файлом.")
        return None

    # 5. Если все проверки пройдены, читаем файл
    try:
        with open(abs_user_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            print("\nСодержимое файла:")
            print("-" * 20)
            print(content)
            print("-" * 20)
            return content
    except Exception as e:
        print(f"\nОшибка при чтении файла {abs_user_path}: {e}")
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
        print(f"\nИспользование: python fixed_app.py <имя_файла_внутри_{BASE_DIR}>")
        print(f"Пример (безопасный): python fixed_app.py welcome.txt")
        print(f"Пример (Path Traversal - БУДЕТ ЗАБЛОКИРОВАН): python fixed_app.py ../../../../../etc/passwd")
        sys.exit(1)

    requested_file = sys.argv[1]
    safe_read_user_file(requested_file) 