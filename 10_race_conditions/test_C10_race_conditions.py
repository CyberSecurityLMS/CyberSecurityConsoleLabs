import pytest
import os
import time
import threading
from C10_race_conditions_lab import perform_action, FILENAME

@pytest.fixture
def setup_file():
    """Фикстура для создания тестового файла"""
    with open(FILENAME, "w") as f:
        f.write("Test content\n")
    yield
    if os.path.exists(FILENAME):
        os.remove(FILENAME)

def test_race_condition_occurrence(setup_file, capsys):
    """Тест: проверка возникновения гонки состояний"""
    # Создаем несколько потоков
    threads = []
    for i in range(3):
        thread = threading.Thread(target=perform_action, args=(i+1,))
        threads.append(thread)
        thread.start()
    
    # Даем время на выполнение
    time.sleep(1)
    
    captured = capsys.readouterr()
    assert "ОШИБКА: Файл не найден!" in captured.out, \
        "Обнаружена уязвимость гонки состояний"

def test_thread_safety_required():
    """Тест: должен использоваться механизм синхронизации"""
    with open('vulnerable_app.py', 'r') as f:
        content = f.read()
        assert 'Lock' in content or 'RLock' in content, \
            "Используйте threading.Lock для синхронизации"
        assert 'with lock' in content or 'lock.acquire()' in content, \
            "Добавьте блокировку для защиты критической секции"

def test_atomic_operations():
    """Тест: проверка и использование должны быть атомарными"""
    with open('vulnerable_app.py', 'r') as f:
        content = f.read()
        assert 'os.path.exists' not in content or 'with lock' in content, \
            "Проверка и использование файла должны быть в одной критической секции"

def test_file_creation_safe():
    """Тест: безопасное создание файла"""
    with open('vulnerable_app.py', 'r') as f:
        content = f.read()
        assert 'open(..., "a")' in content or 'open(..., "x")' in content, \
            "Используйте безопасные режимы открытия файла"

def test_no_sleep_in_critical_section():
    """Тест: в критической секции не должно быть задержек"""
    with open('vulnerable_app.py', 'r') as f:
        content = f.read()
        assert 'time.sleep' not in content or 'with lock' not in content, \
            "Не оставляйте задержки в критической секции"