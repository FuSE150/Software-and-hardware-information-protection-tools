import hashlib

def hash_file_sha2(sentence: str, sha_type: str = 'sha256') -> str:
# Выбираем алгоритм SHA в зависимости от аргумента
    if sha_type == 'sha256':
        hash_object = hashlib.sha256()
    elif sha_type == 'sha384':
        hash_object = hashlib.sha384()
    elif sha_type == 'sha512':
        hash_object = hashlib.sha512()
    else:
        raise ValueError("Неподдерживаемый тип SHA. Используйте 'sha256', 'sha384' или 'sha512'.")

# Открываем файл в бинарном режиме и читаем его блоками
    with open(file_path, 'rb') as file:
        while chunk := file.read(8192): # Читаем по 8192 байта
            hash_object.update(chunk)

# Возвращаем хешированное значение в шестнадцатеричном формате
    return hash_object.hexdigest()

# Пример использования
file_path = input("Введите путь к файлу для хеширования: ")
sha_type = input("Введите тип SHA (sha256, sha384 или sha512): ")
hashed_file = hash_file_sha2(file_path, sha_type)
print(f"Хешированное значение файла: {hashed_file}")
