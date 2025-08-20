import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


def setup_visuals():
    """Настройка стиля графиков"""
    plt.style.use('default')
    sns.set_palette("husl")
    plt.rcParams['figure.figsize'] = (12, 8)
    plt.rcParams['font.size'] = 12


def plot_revenue_by_category(df, top_n=10):
    """Выручка по категориям - какие направления приносят больше прибыли"""
    if 'Категория' not in df.columns or 'Сумма' not in df.columns:
        print("❌ Отсутствуют необходимые столбцы для анализа выручки по категориям")
        return

    category_revenue = df.groupby('Категория')['Сумма'].sum().sort_values(ascending=False)

    if len(category_revenue) > top_n:
        top_categories = category_revenue.head(top_n)
        other_revenue = category_revenue[top_n:].sum()
        top_categories['Другие'] = other_revenue
    else:
        top_categories = category_revenue

    plt.figure(figsize=(14, 8))

    bars = plt.bar(range(len(top_categories)), top_categories.values)
    plt.title('Выручка по категориям товаров', fontsize=16, fontweight='bold')
    plt.xlabel('Категория')
    plt.ylabel('Выручка, руб.')
    plt.xticks(range(len(top_categories)), top_categories.index, rotation=45, ha='right')

    # Добавляем подписи значений на столбцах
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + height * 0.01,
                 f'{height:,.0f}', ha='center', va='bottom', fontsize=10)

    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Выводим статистику
    print("📊 Выручка по категориям:")
    for i, (category, revenue) in enumerate(top_categories.items(), 1):
        print(f"{i}. {category}: {revenue:,.0f} руб.")


def plot_quantity_by_category(df, top_n=10):
    """Количество продаж по категориям - сколько заказов было в каждой группе"""
    if 'Категория' not in df.columns or 'Кол-во' not in df.columns:
        print("❌ Отсутствуют необходимые столбцы для анализа количества по категориям")
        return

    category_quantity = df.groupby('Категория')['Кол-во'].sum().sort_values(ascending=False)

    if len(category_quantity) > top_n:
        top_categories = category_quantity.head(top_n)
        other_quantity = category_quantity[top_n:].sum()
        top_categories['Другие'] = other_quantity
    else:
        top_categories = category_quantity

    plt.figure(figsize=(14, 8))

    bars = plt.bar(range(len(top_categories)), top_categories.values, color='lightgreen')
    plt.title('Количество продаж по категориям', fontsize=16, fontweight='bold')
    plt.xlabel('Категория')
    plt.ylabel('Количество, шт.')
    plt.xticks(range(len(top_categories)), top_categories.index, rotation=45, ha='right')

    # Добавляем подписи значений
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + height * 0.01,
                 f'{height:,.0f}', ha='center', va='bottom', fontsize=10)

    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("📦 Количество продаж по категориям:")
    for i, (category, quantity) in enumerate(top_categories.items(), 1):
        print(f"{i}. {category}: {quantity:,.0f} шт.")


def plot_avg_check_by_region(df, top_n=15):
    """Средний чек по регионам - насколько отличаются суммы покупок"""
    if 'Регион' not in df.columns or 'Сумма' not in df.columns:
        print("❌ Отсутствуют необходимые столбцы для анализа среднего чека по регионам")
        return

    region_avg_check = df.groupby('Регион')['Сумма'].mean().sort_values(ascending=False)

    if len(region_avg_check) > top_n:
        top_regions = region_avg_check.head(top_n)
    else:
        top_regions = region_avg_check

    plt.figure(figsize=(14, 8))

    bars = plt.bar(range(len(top_regions)), top_regions.values, color='orange')
    plt.title('Средний чек по регионам', fontsize=16, fontweight='bold')
    plt.xlabel('Регион')
    plt.ylabel('Средний чек, руб.')
    plt.xticks(range(len(top_regions)), top_regions.index, rotation=45, ha='right')

    # Добавляем подписи значений
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + height * 0.01,
                 f'{height:,.0f}', ha='center', va='bottom', fontsize=10)

    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("💰 Средний чек по регионам:")
    for i, (region, avg_check) in enumerate(top_regions.items(), 1):
        print(f"{i}. {region}: {avg_check:,.0f} руб.")


