import pytest
import pyyaml
import os
import io
from C01_vulnerable_dependencies_lab import load_config

@pytest.fixture
def malicious_yaml_file(tmp_path):
    """Фикстура для создания вредоносного YAML-файла"""
    malicious_yaml = """!!python/object/apply:builtins.print
args: ["Vulnerability Exploited! Code execution detected"]
"""
    file_path = tmp_path / "malicious.yaml"
    file_path.write_text(malicious_yaml)
    return str(file_path)

@pytest.fixture
def safe_yaml_file(tmp_path):
    """Фикстура для создания безопасного YAML-файла"""
    safe_yaml = """
database:
  host: localhost
  port: 5432
  username: admin
  password: secret
"""
    file_path = tmp_path / "safe.yaml"
    file_path.write_text(safe_yaml)
    return str(file_path)

def test_safe_yaml_loading(safe_yaml_file):
    """Тест проверяет, что обычные YAML-файлы загружаются корректно"""
    result = load_config(safe_yaml_file)
    assert result is not None
    assert 'database' in result
    assert result['database']['host'] == 'localhost'

def test_malicious_yaml_loading(malicious_yaml_file, capsys):
    """
    Тест проверяет, что вредоносный YAML не выполняет код
    (должен либо корректно загружать данные, либо вызывать ошибку)
    """
    # Если студент исправил код, этот тест не должен показывать вывод в консоль
    result = load_config(malicious_yaml_file)
    
    captured = capsys.readouterr()
    assert "Vulnerability Exploited!" not in captured.out, \
        "Обнаружено выполнение кода из YAML! Используйте yaml.safe_load() вместо yaml.load()"
    
    # Проверяем, что функция либо возвращает None (ошибка), либо корректные данные
    if result is not None:
        assert isinstance(result, (dict, list, str, int, float)), \
            "Функция должна возвращать только базовые типы данных при использовании safe_load"

def test_file_not_found():
    """Тест проверяет обработку случая, когда файл не существует"""
    result = load_config("nonexistent_file.yaml")
    assert result is None

def test_safe_load_used():
    """Тест проверяет, что в коде используется safe_load вместо load"""
    with open('vulnerable_app.py', 'r') as f:
        content = f.read()
        assert 'yaml.safe_load(' in content, \
            "Вы должны использовать yaml.safe_load() вместо yaml.load()"
        assert 'yaml.load(' not in content, \
            "Вы должны полностью заменить yaml.load() на yaml.safe_load()"