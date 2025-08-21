# Конфигурационный файл для настройки обработки данных

# Путь к файлу с данными
# DATA_FILE_PATH = "C:/Users/Joker/PycharmProjects/Practice/Data/sales_data.xlsx"
DATA_FILE_PATH = "../Data/sales_data.xlsx"

# Настройки очистки данных
CLEANING_CONFIG = {
    # Удаление строк с определенными значениями в столбцах
    "remove_rows_with_values": {
        # "Регион": ["Кострома", "test", "TEST"],
        # "Категория": ["Тест", "test"],
        # "Продукт": ["тестовый", "test"]
    },

    # Дополнительные условия для удаления строк
    "custom_conditions": [
        # Пример: удалить строки, где количество больше 1000
        # "`Кол-во` > 1000",
        # Пример: удалить строки, где сумма меньше 10
        # "`Сумма` < 10"
    ],

    # Столбцы, которые не должны содержать пустые значения
    "required_columns": ["Дата продажи", "Кол-во", "Сумма"]
}

# Конфигурация для модели Prophet
PROPHET_CONFIG = {
    "model_params": {
        "seasonality_mode": "multiplicative",  # 'additive' or 'multiplicative'
        "yearly_seasonality": True,
        "weekly_seasonality": True,
        "daily_seasonality": False,
        "changepoint_prior_scale": 0.05,
        "seasonality_prior_scale": 10.0,
        "holidays_prior_scale": 10.0,
    },
    "forecast_params": {
        "periods": 90,  # Прогноз на 90 дней вперед
        "freq": 'D',     # Частота прогноза ('D' - день, 'W' - неделя, 'M' - месяц)
    },
    "country_holidays": "RU",  # Код страны для автоматического добавления праздников (Russia)
    # Полный список: https://github.com/dr-prodigy/python-holidays
}