def plot_sales_frequency_by_product(df, top_n=15):
    """Частота продаж по продуктам - что популярнее всего"""
    if 'Продукт' not in df.columns:
        print("❌ Отсутствует столбец 'Продукт' для анализа частоты продаж")
        return

    product_frequency = df['Продукт'].value_counts().head(top_n)

    plt.figure(figsize=(14, 8))

    bars = plt.bar(range(len(product_frequency)), product_frequency.values, color='purple')
    plt.title('Частота продаж по продуктам (Топ-15)', fontsize=16, fontweight='bold')
    plt.xlabel('Продукт')
    plt.ylabel('Количество продаж')
    plt.xticks(range(len(product_frequency)), product_frequency.index, rotation=45, ha='right')

    # Добавляем подписи значений
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + height * 0.01,
                 f'{height:,.0f}', ha='center', va='bottom', fontsize=10)

    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

    print("🏆 Самые популярные продукты:")
    for i, (product, count) in enumerate(product_frequency.items(), 1):
        print(f"{i}. {product}: {count} продаж")


def plot_monthly_revenue_trend(df):
    """Тренд выручки по месяцам с детальной статистикой"""
    if 'Дата продажи' in df.columns and 'Сумма' in df.columns:
        # Агрегация по месяцам
        monthly_revenue = df.groupby(['Год', 'Месяц'])['Сумма'].sum().reset_index()

        # Создание даты для графика
        monthly_revenue['Дата'] = monthly_revenue.apply(
            lambda row: pd.to_datetime(f"{int(row['Год'])}-{int(row['Месяц'])}-01"), axis=1
        )

        # Создание строкового представления для таблицы
        monthly_revenue['Месяц_Год'] = monthly_revenue['Месяц'].astype(str) + '.' + monthly_revenue['Год'].astype(str)

        # Сортировка по дате
        monthly_revenue = monthly_revenue.sort_values('Дата')

        # 1. ВЫВОД ТАБЛИЦЫ С ДАННЫМИ
        print("📅 ВЫРУЧКА ПО МЕСЯЦАМ:")
        print("=" * 50)
        print(f"{'Месяц':<10} {'Выручка, руб.':<15} {'Изменение, %':<12} {'Доля, %':<8}")
        print("-" * 50)

        total_revenue = monthly_revenue['Сумма'].sum()
        prev_revenue = None

        for _, row in monthly_revenue.iterrows():
            current_revenue = row['Сумма']
            percentage = (current_revenue / total_revenue) * 100

            # Расчет изменения относительно предыдущего месяца
            if prev_revenue is not None and prev_revenue != 0:
                change_percent = ((current_revenue - prev_revenue) / prev_revenue) * 100
                change_str = f"{change_percent:+.1f}%"
            else:
                change_str = "N/A"

            print(f"{row['Месяц_Год']:<10} {current_revenue:>12,.0f} {change_str:>12} {percentage:>7.1f}%")
            prev_revenue = current_revenue

        print("-" * 50)
        print(f"{'ИТОГО':<10} {total_revenue:>12,.0f} {'':>12} {'100.0':>7}%")

        # 2. СТАТИСТИКА
        print("\n📊 СТАТИСТИКА ПО МЕСЯЦАМ:")
        print(f"• Средняя месячная выручка: {monthly_revenue['Сумма'].mean():,.0f} руб.")
        print(f"• Максимальная выручка: {monthly_revenue['Сумма'].max():,.0f} руб.")
        print(f"• Минимальная выручка: {monthly_revenue['Сумма'].min():,.0f} руб.")
        print(f"• Стандартное отклонение: {monthly_revenue['Сумма'].std():,.0f} руб.")

        # 3. РОСТ/ПАДЕНИЕ
        if len(monthly_revenue) > 1:
            first_month = monthly_revenue['Сумма'].iloc[0]
            last_month = monthly_revenue['Сумма'].iloc[-1]
            if first_month > 0:
                total_growth = ((last_month - first_month) / first_month) * 100
                print(f"• Общий рост за период: {total_growth:+.1f}%")

        # 4. ГРАФИК
        plt.figure(figsize=(15, 8))

        # Основной график
        plt.subplot(2, 1, 1)
        plt.plot(monthly_revenue['Дата'], monthly_revenue['Сумма'], marker='o', linewidth=2,
                 color='green', markersize=6)
        plt.title('Тренд выручки по месяцам', fontsize=16, fontweight='bold')
        plt.xlabel('Дата')
        plt.ylabel('Выручка, руб.')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)

        # Добавление значений на график
        for i, (date, revenue) in enumerate(zip(monthly_revenue['Дата'], monthly_revenue['Сумма'])):
            plt.annotate(f'{revenue:,.0f}',
                         (date, revenue),
                         textcoords="offset points",
                         xytext=(0, 10),
                         ha='center',
                         fontsize=9,
                         bbox=dict(boxstyle="round,pad=0.3", facecolor="yellow", alpha=0.7))

        # График помесячного изменения
        plt.subplot(2, 1, 2)
        monthly_revenue['Изменение'] = monthly_revenue['Сумма'].pct_change() * 100
        colors = ['red' if x < 0 else 'green' for x in monthly_revenue['Изменение']]

        bars = plt.bar(monthly_revenue['Дата'], monthly_revenue['Изменение'], color=colors, alpha=0.7)
        plt.title('Изменение выручки по месяцам (%)', fontsize=14, fontweight='bold')
        plt.xlabel('Дата')
        plt.ylabel('Изменение, %')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)

        # Добавление значений на bars
        for bar, change in zip(bars, monthly_revenue['Изменение']):
            if not pd.isna(change):
                height = bar.get_height()
                va = 'bottom' if height >= 0 else 'top'
                color = 'green' if height >= 0 else 'red'
                plt.text(bar.get_x() + bar.get_width() / 2., height,
                         f'{change:+.1f}%', ha='center', va=va, fontsize=9, color=color,
                         bbox=dict(boxstyle="round,pad=0.2", facecolor="white", alpha=0.8))

        plt.tight_layout()
        plt.show()

        # 5. СЕЗОННОСТЬ
        print("\n🌡️ АНАЛИЗ СЕЗОННОСТИ:")
        # Средняя выручка по месяцам (игнорируя год)
        monthly_avg = df.groupby('Месяц')['Сумма'].mean()
        months_ru = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн', 'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']

        if len(monthly_avg) > 0:
            best_month = monthly_avg.idxmax()
            worst_month = monthly_avg.idxmin()
            print(f"• Самый прибыльный месяц: {months_ru[best_month - 1]} ({monthly_avg.max():,.0f} руб.)")
            print(f"• Самый непродажный месяц: {months_ru[worst_month - 1]} ({monthly_avg.min():,.0f} руб.)")

            # Коэффициент сезонности
            seasonality_ratio = monthly_avg.max() / monthly_avg.min() if monthly_avg.min() > 0 else 0
            print(f"• Коэффициент сезонности: {seasonality_ratio:.1f}x")

