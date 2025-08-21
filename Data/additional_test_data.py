import pandas as pd
import random
import time
from datetime import datetime, timedelta

# Старт таймера
start_time = time.perf_counter()

# Генерация случайных данных
num_rows = int(input("Введите кол-во строк в таблице: "))

# Списки данных
clients = [f"Клиент {i}" for i in range(22, 50)]
regions = ["Брагино", "Фрунзе", "Заволга", "Перекоп"]
products = ["Продукт Д", "Продукт Е", "Продукт Ж", "Продукт М", "Продукт К", "Продукт Л", "Продукт Я"]
categories = ["Категория 4", "Категория 5", "Категория 6", "Категория 7"]
client_types = ["Физическое лицо", "Юр.лицо", "ИП", "Гос.предприятие"]
industries = ["IT", "Медицина", "Лёгкая промышленность", "Тяжёлая промышленность", "Образование"]

# 1. Создаем связи между сущностями
client_regions = {client: random.choice(regions) for client in clients}
product_categories = {product: random.choice(categories) for product in products}
client_info = {
    client: (random.choice(client_types), random.choice(industries))
    for client in clients
}

# Генерация основных данных
data = {
    "Дата продажи": [datetime.now() - timedelta(days=random.randint(0, 365)) for _ in range(num_rows)],
    "Клиент": [random.choice(clients) for _ in range(num_rows)],
    "Продукт": [random.choice(products) for _ in range(num_rows)],
    "Кол-во": [random.randint(1, 100) for _ in range(num_rows)],
    "Сумма": [round(random.uniform(100, 10000), 2) for _ in range(num_rows)],
}

df = pd.DataFrame(data)

df["Регион"] = df["Клиент"].map(client_regions)
df["Категория"] = df["Продукт"].map(product_categories)
df["Тип клиента"] = df["Клиент"].map(lambda x: client_info[x][0])
df["Отрасль"] = df["Клиент"].map(lambda x: client_info[x][1])

# Переупорядочиваем колонки
df = df[["Дата продажи", "Клиент", "Регион", "Тип клиента", "Отрасль",
         "Продукт", "Категория", "Кол-во", "Сумма"]]

# Сохранение в Excel
df.to_excel("data_sales(pro).xlsx", index=False)

# Дополнительная проверка
print("\n🔍 Пример данных:")
for i in range(min(3, len(clients))):
    client = clients[i]
    print(f"Клиент '{client}': {client_regions[client]}, {client_info[client][0]}, {client_info[client][1]}")

# Финиш таймера и вывод времени выполнения
end_time = time.perf_counter()
elapsed = end_time - start_time

if elapsed < 60:
    print(f"\n⏱️ Время генерации таблицы: {elapsed:.2f} секунд")
else:
    print(f"\n⏱️ Время генерации таблицы: {elapsed/60:.2f} минут")