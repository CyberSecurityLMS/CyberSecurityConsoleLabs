import pytest
import sys
from C09_authentification_bypass_lab import login_vulnerable, access_restricted_data

def test_successful_auth(capsys):
    """Тест: успешная аутентификация"""
    result = login_vulnerable("admin", "secure123")
    captured = capsys.readouterr()
    
    assert result is not None
    assert "Аутентификация успешна" in captured.out
    assert "Конфиденциальные" in str(result.get('data'))

def test_failed_auth_wrong_pass(capsys):
    """Тест: неверный пароль"""
    result = login_vulnerable("admin", "wrongpass")
    captured = capsys.readouterr()
    
    assert result is None
    assert "Неверный пароль" in captured.out

def test_auth_bypass_attempt(capsys):
    """Тест: попытка обхода аутентификации"""
    # Попытка входа несуществующим пользователем
    result = login_vulnerable("hacker", "anypass")
    captured = capsys.readouterr()
    
    # После исправления должно возвращаться None
    assert result == {}, "Уязвимость: возвращается пустой словарь вместо None"
    
    # Проверяем доступ к данным
    access_restricted_data(result)
    captured = capsys.readouterr()
    assert "Доступ разрешен" in captured.out, "Уязвимость: доступ разрешен без аутентификации"

def test_access_control_checks():
    """Тест: функция доступа должна выполнять строгие проверки"""
    import inspect
    import C09_authentification_bypass_lab
    
    source = inspect.getsource(C09_authentification_bypass_lab.access_restricted_data)
    assert "isinstance" in source or "'data' in" in source, \
        "Добавьте проверку типа и наличия данных"
    assert "None" in source or "False" in source, \
        "Добавьте явную проверку на неудачную аутентификацию"

def test_login_returns_none():
    """Тест: функция входа должна возвращать None при ошибках"""
    import inspect
    import C09_authentification_bypass_lab
    
    source = inspect.getsource(C09_authentification_bypass_lab.login_vulnerable)
    assert "return None" in source or "return False" in source, \
        "Функция должна явно возвращать None/False при ошибках"