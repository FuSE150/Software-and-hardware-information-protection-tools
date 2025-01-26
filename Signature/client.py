from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import hashlib


# Функция для хеширования файла
def hash_file_sha2(file_path: str, sha_type: str = 'sha256'):
    if sha_type == 'sha256':
        hash_object = hashlib.sha256()
    elif sha_type == 'sha384':
        hash_object = hashlib.sha384()
    elif sha_type == 'sha512':
        hash_object = hashlib.sha512()
    else:
        raise ValueError("Неподдерживаемый тип SHA. Используйте 'sha256', 'sha384' или 'sha512'.")

    with open(file_path, 'rb') as file:
        while chunk := file.read(8192):
            hash_object.update(chunk)

    return hash_object.digest()  # Возвращаем хеш как байты


# Загрузка открытого ключа из файла
def load_public_key():
    with open('public_key.pem', 'rb') as f:
        public_key = serialization.load_pem_public_key(f.read())
    return public_key


# Загрузка цифровой подписи из файла
def load_signature():
    with open('signature.sig', 'rb') as f:
        signature = f.read()
    return signature


# Проверка подписи
def verify_signature(public_key, file_hash, signature):
    try:
        public_key.verify(
            signature,
            file_hash,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        print(f"Ошибка проверки подписи: {e}")
        return False


# Пример использования
if __name__ == "__main__":
    file_path = input("Введите путь к файлу для хеширования: ")
    sha_type = input("Введите тип SHA (sha256, sha384 или sha512): ")

    # Хешируем файл
    hashed_file = hash_file_sha2(file_path, sha_type)

    # Загрузка открытого ключа и подписи
    public_key = load_public_key()
    signature = load_signature()

    # Проверка подписи
    is_valid = verify_signature(public_key, hashed_file, signature)
    print(f"Подпись действительна: {is_valid}")