def plot_client_type_analysis(df):
    """Анализ продаж по типу клиента"""
    print("\n" + "=" * 50)
    print("АНАЛИЗ ПО ТИПУ КЛИЕНТА")
    print("=" * 50)

    # Выручка по типам клиентов
    client_revenue = df.groupby('Тип клиента')['Сумма'].sum().sort_values(ascending=False)

    plt.figure(figsize=(12, 8))
    bars = plt.bar(range(len(client_revenue)), client_revenue.values, color='teal')
    plt.title('Выручка по типам клиентов', fontsize=16, fontweight='bold')
    plt.xlabel('Тип клиента')
    plt.ylabel('Выручка, руб.')
    plt.xticks(range(len(client_revenue)), client_revenue.index, rotation=45, ha='right')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + height * 0.01,
                 f'{height:,.0f}', ha='center', va='bottom', fontsize=10)

    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Количество сделок по типам клиентов
    client_count = df['Тип клиента'].value_counts()

    plt.figure(figsize=(12, 8))
    bars = plt.bar(range(len(client_count)), client_count.values, color='orange')
    plt.title('Количество сделок по типам клиентов', fontsize=16, fontweight='bold')
    plt.xlabel('Тип клиента')
    plt.ylabel('Количество сделок')
    plt.xticks(range(len(client_count)), client_count.index, rotation=45, ha='right')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + height * 0.01,
                 f'{height:,.0f}', ha='center', va='bottom', fontsize=10)

    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Доля по типам клиентов (круговая диаграмма)
    plt.figure(figsize=(10, 8))
    colors = ['gold', 'lightcoral', 'lightskyblue', 'lightgreen', 'plum']
    wedges, texts, autotexts = plt.pie(client_revenue.values, labels=client_revenue.index, autopct='%1.1f%%',
                                       colors=colors[:len(client_revenue)], startangle=90)
    plt.title('Доля выручки по типам клиентов', fontsize=16, fontweight='bold')
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

    # Статистика
    print("📊 Статистика по типам клиентов:")
    total_revenue = client_revenue.sum()
    for i, (client_type, revenue) in enumerate(client_revenue.items(), 1):
        percentage = (revenue / total_revenue) * 100
        count = client_count.get(client_type, 0)
        avg_check = revenue / count if count > 0 else 0
        print(
            f"{i}. {client_type}: {revenue:,.0f} руб. ({percentage:.1f}%), {count} сделок, ср.чек: {avg_check:,.0f} руб.")


