import tkinter as tk
from tkinter import messagebox
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.backends import default_backend
import os
import shutil


class NotaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Нотариус")

        self.private_key = None
        self.public_key = None

        # Кнопка для генерации ключей
        self.generate_keys_button = tk.Button(root, text="Генерировать ключи", command=self.generate_keys)
        self.generate_keys_button.pack(pady=5)

        # Кнопка для подписания файла
        self.sign_file_button = tk.Button(root, text="Подписать файл", command=self.sign_file, state=tk.DISABLED)
        self.sign_file_button.pack(pady=5)

        # Кнопка для отправки открытого ключа Получателю
        self.send_public_key_button = tk.Button(root, text="Отправить открытый ключ Получателю",
                                                command=self.send_public_key, state=tk.DISABLED)
        self.send_public_key_button.pack(pady=5)

        # Состояние подписания файла
        self.file_signed = False

    def generate_keys(self):
        # Генерация пары ключей
        self.private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        self.public_key = self.private_key.public_key()

        # Сохранение открытого ключа в файл
        with open('public_key.pem', 'wb') as f:
            f.write(self.public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))

        messagebox.showinfo("Успех", "Открытый и закрытый ключи успешно сгенерированы и сохранены.")

        # Активируем кнопку для подписания файла
        self.sign_file_button.config(state=tk.NORMAL)

    def sign_file(self):
        file_path = 'notary_received_file.txt'
        if not os.path.exists(file_path):
            messagebox.showwarning("Ошибка", "Нет файла для подписания.")
            return

        with open(file_path, 'rb') as file:
            file_data = file.read()
            file_hash = hashes.Hash(hashes.SHA256(), backend=default_backend())
            file_hash.update(file_data)
            digest = file_hash.finalize()

        # Подписываем хеш файла с помощью закрытого ключа
        signature = self.private_key.sign(
            digest,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Сохранение подписи в файл
        with open('signature.sig', 'wb') as f:
            f.write(signature)

        messagebox.showinfo("Успех", "Файл успешно подписан и сохранен в 'signature.sig'.")
        self.file_signed = True  # Установим флаг, что файл подписан

        # Активируем кнопку для отправки открытого ключа
        self.send_public_key_button.config(state=tk.NORMAL)

    def send_public_key(self):
        if not os.path.exists('public_key.pem'):
            messagebox.showwarning("Ошибка", "Открытый ключ не найден. Пожалуйста, сгенерируйте ключи.")
            return

        shutil.copy('public_key.pem', 'recipient_received_public_key.pem')
        messagebox.showinfo("Успех", "Открытый ключ отправлен Получателю.")


if __name__ == "__main__":
    root = tk.Tk()
    app = NotaryApp(root)
    root.geometry("300x200")
    root.mainloop()
