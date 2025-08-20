import pandas as pd
import random
from datetime import datetime, timedelta

# Генерация случайных данных
num_rows = 1000

# Список клиентов, регионов и продуктов
clients = [f"Клиент {i}" for i in range(1, 21)]
regions = ["Ярославль", "Кострома", "Рыбинск", "Москва"]
products = ["Продукт A", "Продукт B", "Продукт C", "Продукт D"]
categories = ["Категория 1", "Категория 2", "Категория 3"]

# Генерация данных
data = {
    "Дата продажи": [datetime.now() - timedelta(days=random.randint(0, 365)) for _ in range(num_rows)],
    "Клиент": [random.choice(clients) for _ in range(num_rows)],
    "Регион": [random.choice(regions) for _ in range(num_rows)],
    "Продукт": [random.choice(products) for _ in range(num_rows)],
    "Категория": [random.choice(categories) for _ in range(num_rows)],
    "Кол-во": [random.randint(1, 100) for _ in range(num_rows)],
    "Сумма": [round(random.uniform(100, 10000), 2) for _ in range(num_rows)],
}

# Создание DataFrame
df = pd.DataFrame(data)

# Сохранение в Excel
df.to_excel("sales_data.xlsx", index=False)