def plot_industry_analysis(df):
    """Анализ выручки по отраслям"""
    print("\n" + "=" * 50)
    print("АНАЛИЗ ПО ОТРАСЛЯМ")
    print("=" * 50)

    # Выручка по отраслям
    industry_revenue = df.groupby('Отрасль')['Сумма'].sum().sort_values(ascending=False)

    # Топ-10 отраслей
    top_industries = industry_revenue.head(10)

    plt.figure(figsize=(14, 8))
    bars = plt.bar(range(len(top_industries)), top_industries.values, color='navy')
    plt.title('Выручка по отраслям (Топ-10)', fontsize=16, fontweight='bold')
    plt.xlabel('Отрасль')
    plt.ylabel('Выручка, руб.')
    plt.xticks(range(len(top_industries)), top_industries.index, rotation=45, ha='right')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + height * 0.01,
                 f'{height:,.0f}', ha='center', va='bottom', fontsize=10, color='white')

    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Количество клиентов по отраслям
    industry_clients = df.groupby('Отрасль')['Клиент'].nunique().sort_values(ascending=False).head(10)

    plt.figure(figsize=(14, 8))
    bars = plt.bar(range(len(industry_clients)), industry_clients.values, color='darkgreen')
    plt.title('Количество клиентов по отраслям (Топ-10)', fontsize=16, fontweight='bold')
    plt.xlabel('Отрасль')
    plt.ylabel('Количество клиентов')
    plt.xticks(range(len(industry_clients)), industry_clients.index, rotation=45, ha='right')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + height * 0.01,
                 f'{height:,.0f}', ha='center', va='bottom', fontsize=10)

    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Средний чек по отраслям
    industry_avg_check = df.groupby('Отрасль')['Сумма'].mean().sort_values(ascending=False).head(10)

    plt.figure(figsize=(14, 8))
    bars = plt.bar(range(len(industry_avg_check)), industry_avg_check.values, color='darkred')
    plt.title('Средний чек по отраслям (Топ-10)', fontsize=16, fontweight='bold')
    plt.xlabel('Отрасль')
    plt.ylabel('Средний чек, руб.')
    plt.xticks(range(len(industry_avg_check)), industry_avg_check.index, rotation=45, ha='right')

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2., height + height * 0.01,
                 f'{height:,.0f}', ha='center', va='bottom', fontsize=10)

    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    plt.show()

    # Статистика
    print("📊 Статистика по отраслям:")
    total_revenue = industry_revenue.sum()
    for i, (industry, revenue) in enumerate(industry_revenue.head(15).items(), 1):
        percentage = (revenue / total_revenue) * 100
        clients_count = industry_clients.get(industry, 0)
        avg_check = industry_avg_check.get(industry, 0)
        print(
            f"{i}. {industry}: {revenue:,.0f} руб. ({percentage:.1f}%), {clients_count} клиентов, ср.чек: {avg_check:,.0f} руб.")

