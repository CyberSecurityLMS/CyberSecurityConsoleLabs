# 07_weak_cryptography/fixed_app.py
import sys
import os
import base64
from typing import Optional

# Определим заглушки заранее
class AESGCM: pass
class PBKDF2HMAC: pass
class hashes:
    class SHA256:
        pass

# Попытка импорта и переопределения заглушек реальными классами
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM as RealAESGCM
    from cryptography.hazmat.primitives import hashes as RealHashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC as RealPBKDF2HMAC
    # Переопределяем заглушки, если импорт успешен
    AESGCM = RealAESGCM
    hashes = RealHashes
    PBKDF2HMAC = RealPBKDF2HMAC
    CRYPTOGRAPHY_AVAILABLE = True
except ImportError:
    CRYPTOGRAPHY_AVAILABLE = False

# --- Безопасные криптографические операции ---

# Важно: В реальном приложении соль должна быть уникальной для каждого пароля/ключа
# и храниться вместе с зашифрованными данными. Здесь для простоты она фиксирована.
FIXED_SALT = b'\x00\x11\x22\x33\x44\x55\x66\x77\x88\x99\xaa\xbb\xcc\xdd\xee\xff'

def derive_key(password: bytes, salt: bytes) -> bytes:
    """Безопасно генерирует ключ из пароля с использованием PBKDF2."""
    if not CRYPTOGRAPHY_AVAILABLE:
        raise RuntimeError("Библиотека cryptography не установлена")
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32, # Длина ключа AES-256
        salt=salt,
        iterations=100000, # Рекомендуемое количество итераций (может быть больше)
    )
    key = kdf.derive(password)
    return key

def encrypt_aes_gcm(data: bytes, key: bytes) -> bytes:
    """Шифрует данные с использованием AES-GCM (Аутентифицированное шифрование)."""
    if not CRYPTOGRAPHY_AVAILABLE:
        raise RuntimeError("Библиотека cryptography не установлена")
    # Генерируем случайный nonce (Initialization Vector) для каждого шифрования
    nonce = os.urandom(12) # Рекомендуемый размер для GCM - 12 байт
    aesgcm = AESGCM(key)
    encrypted_data = aesgcm.encrypt(nonce, data, None) # None - нет дополнительных аутентифицированных данных (AAD)
    # Возвращаем nonce вместе с зашифрованными данными, он нужен для расшифровки
    return nonce + encrypted_data

def decrypt_aes_gcm(encrypted_blob: bytes, key: bytes) -> Optional[bytes]:
    """Расшифровывает данные, зашифрованные AES-GCM."""
    if not CRYPTOGRAPHY_AVAILABLE:
        raise RuntimeError("Библиотека cryptography не установлена")
    try:
        # Извлекаем nonce (первые 12 байт)
        nonce = encrypted_blob[:12]
        encrypted_data = encrypted_blob[12:]
        aesgcm = AESGCM(key)
        decrypted_data = aesgcm.decrypt(nonce, encrypted_data, None)
        return decrypted_data
    except Exception as e: # Ловим InvalidTag и другие возможные ошибки
        print(f"Ошибка расшифровки AES-GCM: {e} (Возможно, неверный пароль или данные повреждены)")
        return None

# Функция для БЕЗОПАСНОГО сохранения секрета
def save_secret_secure(secret_data: str, password: str):
    print(f"Исходные данные: {secret_data}")
    password_bytes = password.encode('utf-8')
    data_bytes = secret_data.encode('utf-8')

    # 1. Генерируем ключ из пароля
    key = derive_key(password_bytes, FIXED_SALT)
    # print(f"Производный ключ (hex): {key.hex()}") # Не выводить в реальном коде

    # 2. Шифруем данные с использованием AES-GCM
    encrypted_blob = encrypt_aes_gcm(data_bytes, key)

    # 3. Кодируем в Base64 для удобства хранения/передачи
    encoded_blob = base64.b64encode(encrypted_blob).decode('utf-8')
    print(f"Зашифровано (AES-256-GCM, ключ из пароля, Base64): {encoded_blob}")
    # В реальном приложении соль (FIXED_SALT) должна храниться вместе с encoded_blob
    return encoded_blob # и соль

# Функция для БЕЗОПАСНОЙ загрузки секрета
def load_secret_secure(encoded_blob: str, password: str) -> Optional[str]:
    password_bytes = password.encode('utf-8')
    try:
        encrypted_blob = base64.b64decode(encoded_blob)

        # 1. Генерируем ТОТ ЖЕ ключ из пароля и СОЛИ
        # (в реальном приложении соль загружалась бы вместе с blob)
        key = derive_key(password_bytes, FIXED_SALT)
        # print(f"Производный ключ для расшифровки (hex): {key.hex()}")

        # 2. Расшифровываем данные
        decrypted_bytes = decrypt_aes_gcm(encrypted_blob, key)

        if decrypted_bytes:
            decrypted_data = decrypted_bytes.decode('utf-8')
            print(f"Расшифровано: {decrypted_data}")
            return decrypted_data
        else:
            # Ошибка уже выведена в decrypt_aes_gcm
            return None
    except Exception as e:
        print(f"Ошибка загрузки/расшифровки: {e}")
        return None


if __name__ == "__main__":
    # Проверка установки библиотеки перед использованием
    if not CRYPTOGRAPHY_AVAILABLE:
        print("-" * 30)
        print("Ошибка: Библиотека 'cryptography' не установлена.")
        print("Пожалуйста, установите ее:")
        print("1. Создайте виртуальное окружение (если еще нет): python -m venv venv")
        print("2. Активируйте его: source venv/bin/activate (Linux/Mac) или .\\venv\\Scripts\\activate (Win)")
        print("3. Установите зависимости: pip install -r requirements.txt")
        print("-" * 30)
        sys.exit(1)

    if len(sys.argv) != 3:
        print("Использование: python fixed_app.py \"<секретные_данные>\" \"<пароль_для_ключа>\"")
        print("Пример: python fixed_app.py \"My Secret Password!\" \"super_secret_phrase\"")
        sys.exit(1)

    secret = sys.argv[1]
    password = sys.argv[2]

    print("--- Безопасное сохранение ---")
    saved_blob = save_secret_secure(secret, password)

    print("\n--- Безопасная загрузка ---")
    # Имитация ситуации: для загрузки нужен тот же пароль
    loaded_secret = load_secret_secure(saved_blob, password)

    if loaded_secret == secret:
        print("\nДанные успешно сохранены и восстановлены безопасно.")
    else:
        print("\nОшибка: Восстановленные данные не совпадают или произошла ошибка расшифровки.")

    print("\n--- Попытка загрузки с неверным паролем ---")
    load_secret_secure(saved_blob, "wrong_password") 