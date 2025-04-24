# 07_weak_cryptography/vulnerable_app.py
import sys
import base64

# ОЧЕНЬ СЛАБЫЙ "шифр" - Шифр Цезаря с фиксированным сдвигом
FIXED_SHIFT = 3

def caesar_cipher_encrypt(plaintext, shift):
    """Шифрует текст с помощью шифра Цезаря."""
    encrypted_text = ""
    for char in plaintext:
        if 'a' <= char <= 'z':
            shifted = ord('a') + (ord(char) - ord('a') + shift) % 26
            encrypted_text += chr(shifted)
        elif 'A' <= char <= 'Z':
            shifted = ord('A') + (ord(char) - ord('A') + shift) % 26
            encrypted_text += chr(shifted)
        else:
            encrypted_text += char # Не шифруем не-буквы
    return encrypted_text

def caesar_cipher_decrypt(ciphertext, shift):
    """Дешифрует текст шифра Цезаря."""
    # Дешифровка - это шифрование с отрицательным сдвигом
    return caesar_cipher_encrypt(ciphertext, -shift)

# Функция для "безопасного" сохранения секрета
def save_secret_vulnerable(secret_data):
    print(f"Исходные данные: {secret_data}")
    # УЯЗВИМОСТЬ: Используется очень слабый шифр с фиксированным ключом
    encrypted_data = caesar_cipher_encrypt(secret_data, FIXED_SHIFT)
    # Используем Base64 просто для того, чтобы это не выглядело как читаемый текст
    encoded_data = base64.b64encode(encrypted_data.encode()).decode()
    print(f"\"Зашифровано\" (Шифр Цезаря, shift={FIXED_SHIFT}, затем Base64): {encoded_data}")
    # В реальном приложении это бы сохранялось в файл или БД
    return encoded_data

# Функция для загрузки секрета
def load_secret_vulnerable(encoded_data):
    try:
        decoded_data = base64.b64decode(encoded_data).decode()
        decrypted_data = caesar_cipher_decrypt(decoded_data, FIXED_SHIFT)
        print(f"\"Расшифровано\": {decrypted_data}")
        return decrypted_data
    except Exception as e:
        print(f"Ошибка расшифровки: {e}")
        return None

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Использование: python vulnerable_app.py \"<секретные_данные>\"")
        print("Пример: python vulnerable_app.py \"My Secret Password!\"")
        sys.exit(1)

    secret = sys.argv[1]
    print("--- Уязвимое сохранение ---")
    saved_blob = save_secret_vulnerable(secret)

    print("\n--- Уязвимая загрузка ---")
    loaded_secret = load_secret_vulnerable(saved_blob)

    if loaded_secret == secret:
        print("\nДанные успешно сохранены и восстановлены (но небезопасно!)")
    else:
        print("\nОшибка: Восстановленные данные не совпадают с исходными.") 