import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext  # Импортируем для многострочного текстового поля
import shutil
import os


class SenderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Отправитель")

        self.file_path = None

        # Создаем текстовое поле для ввода сообщения
        self.message_label = tk.Label(root, text="Введите сообщение:")
        self.message_label.pack(pady=5)

        self.message_text = scrolledtext.ScrolledText(root, width=40, height=10)
        self.message_text.pack(pady=5)

        # Кнопка для создания файла
        self.create_file_button = tk.Button(root, text="Создать файл", command=self.create_file)
        self.create_file_button.pack(pady=5)

        # Кнопка для отправки файла Нотариусу
        self.send_to_notary_button = tk.Button(root, text="Отправить файл Нотариусу", command=self.send_to_notary,
                                               state=tk.DISABLED)
        self.send_to_notary_button.pack(pady=5)

        # Кнопка для отправки файла и подписи Получателю
        self.send_to_recipient_button = tk.Button(root, text="Отправить файл и подпись Получателю",
                                                  command=self.send_to_recipient, state=tk.DISABLED)
        self.send_to_recipient_button.pack(pady=5)

    def create_file(self):
        # Получаем текст сообщения из текстового поля
        message = self.message_text.get("1.0", tk.END).strip()
        if not message:
            messagebox.showwarning("Ошибка", "Сообщение не может быть пустым.")
            return

        self.file_path = 'file.txt'
        with open(self.file_path, 'w') as f:
            f.write(message)
        messagebox.showinfo("Успех", f"Файл '{self.file_path}' успешно создан.")

        # Активируем кнопку для отправки файла Нотариусу
        self.send_to_notary_button.config(state=tk.NORMAL)

    def send_to_notary(self):
        if self.file_path:
            notary_file_path = 'notary_received_file.txt'
            shutil.copy(self.file_path, notary_file_path)
            messagebox.showinfo("Успех", f"Файл отправлен Нотариусу: {notary_file_path}")

            # Активируем кнопку для отправки Получателю только после отправки
            self.send_to_recipient_button.config(state=tk.NORMAL)

    def send_to_recipient(self):
        # Копируем файл и подпись для Получателя
        try:
            shutil.copy('file.txt', 'recipient_file.txt')
            shutil.copy('signature.sig', 'recipient_signature.sig')
            messagebox.showinfo("Успех", "Файл и подпись успешно отправлены Получателю.")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при отправке файла и подписи: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SenderApp(root)
    root.geometry("400x400")
    root.mainloop()
