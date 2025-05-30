import pytest
import os
import sys
from C03_file_handling_lab import read_user_file, BASE_DIR

@pytest.fixture
def setup_files(tmp_path):
    """Фикстура для создания тестовых файлов"""
    # Создаем базовую директорию
    base_dir = tmp_path / BASE_DIR
    base_dir.mkdir()
    
    # Создаем разрешенный файл
    allowed_file = base_dir / "allowed.txt"
    allowed_file.write_text("This is allowed content")
    
    # Создаем файл вне базовой директории
    outside_file = tmp_path / "outside.txt"
    outside_file.write_text("This is outside content")
    
    return {
        "base_dir": str(base_dir),
        "allowed_file": "allowed.txt",
        "outside_file": f"../../{outside_file.name}",
    }

def test_allowed_file_access(setup_files, capsys):
    """Тест: доступ к разрешенному файлу"""
    # Монkey-патчим BASE_DIR для теста
    original_base_dir = BASE_DIR
    try:
        import C03_file_handling_lab
        C03_file_handling_lab.BASE_DIR = setup_files["base_dir"]
        
        content = read_user_file(setup_files["allowed_file"])
        captured = capsys.readouterr()
        
        assert "This is allowed content" in content
        assert "Ошибка доступа" not in captured.out
    finally:
        C03_file_handling_lab.BASE_DIR = original_base_dir

def test_path_traversal_attempt(setup_files, capsys):
    """Тест: попытка Path Traversal"""
    original_base_dir = BASE_DIR
    try:
        import C03_file_handling_lab
        C03_file_handling_lab.BASE_DIR = setup_files["base_dir"]
        
        content = read_user_file(setup_files["outside_file"])
        captured = capsys.readouterr()
        
        # После исправления должно быть сообщение об ошибке
        assert content is None
        assert "Ошибка доступа" in captured.out or "вне базовой директории" in captured.out
    finally:
        C03_file_handling_lab.BASE_DIR = original_base_dir

def test_function_checks_path():
    """Тест: функция проверяет путь перед чтением"""
    import inspect
    import C03_file_handling_lab
    
    # Проверяем, что функция использует os.path.abspath
    source = inspect.getsource(C03_file_handling_lab.read_user_file)
    assert "os.path.abspath" in source, "Функция должна использовать os.path.abspath"
    
    # Проверяем, что есть проверка базового пути
    assert "startswith" in source or "commonpath" in source, \
        "Функция должна проверять, что путь начинается с BASE_DIR"

def test_non_existent_file(setup_files, capsys):
    """Тест: обработка несуществующего файла"""
    original_base_dir = BASE_DIR
    try:
        import C03_file_handling_lab
        C03_file_handling_lab.BASE_DIR = setup_files["base_dir"]
        
        content = read_user_file("non_existent.txt")
        captured = capsys.readouterr()
        
        assert content is None
        assert "не найден" in captured.out
    finally:
        C03_file_handling_lab.BASE_DIR = original_base_dir