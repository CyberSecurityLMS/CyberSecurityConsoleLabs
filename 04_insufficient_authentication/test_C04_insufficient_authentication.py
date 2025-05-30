import pytest
import sys
import os
from C04_insufficient_authentification_lab import login, get_user_profile, USERS

# Фикстура для имитации сессии
@pytest.fixture
def mock_session(monkeypatch):
    # Мокаем глобальную переменную для хранения текущего пользователя
    current_user = None
    
    def mock_login(user_id, password):
        nonlocal current_user
        user = USERS.get(user_id)
        if user and user["password"] == password:
            current_user = user_id
            return user
        return None
    
    def mock_get_user_profile(user_id):
        nonlocal current_user
        if not current_user:
            print("Ошибка: Требуется вход в систему")
            return None
        if current_user != user_id:
            print("Ошибка: Можно просматривать только свой профиль")
            return None
        user = USERS.get(user_id)
        if user:
            print(f"\n--- Профиль пользователя ID {user_id} ---")
            print(f"  Имя пользователя: {user['username']}")
            return user
        return None
    
    monkeypatch.setattr('vulnerable_app.login', mock_login)
    monkeypatch.setattr('vulnerable_app.get_user_profile', mock_get_user_profile)
    yield

def test_successful_login(mock_session, capsys):
    """Тест: успешный вход в систему"""
    result = login("1", "admin_pass")
    captured = capsys.readouterr()
    assert result is not None
    assert "успешно вошел" in captured.out

def test_failed_login(mock_session, capsys):
    """Тест: неудачный вход в систему"""
    result = login("1", "wrong_pass")
    captured = capsys.readouterr()
    assert result is None
    assert "Неверный" in captured.out

def test_profile_access_without_login(mock_session, capsys):
    """Тест: попытка доступа к профилю без аутентификации"""
    get_user_profile("1")
    captured = capsys.readouterr()
    assert "Требуется вход" in captured.out or "Ошибка доступа" in captured.out

def test_profile_access_after_login(mock_session, capsys):
    """Тест: доступ к своему профилю после аутентификации"""
    login("1", "admin_pass")
    get_user_profile("1")
    captured = capsys.readouterr()
    assert "Профиль пользователя" in captured.out
    assert "admin" in captured.out

def test_profile_access_other_user(mock_session, capsys):
    """Тест: попытка доступа к чужому профилю"""
    login("1", "admin_pass")
    get_user_profile("2")
    captured = capsys.readouterr()
    assert "только свой профиль" in captured.out or "Ошибка доступа" in captured.out

def test_function_checks_authentication():
    """Тест: функция проверяет аутентификацию перед доступом"""
    import inspect
    import C04_insufficient_authentification_lab
    
    # Проверяем, что функция использует проверку текущего пользователя
    source = inspect.getsource(C04_insufficient_authentification_lab.get_user_profile)
    assert "current_user" in source or "session" in source, \
        "Функция должна проверять аутентификацию пользователя"