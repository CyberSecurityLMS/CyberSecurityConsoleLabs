# 10_race_conditions/fixed_app.py
import sys
import os
import time
import threading

FILENAME = "shared_resource_fixed.txt"
ACTION_DELAY_SECONDS = 0.1 # Можно уменьшить задержку
NUM_THREADS = 5

# Создаем блокировку для синхронизации доступа к файлу
# Важно: Блокировка должна быть ОДНА на всех потоков, обращающихся к ресурсу
file_lock = threading.Lock()

def perform_action_safe(thread_id):
    """Выполняет действие с файлом, используя блокировку."""
    print(f"[Поток {thread_id}] Ожидание блокировки...")

    # --- Исправление: Использование блокировки ---
    with file_lock:
        # Код внутри этого блока выполняется только одним потоком в один момент времени
        print(f"[Поток {thread_id}] Блокировка получена. Доступ к файлу '{FILENAME}'...")
        # Имитируем какую-то работу с ресурсом
        time.sleep(ACTION_DELAY_SECONDS)

        try:
            # Операция записи теперь защищена блокировкой.
            # Используем 'a' (append), которая также создаст файл, если его нет.
            with open(FILENAME, "a") as f:
                f.write(f"Запись от потока {thread_id} под блокировкой\n")
            print(f"[Поток {thread_id}] Запись успешна.")

        except Exception as e:
             # Ошибки все еще возможны (например, нет прав на запись), но не FileNotFoundError из-за гонки
             print(f"[Поток {thread_id}] Ошибка записи под блокировкой: {e}")

        print(f"[Поток {thread_id}] Блокировка освобождена.")
    # --- Конец блока блокировки ---


def cleanup():
    """Удаляет файл, если он существует."""
    if os.path.exists(FILENAME):
        try:
            # Блокировка нужна и здесь, если другие потоки еще могут работать
            with file_lock:
                 if os.path.exists(FILENAME): # Проверяем еще раз под блокировкой
                    os.remove(FILENAME)
                    print(f"[Main] Файл '{FILENAME}' удален.")
        except Exception as e:
            print(f"[Main] Ошибка при удалении файла: {e}")

if __name__ == "__main__":
    num_threads_to_run = NUM_THREADS
    if len(sys.argv) > 1:
        try:
            num_threads_to_run = int(sys.argv[1])
        except ValueError:
            print("Ошибка: Количество потоков должно быть числом.")
            sys.exit(1)

    print(f"Запуск {num_threads_to_run} потоков для БЕЗОПАСНОГО доступа к '{FILENAME}'...")
    # Удаляем файл перед запуском, если он остался от прошлого раза
    cleanup()

    threads = []
    for i in range(num_threads_to_run):
        # Передаем ту же самую блокировку во все потоки
        thread = threading.Thread(target=perform_action_safe, args=(i+1,))
        threads.append(thread)
        thread.start()

    # Ждем завершения всех потоков
    for thread in threads:
        thread.join()

    print("\n[Main] Все потоки завершены.")
    # Посмотрим на результат
    if os.path.exists(FILENAME):
        print(f"\n--- Содержимое файла {FILENAME}: ---")
        try:
            with open(FILENAME, "r") as f:
                print(f.read())
        except Exception as e:
            print(f"Ошибка чтения файла: {e}")
        print("------------------------------------")
        # Очистка в конце
        cleanup()
    else:
        print(f"[Main] Файл {FILENAME} не был создан (возможно, были ошибки).") 