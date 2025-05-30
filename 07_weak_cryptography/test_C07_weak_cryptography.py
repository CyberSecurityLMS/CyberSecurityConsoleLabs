import pytest
import sys
import os
import base64
from C07_weak_cryptography_lab import save_secret_vulnerable

def test_weak_encryption_breakable(capsys):
    """Тест: слабое шифрование легко взломать"""
    secret = "TopSecret123"
    encrypted = save_secret_vulnerable(secret)
    captured = capsys.readouterr()
    
    # Проверяем, что шифрование работает
    assert encrypted is not None
    
    # Пытаемся взломать шифр Цезаря
    decoded = base64.b64decode(encrypted).decode()
    for shift in range(26):  # Все возможные сдвиги
        decrypted = ""
        for char in decoded:
            if 'a' <= char <= 'z':
                decrypted += chr(ord('a') + (ord(char) - ord('a') - shift) % 26)
            elif 'A' <= char <= 'Z':
                decrypted += chr(ord('A') + (ord(char) - ord('A') - shift) % 26)
            else:
                decrypted += char
        if decrypted == secret:
            break
    
    assert decrypted == secret, "Шифр Цезаря взломан простым перебором"

def test_fixed_encryption_required():
    """Тест: должен использоваться надежный алгоритм"""
    with open('vulnerable_app.py', 'r') as f:
        content = f.read()
        assert 'AESGCM' in content, "Используйте AES-GCM для шифрования"
        assert 'PBKDF2HMAC' in content, "Используйте PBKDF2 для генерации ключа"

def test_no_hardcoded_keys():
    """Тест: не должно быть фиксированных ключей"""
    with open('vulnerable_app.py', 'r') as f:
        content = f.read()
        assert 'FIXED_SHIFT' not in content, "Не используйте фиксированные ключи"

def test_authentication_required():
    """Тест: шифрование должно обеспечивать аутентификацию"""
    with open('vulnerable_app.py', 'r') as f:
        content = f.read()
        assert 'authenticated' in content or 'GCM' in content, \
            "Используйте аутентифицированное шифрование (AEAD)"

def test_salt_required():
    """Тест: должна использоваться соль для генерации ключа"""
    with open('vulnerable_app.py', 'r') as f:
        content = f.read()
        assert 'salt' in content, "Используйте соль при генерации ключа"