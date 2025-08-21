import pandas as pd
import random
import time
from datetime import datetime, timedelta

# Старт таймера
start_time = time.perf_counter()

# Генерация случайных данных
num_rows = int(input("Введите кол-во строк в таблице: "))

# Списки данных
clients = [f"Клиент {i}" for i in range(1, 21)]
regions = ["Ярославль", "Кострома", "Рыбинск", "Москва"]
products = ["Продукт A", "Продукт B", "Продукт C", "Продукт D", "Продукт E", "Продукт F", "Продукт G", "Продукт Y"]
categories = ["Категория 1", "Категория 2", "Категория 3", "Категория 4"]

client_regions = {client: random.choice(regions) for client in clients}
product_categories = {product: random.choice(categories) for product in products}

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

# Переупорядочиваем колонки для красоты
df = df[["Дата продажи", "Клиент", "Регион", "Продукт", "Категория", "Кол-во", "Сумма"]]

# Сохранение в Excel
df.to_excel("sales_data.xlsx", index=False)

# Финиш таймера и вывод времени выполнения
end_time = time.perf_counter()
elapsed = end_time - start_time

if elapsed < 60:
    print(f"\n⏱️ Время генерации таблицы: {elapsed:.2f} секунд")
else:
    print(f"\n⏱️ Время генерации таблицы: {elapsed/60:.2f} минут")