def plot_additional_analysis(df):
    """Дополнительные графики анализа"""
    # Динамика продаж по месяцам
    if 'Дата продажи' in df.columns and 'Сумма' in df.columns:
        monthly_sales = df.groupby(['Год', 'Месяц'])['Сумма'].sum().reset_index()
        monthly_sales['Месяц_год'] = monthly_sales['Месяц'].astype(str) + '-' + monthly_sales['Год'].astype(str)

        plt.figure(figsize=(15, 6))
        plt.plot(monthly_sales['Месяц_год'], monthly_sales['Сумма'], marker='o', linewidth=2, color='blue')
        plt.title('Динамика продаж по месяцам', fontsize=16, fontweight='bold')
        plt.xlabel('Месяц-Год')
        plt.ylabel('Выручка, руб.')
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()

    # Продажи по дням недели
    if 'День недели' in df.columns and 'Сумма' in df.columns:
        weekday_sales = df.groupby('День недели')['Сумма'].sum()
        days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']

        plt.figure(figsize=(10, 6))
        plt.bar(range(len(weekday_sales)), weekday_sales.values, color='red')
        plt.title('Продажи по дням недели', fontsize=16, fontweight='bold')
        plt.xlabel('День недели')
        plt.ylabel('Выручка, руб.')
        plt.xticks(range(len(weekday_sales)), days[:len(weekday_sales)])
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()

    # Анализ по типу клиента (если есть столбец)
    if 'Тип клиента' in df.columns:
        plot_client_type_analysis(df)

    # Анализ по отраслям (если есть столбец)
    if 'Отрасль' in df.columns:
        plot_industry_analysis(df)


def plot_all_analysis(df):
    """Построение всех графиков анализа"""
    print("📈 Запуск полного анализа данных...")

    setup_visuals()

    # Основные графики
    print("\n" + "=" * 50)
    print("ВЫРУЧКА ПО КАТЕГОРИЯМ")
    print("=" * 50)
    plot_revenue_by_category(df)

    print("\n" + "=" * 50)
    print("КОЛИЧЕСТВО ПРОДАЖ ПО КАТЕГОРИЯМ")
    print("=" * 50)
    plot_quantity_by_category(df)

    print("\n" + "=" * 50)
    print("СРЕДНИЙ ЧЕК ПО РЕГИОНАМ")
    print("=" * 50)
    plot_avg_check_by_region(df)

    print("\n" + "=" * 50)
    print("ЧАСТОТА ПРОДАЖ ПО ПРОДУКТАМ")
    print("=" * 50)
    plot_sales_frequency_by_product(df)

    # Дополнительные графики (включая анализ по типу клиента и отраслям)
    print("\n" + "=" * 50)
    print("ДОПОЛНИТЕЛЬНЫЙ АНАЛИЗ")
    print("=" * 50)
    plot_additional_analysis(df)

    # Тренд выручки
    print("\n" + "=" * 50)
    print("ТРЕНД ВЫРУЧКИ")
    print("=" * 50)
    plot_monthly_revenue_trend(df)