import pytest
import sys
from C02_access_control_lab import delete_user, login, USERS

@pytest.fixture(autouse=True)
def reset_users():
    """Сбрасываем состояние USERS перед каждым тестом"""
    global USERS
    USERS = {
        "alice": {"role": "admin", "password": "password123"},
        "bob": {"role": "user", "password": "password456"},
        "eve": {"role": "user", "password": "password789"},
    }
    yield
    # Восстанавливаем оригинальное состояние после теста
    USERS = {
        "alice": {"role": "admin", "password": "password123"},
        "bob": {"role": "user", "password": "password456"},
        "eve": {"role": "user", "password": "password789"},
    }

def test_admin_can_delete_user(capsys):
    """Тест: Администратор может удалять пользователей"""
    # Модифицируем функцию для теста (принимает роль)
    original_delete_user = delete_user
    def patched_delete_user(username_to_delete, caller_role="admin"):
        return original_delete_user(username_to_delete)
    
    # Пытаемся удалить пользователя
    patched_delete_user("bob")
    
    captured = capsys.readouterr()
    assert "успешно удален" in captured.out
    assert "bob" not in USERS

def test_user_cannot_delete_admin(capsys):
    """Тест: Обычный пользователь не может удалять администратора"""
    # Модифицируем функцию для теста (принимает роль)
    original_delete_user = delete_user
    def patched_delete_user(username_to_delete, caller_role="user"):
        return original_delete_user(username_to_delete)
    
    # Пытаемся удалить администратора
    patched_delete_user("alice")
    
    captured = capsys.readouterr()
    assert "успешно удален" not in captured.out
    assert "alice" in USERS
    # После исправления должно быть сообщение об ошибке доступа
    assert "Ошибка доступа" in captured.out or "администраторы" in captured.out

def test_function_accepts_caller_role():
    """Тест: Функция delete_user принимает параметр caller_role"""
    import inspect
    sig = inspect.signature(delete_user)
    assert 'caller_role' in sig.parameters, \
        "Функция delete_user должна принимать параметр caller_role"

def test_login_returns_user_data():
    """Тест: Функция login возвращает данные пользователя с ролью"""
    user_data = login("alice", "password123")
    assert user_data is not None
    assert 'role' in user_data
    assert user_data['role'] == 'admin'

def test_unauthorized_deletion_attempt(capsys):
    """Тест: Попытка удаления без прав администратора"""
    # После исправления этот тест должен проходить
    delete_user("alice", caller_role="user")
    captured = capsys.readouterr()
    assert "Ошибка доступа" in captured.out or "администраторы" in captured.out
    assert "alice" in USERS