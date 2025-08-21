def calculate_basic_stats(df):
    """Расчет базовой статистики"""
    stats = {}

    if df is not None:
        stats['total_revenue'] = df['Сумма'].sum() if 'Сумма' in df.columns else 0
        stats['total_quantity'] = df['Кол-во'].sum() if 'Кол-во' in df.columns else 0
        stats['avg_check'] = stats['total_revenue'] / stats['total_quantity'] if stats['total_quantity'] > 0 else 0
        stats['unique_categories'] = df['Категория'].nunique() if 'Категория' in df.columns else 0
        stats['unique_products'] = df['Продукт'].nunique() if 'Продукт' in df.columns else 0
        stats['unique_regions'] = df['Регион'].nunique() if 'Регион' in df.columns else 0
        stats['unique_clients'] = df['Клиент'].nunique() if 'Клиент' in df.columns else 0

    return stats


def print_basic_stats(stats):
    """Вывод базовой статистики"""
    print("📊 ОСНОВНАЯ СТАТИСТИКА:")
    print("=" * 40)
    print(f"Общая выручка: {stats['total_revenue']:,.0f} руб.")
    print(f"Общее количество: {stats['total_quantity']:,.0f} шт.")
    print(f"Средний чек: {stats['avg_check']:,.0f} руб.")
    print(f"Уникальных категорий: {stats['unique_categories']}")
    print(f"Уникальных продуктов: {stats['unique_products']}")
    print(f"Уникальных регионов: {stats['unique_regions']}")
    if stats['unique_clients'] > 0:
        print(f"Уникальных клиентов: {stats['unique_clients']}")