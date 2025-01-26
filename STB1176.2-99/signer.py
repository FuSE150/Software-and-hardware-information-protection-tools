from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import pickle

def sign_message(message, private_key):
    # Создание хэша сообщения
    h = SHA256.new(message.encode())
    # Подпись хэша
    signature = pkcs1_15.new(private_key).sign(h)
    return signature

def main():
    # Чтение сообщения из слепого файла
    with open("blinded_message.txt", "r", encoding='utf-8') as f:
        blinded_message, mask = f.read().strip().split("\n")
        blinded_message = int(blinded_message)
        mask = bytes.fromhex(mask)

    # Загрузка закрытого ключа
    with open("private_key.pem", "rb") as key_file:
        private_key = RSA.import_key(key_file.read())

    # Подписание сообщения
    signature = sign_message(str(blinded_message), private_key)

    # Сохранение подписи в текстовый файл
    with open("signed_blinded_message.txt", "wb") as f:
        f.write(signature)

    print("Подпись сохранена в 'signed_blinded_message.txt'.")

if __name__ == "__main__":
    main()
