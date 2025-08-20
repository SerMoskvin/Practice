import pandas as pd
import random
from datetime import datetime, timedelta

# Генерация случайных данных
num_rows = 1000

# Список клиентов, регионов и продуктов
clients = [f"Клиент {i}" for i in range(22, 50)]
regions = ["Брагино", "Фрунзе", "Заволга", "Перекоп"]
products = ["Продукт Д", "Продукт Е", "Продукт Ж", "Продукт М"]
categories = ["Категория 4", "Категория 5", "Категория 6"]
client_type = ["Физическое лицо", "Юр.лицо", "ИП", "Гос.предприятие"]
industry_category = ["IT", "Медицина", "Лёгкая промышленность", "Тяжёлая промышленность", "Образование"]

# Словарь для хранения типа клиента и отрасли
client_info = {
    client: (random.choice(client_type), random.choice(industry_category))
    for client in clients
}

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

# Создание DataFrame сначала
df = pd.DataFrame(data)

# Теперь добавляем тип клиента и отрасль, используя уже созданный DataFrame
df["Тип клиента"] = df["Клиент"].map(lambda x: client_info[x][0])
df["Отрасль"] = df["Клиент"].map(lambda x: client_info[x][1])

# Сохранение в Excel
df.to_excel("data_sales(pro).xlsx", index=False)