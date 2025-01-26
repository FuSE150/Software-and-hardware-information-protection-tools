from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import pickle

def unblind_signature(signed_blinded_message, mask, public_key):
    # Удаление маски с подписи
    return (signed_blinded_message * pow(mask, -1, public_key.n)) % public_key.n

def verify_signature(unblinded_signature, public_key, original_hash):
    # Проверка подписи
    verification = pow(unblinded_signature, public_key.e, public_key.n)
    return verification == original_hash

def main():
    # Загрузка открытого ключа подписывающего
    with open("public_key.pem", "rb") as key_file:
        public_key = RSA.import_key(key_file.read())

    # Загрузка маски и слепого сообщения
    with open("blinded_message.bin", "rb") as f:
        blinded_message, mask = pickle.load(f)

    # Загрузка подписанного слепого сообщения
    with open("signed_blinded_message.bin", "rb") as f:
        signed_blinded_message = pickle.load(f)

    # Снятие маски с подписанного сообщения
    unblinded_signature = unblind_signature(signed_blinded_message, mask, public_key)

    # Оригинальное сообщение для подписи
    original_message = "Ваше сообщение для подписи"
    # Получение оригинального хэша сообщения
    original_hash = int.from_bytes(SHA256.new(original_message.encode()).digest(), byteorder='big')

    # Проверка подписи
    if verify_signature(unblinded_signature, public_key, original_hash):
        print("Подпись подтверждена.")
        print("Оригинальное сообщение:", original_message)  # Отображение оригинального сообщения
    else:
        print("Подпись недействительна.")

if __name__ == "__main__":
    main()
