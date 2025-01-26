import hashlib
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend


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


# Генерация пары ключей (закрытый и открытый ключи)
def generate_rsa_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


# Экспорт открытого ключа в файл
def export_public_key(public_key):
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open('public_key.pem', 'wb') as f:
        f.write(public_key_pem)


# Подписание хешированного файла
def sign_file(private_key, file_hash):
    signature = private_key.sign(
        file_hash,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


# Сохранение цифровой подписи в файл
def save_signature(signature):
    with open('signature.sig', 'wb') as f:
        f.write(signature)


# Пример использования
if __name__ == "__main__":
    file_path = input("Введите путь к файлу для хеширования: ")
    sha_type = input("Введите тип SHA (sha256, sha384 или sha512): ")

    # Генерируем ключи
    private_key, public_key = generate_rsa_keys()

    # Хешируем файл
    hashed_file = hash_file_sha2(file_path, sha_type)
    print(f"Хешированное значение файла (в байтах): {hashed_file.hex()}")

    # Подписываем файл
    signature = sign_file(private_key, hashed_file)
    save_signature(signature)
    print(f"Цифровая подпись сохранена в 'signature.sig'")

    # Экспортируем публичный ключ для передачи другому человеку
    export_public_key(public_key)
    print("Открытый ключ экспортирован и сохранен в 'public_key.pem'")
