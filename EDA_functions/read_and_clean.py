import pandas as pd
import warnings

warnings.filterwarnings('ignore')

from config import DATA_FILE_PATH, CLEANING_CONFIG


def load_data(file_path=DATA_FILE_PATH):
    """Загрузка данных из Excel файла"""
    try:
        df = pd.read_excel(file_path)
        print(f"✅ Данные загружены. Размер: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"❌ Файл не найден: {file_path}")
        return None
    except Exception as e:
        print(f"❌ Ошибка загрузки: {e}")
        return None


def clean_data(df):
    """Очистка данных на основе конфигурации"""
    if df is None:
        return None

    df_clean = df.copy()
    initial_size = len(df_clean)

    # 1. Проверка обязательных столбцов
    required_columns = CLEANING_CONFIG.get("required_columns", [])
    missing_columns = [col for col in required_columns if col not in df_clean.columns]
    if missing_columns:
        print(f"❌ Отсутствуют столбцы: {missing_columns}")
        return None

    # 2. Удаление пропусков
    removed_nulls = 0
    for column in required_columns:
        before = len(df_clean)
        df_clean = df_clean.dropna(subset=[column])
        removed_nulls += (before - len(df_clean))
    if removed_nulls > 0:
        print(f"✅ Удалено строк с пропусками: {removed_nulls}")

    # 3. Преобразование типов
    try:
        if 'Дата продажи' in df_clean.columns:
            df_clean['Дата продажи'] = pd.to_datetime(df_clean['Дата продажи'], errors='coerce')
        if 'Кол-во' in df_clean.columns:
            df_clean['Кол-во'] = pd.to_numeric(df_clean['Кол-во'], errors='coerce')
        if 'Сумма' in df_clean.columns:
            df_clean['Сумма'] = pd.to_numeric(df_clean['Сумма'], errors='coerce')
    except Exception as e:
        print(f"❌ Ошибка преобразования типов: {e}")
        return None

    # 4. Удаление по значениям из конфига
    remove_config = CLEANING_CONFIG.get("remove_rows_with_values", {})
    removed_by_values = 0
    for column, values_to_remove in remove_config.items():
        if column in df_clean.columns:
            before = len(df_clean)
            df_clean = df_clean[~df_clean[column].isin(values_to_remove)]
            removed = before - len(df_clean)
            removed_by_values += removed
            if removed > 0:
                print(f"✅ Удалено из {column}: {removed}")

    # 5. Удаление по пользовательским условиям
    custom_conditions = CLEANING_CONFIG.get("custom_conditions", [])
    removed_by_conditions = 0
    for condition in custom_conditions:
        try:
            before = len(df_clean)
            df_clean = df_clean.query(f"not ({condition})")
            removed = before - len(df_clean)
            removed_by_conditions += removed
            if removed > 0:
                print(f"✅ Удалено по условию '{condition}': {removed}")
        except:
            print(f"⚠️ Не удалось применить условие: {condition}")

    # 6. Удаление отрицательных значений
    if 'Кол-во' in df_clean.columns:
        before = len(df_clean)
        df_clean = df_clean[df_clean['Кол-во'] >= 0]
        removed_negative_qty = before - len(df_clean)
        if removed_negative_qty > 0:
            print(f"✅ Удалено с отрицательным количеством: {removed_negative_qty}")

    if 'Сумма' in df_clean.columns:
        before = len(df_clean)
        df_clean = df_clean[df_clean['Сумма'] >= 0]
        removed_negative_sum = before - len(df_clean)
        if removed_negative_sum > 0:
            print(f"✅ Удалено с отрицательной суммой: {removed_negative_sum}")

    # 7. Добавление временных признаков
    if 'Дата продажи' in df_clean.columns:
        df_clean['Год'] = df_clean['Дата продажи'].dt.year
        df_clean['Месяц'] = df_clean['Дата продажи'].dt.month
        df_clean['Квартал'] = df_clean['Дата продажи'].dt.quarter
        df_clean['День недели'] = df_clean['Дата продажи'].dt.dayofweek

    # 8. Итоговая статистика
    final_size = len(df_clean)
    print(f"📊 Итоги: {initial_size} → {final_size} строк")

    return df_clean if final_size > 0 else None


def prepare_for_prophet(df, target_column='Сумма'):
    """Подготовка данных для Prophet"""
    if df is None or 'Дата продажи' not in df.columns or target_column not in df.columns:
        print("❌ Недостаточно данных для Prophet")
        return None

    daily_data = df.groupby('Дата продажи')[target_column].sum().reset_index()
    daily_data.columns = ['ds', 'y']

    date_range = pd.date_range(start=daily_data['ds'].min(), end=daily_data['ds'].max(), freq='D')
    full_range = pd.DataFrame({'ds': date_range})
    prophet_data = full_range.merge(daily_data, on='ds', how='left')
    prophet_data['y'] = prophet_data['y'].fillna(0)

    print(f"✅ Данные для Prophet подготовлены")
    return prophet_data

