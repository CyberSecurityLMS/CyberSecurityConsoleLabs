import pytest
import sys
import os
from C06_command_injection_lab import check_host
from unittest.mock import patch, MagicMock

def test_safe_host_check(capsys):
    """Тест: безопасная проверка хоста"""
    with patch('os.system') as mock_system:
        mock_system.return_value = 0
        result = check_host("google.com")
        captured = capsys.readouterr()
        
        assert result is True
        assert "google.com" in captured.out
        assert "Ошибка" not in captured.out

def test_command_injection_attempt(capsys):
    """Тест: попытка инъекции команды"""
    # Мокаем os.system для проверки переданной команды
    with patch('os.system') as mock_system:
        mock_system.return_value = 0
        malicious_input = "google.com ; echo HACKED"
        result = check_host(malicious_input)
        captured = capsys.readouterr()
        
        # После исправления должна быть ошибка или безопасная обработка
        assert "HACKED" not in captured.out, "Обнаружено выполнение инъекции!"
        assert ";" in captured.out, "Символы инъекции должны быть экранированы"

def test_shell_false_used():
    """Тест: используется безопасный метод выполнения команд"""
    with open('vulnerable_app.py', 'r') as f:
        content = f.read()
        assert 'subprocess.run(' in content, \
            "Используйте subprocess.run вместо os.system"
        assert 'shell=True' not in content, \
            "Не используйте shell=True с пользовательским вводом"

def test_command_as_list():
    """Тест: команда передается как список аргументов"""
    with open('vulnerable_app.py', 'r') as f:
        content = f.read()
        assert '["ping", ' in content or "['ping', " in content, \
            "Команда должна передаваться как список аргументов"

def test_error_handling(capsys):
    """Тест: обработка ошибок выполнения команды"""
    with patch('os.system') as mock_system:
        mock_system.side_effect = Exception("Test error")
        result = check_host("invalid.host")
        captured = capsys.readouterr()
        
        assert result is False
        assert "Ошибка" in captured.out