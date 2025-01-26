import hashlib
import random

# Параметры
p = 1019   # Простое число для модуля
q = 509    # Простое число для модуля, отличное от p
k = 3      # Степень для вычисления R_alpha и проверки подписи

# Сообщение для подписи
message = "Test message for signature"

# Функция хеширования
def hash_message(msg):
    hash_obj = hashlib.sha256(msg.encode())
    return int(hash_obj.hexdigest(), 16)

# Шаг 1: Генерация случайных значений t_alpha и вычисление частных R_alpha
def generate_partial_R():
    t_alpha = random.randint(1, p - 1)  # Случайное число < p
    R_alpha = pow(t_alpha, k, p)        # R_alpha = (t_alpha)^k mod p
    return t_alpha, R_alpha

# Шаг 2: Объединение всех R_alpha
def compute_combined_R(R_values):
    R = 1
    for R_alpha in R_values:
        R = (R * R_alpha) % p
    return R

# Шаг 3: Вычисление e
def compute_e(R, H):
    return pow(R, H, q)  # e = R^H mod q

# Шаг 4: Вычисление частных S_alpha для каждого пользователя
def compute_partial_S(x_alpha, e, t_alpha):
    return (pow(x_alpha, e, p) * t_alpha) % p  # S_alpha = x_alpha^e * t_alpha mod p

# Шаг 5: Объединение всех S_alpha
def compute_combined_S(S_values):
    S = 1
    for S_alpha in S_values:
        S = (S * S_alpha) % p
    return S

# Шаг 6: Вычисление коллективного открытого ключа y
def compute_combined_y(y_values):
    y = 1
    for y_alpha in y_values:
        y = (y * y_alpha) % p
    return y

# Шаг 7: Проверка подписи
def verify_signature(S, y, e, H):
    # Вычисляем R_check = S^k * y^(-e) mod p
    y_inverse_e = pow(y, -e, p)  # Инверсия y^e mod p
    R_check = (pow(S, k, p) * y_inverse_e) % p
    # Вычисляем e' = R_check^H mod q
    e_check = pow(R_check, H, q)
    return e_check == e, R_check, e_check

# Основной процесс
num_users = 100  # Количество пользователей
x_values = [random.randint(1, p - 1) for _ in range(num_users)]  # Секретные ключи пользователей
y_values = [pow(x, k, p) for x in x_values]  # Открытые ключи пользователей

# Шаг 1 и 2: Генерация t_alpha и R_alpha, вычисление объединённого R
t_values = []
R_values = []
for i in range(num_users):
    t_alpha, R_alpha = generate_partial_R()
    t_values.append(t_alpha)
    R_values.append(R_alpha)
    print(f"Пользователь {i+1}: t_alpha = {t_alpha}, R_alpha = {R_alpha}")

R = compute_combined_R(R_values)
print(f"\nШаг 2: Объединённое R = {R}")

# Шаг 3: Вычисление хеша и e
H = hash_message(message) % q  # Ограничиваем H по модулю q для отладки
e = compute_e(R, H)
print(f"\nШаг 3: Хеш сообщения H = {H}, e = {e}")

# Шаг 4: Вычисление частных S_alpha для каждого пользователя
S_values = []
for i in range(num_users):
    S_alpha = compute_partial_S(x_values[i], e, t_values[i])
    S_values.append(S_alpha)
    print(f"Пользователь {i+1}: x_alpha = {x_values[i]}, S_alpha = {S_alpha}")

# Шаг 5: Объединённое S
S = compute_combined_S(S_values)
print(f"\nШаг 5: Объединённое S = {S}")

# Шаг 6: Коллективный открытый ключ y
y = compute_combined_y(y_values)
print(f"\nШаг 6: Коллективный открытый ключ y = {y}")

# Шаг 7: Проверка подписи
is_valid, R_check, e_check = verify_signature(S, y, e, H)
print("\nШаг 7: Проверка подписи")
print(f"R_check = {R_check}")
print(f"e_check = {e_check}")
print(f"e (ожидаемое) = {e}")
print(f"\nРезультат: Подпись {'действительна' if is_valid else 'недействительна'}")

# Промежуточные значения для отладки
print("\nПромежуточные значения для отладки:")
print(f"R (объединённое) = {R}")
print(f"S (объединённое) = {S}")
print(f"Хеш H (сообщения) = {H}")
print(f"Значение e (подпись) = {e}")
print(f"Значение e_check (проверка подписи) = {e_check}")
print(f"Коллективный открытый ключ y = {y}")
