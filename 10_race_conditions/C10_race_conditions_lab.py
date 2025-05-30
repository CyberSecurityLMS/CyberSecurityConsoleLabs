# Уязвимое приложение - лабораторная работа по гонке состояний
# Студенту нужно исправить этот файл, добавив механизм синхронизации

import sys
import os
import time
import threading

FILENAME = "shared_resource.txt"
ACTION_DELAY_SECONDS = 0.5

def perform_action(thread_id):
    """
    Уязвимая функция работы с файлом
    
    ЗАДАНИЕ ДЛЯ СТУДЕНТА:
    Эта функция содержит уязвимость типа TOCTOU (Time-of-Check to Time-of-Use).
    Тебе нужно:
    1. Добавить механизм синхронизации (блокировку)
    2. Объединить проверку и использование файла в атомарную операцию
    3. Обеспечить безопасное создание файла при необходимости
    
    После исправления тесты из test_race_condition.py должны пройти успешно.
    """
    print(f"[Поток {thread_id}] Проверка файла '{FILENAME}'...")

    # TODO: Добавьте механизм синхронизации здесь
    file_exists = os.path.exists(FILENAME)

    if file_exists:
        print(f"[Поток {thread_id}] Файл существует. Ожидание {ACTION_DELAY_SECONDS} сек...")
        time.sleep(ACTION_DELAY_SECONDS)

        try:
            with open(FILENAME, "a") as f:
                f.write(f"Запись от потока {thread_id}\n")
            print(f"[Поток {thread_id}] Запись успешна.")
        except FileNotFoundError:
            print(f"[Поток {thread_id}] ОШИБКА: Файл не найден! (Race Condition)")
    else:
        print(f"[Поток {thread_id}] Файл не существует при проверке.")

if __name__ == "__main__":
    num_threads = 3
    if len(sys.argv) > 1:
        try:
            num_threads = int(sys.argv[1])
        except ValueError:
            print("Ошибка: Количество потоков должно быть числом.")
            sys.exit(1)

    print(f"Запуск {num_threads} потоков для доступа к '{FILENAME}'...")
    
    # Создаем файл перед запуском
    with open(FILENAME, "w") as f:
        f.write("Начальный контент.\n")

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=perform_action, args=(i+1,))
        threads.append(thread)
        thread.start()

    # Ждем завершения потоков
    for thread in threads:
        thread.join()

    print("\nВсе потоки завершены.")
    
    # Показываем содержимое файла
    with open(FILENAME, "r") as f:
        print(f"\nСодержимое файла:\n{f.read()}")
    
    # Удаляем файл
    os.remove(FILENAME)