import pytest
import sys
import os
from C05_code_injection_lab import calculate

def test_safe_math_expression(capsys):
    """Тест: вычисление безопасного математического выражения"""
    result = calculate("2 + 2 * 3")
    captured = capsys.readouterr()
    assert result == 8
    assert "Ошибка" not in captured.out

def test_code_injection_attempt(capsys):
    """Тест: попытка внедрения кода"""
    # Попытка выполнить команду системы
    malicious_code = "__import__('os').system('echo HACKED')"
    result = calculate(malicious_code)
    captured = capsys.readouterr()
    
    # После исправления должно быть сообщение об ошибке
    assert result is None
    assert "Ошибка" in captured.out
    assert "HACKED" not in captured.out, "Обнаружено выполнение кода!"

def test_function_calls_not_allowed(capsys):
    """Тест: вызовы функций должны быть запрещены"""
    result = calculate("print('test')")
    captured = capsys.readouterr()
    assert result is None
    assert "Ошибка" in captured.out
    assert "test" not in captured.out

def test_variable_access_not_allowed(capsys):
    """Тест: доступ к переменным должен быть запрещен"""
    result = calculate("__import__")
    captured = capsys.readouterr()
    assert result is None
    assert "Ошибка" in captured.out

def test_complex_math_allowed(capsys):
    """Тест: сложные математические выражения должны работать"""
    expressions = [
        ("(2 + 3) * 4", 20),
        ("2 ** 8", 256),
        ("1.5 + 2.5", 4.0),
        ("-5 * 2", -10)
    ]
    
    for expr, expected in expressions:
        result = calculate(expr)
        captured = capsys.readouterr()
        assert result == expected
        assert "Ошибка" not in captured.out

def test_eval_not_used():
    """Тест: функция не должна использовать eval()"""
    with open('vulnerable_app.py', 'r') as f:
        content = f.read()
        assert 'eval(' not in content, \
            "Вы должны полностью заменить eval() на безопасную альтернативу"