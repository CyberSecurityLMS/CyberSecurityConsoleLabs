# Уязвимое приложение - лабораторная работа по слабой криптографии
# Студенту нужно исправить этот файл, заменив слабый шифр Цезаря на надежное шифрование

import sys
import base64

# Очень слабый "шифр" - Шифр Цезаря с фиксированным сдвигом
FIXED_SHIFT = 3

def caesar_cipher_encrypt(plaintext, shift):
    """
    Уязвимая функция шифрования
    
    ЗАДАНИЕ ДЛЯ СТУДЕНТА:
    Эта функция использует шифр Цезаря - очень слабый алгоритм шифрования.
    Тебе нужно:
    1. Заменить его на современный алгоритм (AES-GCM)
    2. Использовать надежный ключ (256 бит)
    3. Добавить аутентификацию данных
    4. Использовать соль для генерации ключа
    
    После исправления тесты из test_cryptography.py должны пройти успешно.
    """
    encrypted_text = ""
    for char in plaintext:
        if 'a' <= char <= 'z':
            shifted = ord('a') + (ord(char) - ord('a') + shift) % 26
            encrypted_text += chr(shifted)
        elif 'A' <= char <= 'Z':
            shifted = ord('A') + (ord(char) - ord('A') + shift) % 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char
    return encrypted_text

def save_secret_vulnerable(secret_data):
    print(f"Исходные данные: {secret_data}")
    # TODO: ЗАМЕНИТЕ ЭТО НА БЕЗОПАСНОЕ ШИФРОВАНИЕ
    encrypted_data = caesar_cipher_encrypt(secret_data, FIXED_SHIFT)
    encoded_data = base64.b64encode(encrypted_data.encode()).decode()
    print(f"\"Зашифровано\": {encoded_data}")
    return encoded_data

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python vulnerable_app.py \"<секретные_данные>\"")
        print("Пример: python vulnerable_app.py \"MySecretPassword\"")
        sys.exit(1)

    secret = sys.argv[1]
    print("--- Уязвимое сохранение ---")
    saved_blob = save_secret_vulnerable(secret)