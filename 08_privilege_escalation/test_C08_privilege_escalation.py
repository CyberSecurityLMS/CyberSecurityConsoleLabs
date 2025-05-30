import pytest
import sys
import json
from C08_privilege_escalation_lab import update_profile_vulnerable, USERS

@pytest.fixture
def setup_users():
    """Фикстура для создания тестовых пользователей"""
    users = {
        "user1": {"password": "pass1", "role": "user", "email": "user1@test.com"},
        "admin1": {"password": "adminpass", "role": "admin", "email": "admin@test.com"}
    }
    return users

def test_normal_profile_update(setup_users, capsys):
    """Тест: обычное обновление email"""
    original_users = setup_users.copy()
    result = update_profile_vulnerable("user1", '{"email": "new@test.com"}')
    captured = capsys.readouterr()
    
    assert result is True
    assert "new@test.com" in captured.out
    assert "role" not in captured.out

def test_privilege_escalation_attempt(setup_users, capsys):
    """Тест: попытка повышения привилегий"""
    original_role = setup_users["user1"]["role"]
    result = update_profile_vulnerable("user1", '{"role": "admin"}')
    captured = capsys.readouterr()
    
    # После исправления должно быть сообщение об ошибке
    assert "role" in captured.out.lower()
    assert "admin" not in captured.out or "запрещено" in captured.out

def test_function_checks_fields():
    """Тест: функция проверяет изменяемые поля"""
    import inspect
    import C08_privilege_escalation_lab
    
    source = inspect.getsource(C08_privilege_escalation_lab.update_profile_vulnerable)
    assert "role" in source, "Функция должна проверять поле 'role'"
    assert "if key ==" in source or "forbidden" in source, \
        "Должна быть проверка на запрещенные поля"

def test_admin_can_change_own_email(setup_users, capsys):
    """Тест: админ может менять свой email"""
    result = update_profile_vulnerable("admin1", '{"email": "newadmin@test.com"}')
    captured = capsys.readouterr()
    
    assert result is True
    assert "newadmin@test.com" in captured.out
    assert "role" not in captured.out

def test_no_arbitrary_field_updates(setup_users, capsys):
    """Тест: нельзя добавлять произвольные поля"""
    result = update_profile_vulnerable("user1", '{"is_superuser": true}')
    captured = capsys.readouterr()
    
    assert "is_superuser" not in captured.out
    assert "не разрешено" in captured.out or "игнорировано" in captured.out