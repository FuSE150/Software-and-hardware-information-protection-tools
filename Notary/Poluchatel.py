import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding
import hashlib


class RecipientApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Получатель")

        self.file_path = 'recipient_file.txt'
        self.signature_path = 'recipient_signature.sig'
        self.public_key_path = 'recipient_received_public_key.pem'  # Путь к открытому ключу

        # Кнопка для проверки подписи
        self.verify_signature_button = tk.Button(root, text="Проверить подпись", command=self.verify_signature)
        self.verify_signature_button.pack(pady=5)

    def load_public_key(self):
        with open(self.public_key_path, 'rb') as f:
            public_key = serialization.load_pem_public_key(f.read())
        return public_key

    def load_signature(self):
        with open(self.signature_path, 'rb') as f:
            signature = f.read()
        return signature

    def hash_file_sha2(self, file_path: str, sha_type: str = 'sha256'):
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

    def verify_signature(self):
        try:
            # Хешируем файл
            hashed_file = self.hash_file_sha2(self.file_path)

            # Загружаем открытый ключ и подпись
            public_key = self.load_public_key()
            signature = self.load_signature()

            # Проверяем подпись
            public_key.verify(
                signature,
                hashed_file,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            messagebox.showinfo("Успех", "Подпись действительна.")
        except Exception as e:
            messagebox.showerror("Ошибка проверки подписи", "Подпись недействительна.")


if __name__ == "__main__":
    root = tk.Tk()
    app = RecipientApp(root)
    root.geometry("300x200")
    root.mainloop()
