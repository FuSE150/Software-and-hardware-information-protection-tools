import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import hashlib
import random
import time

# Параметры
p = 1019
q = 509
k = 3

# Функции программы
def hash_message(msg):
    hash_obj = hashlib.sha256(msg.encode())
    return int(hash_obj.hexdigest(), 16)

def generate_partial_R():
    t_alpha = random.randint(1, p - 1)
    R_alpha = pow(t_alpha, k, p)
    return t_alpha, R_alpha

def compute_combined_R(R_values):
    R = 1
    for R_alpha in R_values:
        R = (R * R_alpha) % p
    return R

def compute_e(R, H):
    return pow(R, H, q)

def compute_partial_S(x_alpha, e, t_alpha):
    return (pow(x_alpha, e, p) * t_alpha) % p

def compute_combined_S(S_values):
    S = 1
    for S_alpha in S_values:
        S = (S * S_alpha) % p
    return S

def compute_combined_y(y_values):
    y = 1
    for y_alpha in y_values:
        y = (y * y_alpha) % p
    return y

def verify_signature(S, y, e, H):
    y_inverse_e = pow(y, -e, p)
    R_check = (pow(S, k, p) * y_inverse_e) % p
    e_check = pow(R_check, H, q)
    return e_check == e, R_check, e_check

def select_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        file_path.set(filepath)

def sign_file():
    try:
        filepath = file_path.get()
        if not filepath:
            messagebox.showerror("Ошибка", "Файл не выбран!")
            return

        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()

        # Основные шаги
        num_users = int(users_entry.get())
        x_values = [random.randint(1, p - 1) for _ in range(num_users)]
        y_values = [pow(x, k, p) for x in x_values]

        t_values = []
        R_values = []
        for i in range(num_users):
            t_alpha, R_alpha = generate_partial_R()
            t_values.append(t_alpha)
            R_values.append(R_alpha)

        R = compute_combined_R(R_values)
        H = hash_message(content) % q
        e = compute_e(R, H)

        S_values = []
        for i in range(num_users):
            S_alpha = compute_partial_S(x_values[i], e, t_values[i])
            S_values.append(S_alpha)

        S = compute_combined_S(S_values)
        y = compute_combined_y(y_values)

        is_valid, R_check, e_check = verify_signature(S, y, e, H)

        # Добавляем метку времени
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # Создаем файл подписи
        signature_data = (
            f"Сообщение подписано: {timestamp}\n"
            f"Проверка подписи: {'Действительна' if is_valid else 'Недействительна'}\n"
            f"R = {R}, H = {H}, e = {e}\n"
            f"S = {S}, y = {y}, R_check = {R_check}, e_check = {e_check}"
        )

        signed_file = filepath.replace(".txt", "_signed.txt")
        with open(signed_file, "w", encoding="utf-8") as out_file:
            out_file.write(content + "\n\n" + signature_data)

        messagebox.showinfo("Успех", f"Файл подписан! Сохранено в: {signed_file}")

    except Exception as ex:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {ex}")

# Интерфейс
root = tk.Tk()
root.title("Подписание текстовых файлов")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

file_path = tk.StringVar()

ttk.Label(frame, text="Файл:").grid(row=0, column=0, sticky=tk.W, pady=5)
file_entry = ttk.Entry(frame, textvariable=file_path, width=50)
file_entry.grid(row=0, column=1, pady=5)
file_button = ttk.Button(frame, text="Выбрать файл", command=select_file)
file_button.grid(row=0, column=2, pady=5)

ttk.Label(frame, text="Количество пользователей:").grid(row=1, column=0, sticky=tk.W, pady=5)
users_entry = ttk.Entry(frame, width=10)
users_entry.insert(0, "100")  # По умолчанию 100 пользователей
users_entry.grid(row=1, column=1, pady=5)

sign_button = ttk.Button(frame, text="Подписать файл", command=sign_file)
sign_button.grid(row=2, column=0, columnspan=3, pady=10)

root.mainloop()
