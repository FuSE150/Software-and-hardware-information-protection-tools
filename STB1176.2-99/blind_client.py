import random
from hashlib import sha256


def generate_random_in_range(min_val, max_val):
    """Генерация случайного числа в заданном диапазоне."""
    return random.randint(min_val, max_val)


def hash_function(data):
    """Функция хеширования SHA-256 с приведением результата к диапазону (0, q-1)."""
    return int(sha256(data.encode()).hexdigest(), 16)


def blind_signature_protocol(M, q, a, x, y):
    # Шаг 1: Подписывающий генерирует случайное k и вычисляет R
    k = generate_random_in_range(2, q - 1)
    R = pow(a, k, q)
    print(f"Подписывающий: Сгенерировано k = {k}, Вычислено R = {R}")

    # Передача R пользователю

    # Шаг 2: Пользователь генерирует случайные числа ε и τ
    e = generate_random_in_range(2, q - 1)
    t = generate_random_in_range(2, q - 1)

    # Вычисление R' и E'
    R_dash = (R * pow(y, e, q) * pow(a, t, q)) % q
    E_dash = hash_function(str(R_dash) + M) % (q - 1)  # Приводим к диапазону (0, q-1)
    E = (E_dash - t) % (q - 1)
    print(f"Пользователь: Сгенерировано e = {e}, t = {t}, Вычислено R' = {R_dash}, E' = {E_dash}, E = {E}")

    # Передача E подписывающему

    # Шаг 3: Подписывающий вычисляет второй элемент подписи S
    S = (k - x * E) % (q - 1)
    print(f"Подписывающий: Вычислено S = {S}")

    # Передача S пользователю

    # Шаг 4: Пользователь вычисляет S'
    S_dash = (S + t) % (q - 1)
    print(f"Пользователь: Вычислено S' = {S_dash}")

    # Подпись, состоящая из (E, S'), готова
    return E, S_dash, R_dash, M




# Параметры
q = 1019  # модуль, простое число
a = 2  # порождающий элемент
x = 5  # закрытый ключ
y = pow(a, x, q)  # открытый ключ

# Сообщение
M = "Привет"

# Выполнение протокола
E, S_dash, R_dash, M = blind_signature_protocol(M, q, a, x, y)
print(f"Слепая подпись: (E = {E}, S' = {S_dash})")
