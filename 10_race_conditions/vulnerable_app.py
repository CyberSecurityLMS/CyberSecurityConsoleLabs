# 10_race_conditions/vulnerable_app.py
import sys
import os
import time
import threading # Для имитации параллельного доступа

FILENAME = "shared_resource.txt"
ACTION_DELAY_SECONDS = 0.5 # Имитация времени между проверкой и действием

def perform_action(thread_id):
    """Проверяет файл, ждет, затем пишет."""
    print(f"[Поток {thread_id}] Проверка файла '{FILENAME}'...")

    # --- TOCTOU Уязвимость ---
    # 1. Проверка (Time-of-Check)
    file_exists = os.path.exists(FILENAME)

    if file_exists:
        print(f"[Поток {thread_id}] Файл существует. Ожидание {ACTION_DELAY_SECONDS} сек...")
        time.sleep(ACTION_DELAY_SECONDS) # Имитируем задержку

        # 2. Действие (Time-of-Use)
        print(f"[Поток {thread_id}] Попытка записи в файл '{FILENAME}'...")
        try:
            # Эта операция может упасть, если другой поток удалил файл
            # между проверкой os.path.exists() и этим моментом.
            with open(FILENAME, "a") as f:
                f.write(f"Запись от потока {thread_id}\n")
            print(f"[Поток {thread_id}] Запись успешна.")
        except FileNotFoundError:
            print(f"[Поток {thread_id}] ОШИБКА: Файл '{FILENAME}' не найден во время записи! (Race Condition)")
        except Exception as e:
             print(f"[Поток {thread_id}] Неожиданная ошибка записи: {e}")
    else:
         print(f"[Поток {thread_id}] Файл '{FILENAME}' не существует при проверке.")
         # Можно было бы создать файл здесь, но это другая логика

def cleanup():
    """Удаляет файл, если он существует."""
    if os.path.exists(FILENAME):
        try:
            os.remove(FILENAME)
            print(f"[Main] Файл '{FILENAME}' удален.")
        except Exception as e:
            print(f"[Main] Ошибка при удалении файла: {e}")

if __name__ == "__main__":
    num_threads = 3 # Количество потоков для имитации гонки
    if len(sys.argv) > 1:
        try:
            num_threads = int(sys.argv[1])
        except ValueError:
            print("Ошибка: Количество потоков должно быть числом.")
            sys.exit(1)

    print(f"Запуск {num_threads} потоков для доступа к '{FILENAME}'...")
    # Создаем файл перед запуском потоков для демонстрации
    with open(FILENAME, "w") as f:
        f.write("Начальный контент.\n")
    print(f"[Main] Файл '{FILENAME}' создан.")

    threads = []
    for i in range(num_threads):
        thread = threading.Thread(target=perform_action, args=(i+1,))
        threads.append(thread)
        thread.start()

    # Даем потокам время поработать
    # В реальной эксплуатации гонка может зависеть от планировщика ОС
    # Можно добавить имитацию удаления файла другим "процессом" во время работы потоков
    # time.sleep(ACTION_DELAY_SECONDS / 2)
    # print("\n[ИМИТАЦИЯ] ВНЕШНЕЕ УДАЛЕНИЕ ФАЙЛА!\n")
    # cleanup() # Раскомментируйте, чтобы явно вызвать гонку

    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()

    print("\n[Main] Все потоки завершены.")
    # Очистка в конце
    cleanup() 