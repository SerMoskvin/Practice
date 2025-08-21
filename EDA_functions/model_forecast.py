import matplotlib.pyplot as plt
import pandas as pd
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import warnings

warnings.filterwarnings('ignore')

# Импортируем наши функции и конфиг
from config import PROPHET_CONFIG
from read_and_clean import load_data, clean_data, prepare_for_prophet
from analyze import plot_all_analysis


def create_prophet_model(df_prophet, config=PROPHET_CONFIG):
    """
    Создает и обучает модель Prophet на основе конфигурации.
    """

    if df_prophet is None:
        print("❌ Нет данных для обучения модели")
        return None, None

    model_params = config.get("model_params", {}).copy()  # Делаем копию, чтобы не менять оригинал
    forecast_params = config.get("forecast_params", {})

    # 1. Инициализация модели с параметрами из конфига
    model = Prophet(**model_params)

    # 2. Добавляем праздники страны, если указано в конфиге
    country_holidays = config.get("country_holidays")
    if country_holidays:
        try:
            model.add_country_holidays(country_name=country_holidays)
            print(f"✅ Добавлены праздники страны: {country_holidays}")
        except Exception as e:
            print(f"⚠️ Не удалось добавить праздники: {e}")

    # 3. Добавляем КАСТОМНЫЕ праздники/события
    custom_holidays = config.get("custom_holidays", [])
    if custom_holidays:
        try:
            for holiday_df in custom_holidays:
                model = model.add_seasonality(
                    name=holiday_df['holiday'].iloc[0],
                    period=365,  # Условно годовой период
                    fourier_order=5  # Сложность паттерна
                )
            # Альтернативный подход: добавляем как holidays
            # all_custom_holidays = pd.concat(custom_holidays, ignore_index=True)
            # model = model.add_country_holidays(country_name=None, holidays=all_custom_holidays)
            print(f"✅ Добавлены кастомные события: {[df['holiday'].iloc[0] for df in custom_holidays]}")
        except Exception as e:
            print(f"⚠️ Не удалось добавить кастомные события: {e}")

    # 4. Обучение модели
    print("🔄 Обучаю модель Prophet...")
    model.fit(df_prophet)

    # 5. Создание датафрейма для будущего
    periods = forecast_params.get("periods", 30)
    freq = forecast_params.get("freq", 'D')

    future = model.make_future_dataframe(periods=periods, freq=freq)

    # 6. Построение прогноза
    print("🔮 Строю прогноз...")
    forecast = model.predict(future)

    return model, forecast


def plot_prophet_forecast(model, forecast, df_prophet=None):
    """Визуализация результатов прогноза Prophet"""
    if model is None or forecast is None:
        return

    # График 1: Основной прогноз
    fig, ax = plt.subplots(figsize=(15, 8))
    model.plot(forecast, ax=ax)

    # Добавляем фактические точки для наглядности
    if df_prophet is not None:
        ax.plot(df_prophet['ds'], df_prophet['y'], '.', color='black',
                alpha=0.3, markersize=2, label='Факт (daily)')
        ax.legend()

    plt.title('Прогноз продаж: исторические данные + прогноз', fontsize=16, fontweight='bold')
    plt.xlabel('Дата')
    plt.ylabel('Выручка')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.show()

    # График 2: Компоненты прогноза
    fig2 = model.plot_components(forecast)
    plt.suptitle('Компоненты прогноза: тренд и сезонность', fontsize=16, fontweight='bold')
    plt.tight_layout()
    plt.show()

    # Выводим статистику прогноза
    print("\n" + "=" * 50)
    print("СТАТИСТИКА ПРОГНОЗА")
    print("=" * 50)

    # Последние 5 дней прогноза
    print("📋 Последние 5 дней прогноза:")
    forecast_display = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail().copy()
    forecast_display['ds'] = forecast_display['ds'].dt.strftime('%Y-%m-%d')
    forecast_display['yhat'] = forecast_display['yhat'].round().astype(int)
    forecast_display['yhat_lower'] = forecast_display['yhat_lower'].round().astype(int)
    forecast_display['yhat_upper'] = forecast_display['yhat_upper'].round().astype(int)
    print(forecast_display.to_string(index=False))

    # Суммарный прогноз на весь период
    future_forecast = forecast[forecast['ds'] > df_prophet['ds'].max()].copy()
    total_forecast = future_forecast['yhat'].sum()
    print(f"\n💰 Суммарный прогноз на {len(future_forecast)} дней: {total_forecast:,.0f} руб.")

def run_full_analysis():
    """
    Запускает полный анализ: EDA + прогнозирование
    Возвращает: model, forecast, df_clean, mape
    """
    print("🚀 Запуск полного пайплайна анализа и прогнозирования")
    print("=" * 60)

    # 1. Загрузка и очистка данных
    df = load_data()
    if df is None:
        return None, None, None, None

    df_clean = clean_data(df)
    if df_clean is None:
        return None, None, None, None

    # 2. Исследовательский анализ (EDA)
    print("\n" + "=" * 60)
    print("ЭТАП 1: ИССЛЕДОВАТЕЛЬСКИЙ АНАЛИЗ ДАННЫХ (EDA)")
    print("=" * 60)
    plot_all_analysis(df_clean)

    # 3. Подготовка данных для прогнозирования
    print("\n" + "=" * 60)
    print("ЭТАП 2: ПОДГОТОВКА К ПРОГНОЗИРОВАНИЮ")
    print("=" * 60)
    df_prophet = prepare_for_prophet(df_clean)

    if df_prophet is None or len(df_prophet) < 100:
        print("❌ Недостаточно данных для построения прогноза")
        print(f"   Требуется: минимум 100 дней, available: {len(df_prophet)}")
        return None, None, df_clean, None

    # 4. Построение и оценка модели
    print("\n" + "=" * 60)
    print("ЭТАП 3: ПОСТРОЕНИЕ И ОЦЕНКА МОДЕЛИ PROPHET")
    print("=" * 60)
    model, forecast = create_prophet_model(df_prophet)

    if model and forecast is not None:
        # Визуализация результатов
        plot_prophet_forecast(model, forecast, df_prophet)

        # Оценка качества (mape - Mean Absolute Percentage Error)
        mape = evaluate_prophet_model(model, forecast, df_prophet)

        print("\n✅ Прогнозирование завершено успешно!")

        # Дополнительно: интерактивные графики
        try:
            import plotly.offline as py
            print("\n🌐 Генерация интерактивных графиков...")
            fig_plotly = plot_plotly(model, forecast)
            fig_components = plot_components_plotly(model, forecast)

            # Сохранение в HTML файлы
            py.plot(fig_plotly, filename='prophet_forecast.html', auto_open=False)
            py.plot(fig_components, filename='prophet_components.html', auto_open=False)
            print("💾 Интерактивные графики сохранены как 'prophet_forecast.html' и 'prophet_components.html'")

        except ImportError:
            py = None
            print("ℹ️  Для интерактивных графиков установите plotly: `pip install plotly`")

        return model, forecast, df_clean, mape

    return None, None, df_clean, None


def run_only_forecast():
    """
    Запускает только прогнозирование без EDA
    Полезно, когда EDA уже был выполнен
    """
    print("🚀 Запуск только прогнозирования")

    df = load_data()
    if df is None:
        return None, None, None

    df_clean = clean_data(df)
    if df_clean is None:
        return None, None, None

    df_prophet = prepare_for_prophet(df_clean)

    if df_prophet is None or len(df_prophet) < 100:
        print("❌ Недостаточно данных для построения прогноза")
        return None, None, None

    model, forecast = create_prophet_model(df_prophet)

    if model and forecast is not None:
        plot_prophet_forecast(model, forecast, df_prophet)
        mape = evaluate_prophet_model(model, forecast, df_prophet)
        return model, forecast, mape

    return None, None, None


def forecast_by_category(df_clean, config=PROPHET_CONFIG):
    """
    Прогноз продаж по отдельным категориям товаров
    Строит отдельную модель Prophet для каждой категории
    """
    if 'Категория' not in df_clean.columns:
        print("❌ Отсутствует столбец 'Категория'")
        return {}

    categories = df_clean['Категория'].unique()
    print(f"📊 Прогнозирование для {len(categories)} категорий")

    results = {}

    for category in categories:
        print(f"\n🔍 Анализируем категорию: {category}")

        # Фильтруем данные по категории
        df_category = df_clean[df_clean['Категория'] == category]

        # Подготавливаем данные для Prophet
        df_prophet = prepare_for_prophet(df_category)

        # Проверяем, достаточно ли данных для прогноза
        if df_prophet is not None and len(df_prophet) > 30:
            try:
                # Создаем и обучаем модель для категории
                model, forecast = create_prophet_model(df_prophet, config)

                if model and forecast is not None:
                    # Оцениваем качество прогноза
                    mape = evaluate_prophet_model(model, forecast, df_prophet)

                    # Сохраняем результаты
                    results[category] = {
                        'model': model,
                        'forecast': forecast,
                        'last_actual_value': df_prophet['y'].iloc[-1] if len(df_prophet) > 0 else 0,
                        'data_points': len(df_prophet),
                        'mape': mape,
                        'df_prophet': df_prophet
                    }

                    # Визуализируем прогноз для категории
                    plt.figure(figsize=(12, 6))
                    model.plot(forecast)
                    plt.title(f'Прогноз продаж для категории: {category}\nMAPE: {mape:.1f}%',
                              fontsize=14, fontweight='bold')
                    plt.xlabel('Дата')
                    plt.ylabel('Выручка, руб.')
                    plt.grid(True, alpha=0.3)
                    plt.tight_layout()
                    plt.show()

                    print(f"✅ Прогноз для '{category}' готов ({len(df_prophet)} точек данных, MAPE: {mape:.1f}%)")

            except Exception as e:
                print(f"❌ Ошибка при прогнозировании категории '{category}': {e}")
        else:
            data_points = len(df_prophet) if df_prophet is not None else 0
            print(f"⚠️ Недостаточно данных для категории '{category}': {data_points} точек (требуется > 30)")

    return results


def analyze_category_forecasts(results):
    """
    Анализ и сравнение прогнозов по категориям
    """
    if not results:
        print("❌ Нет результатов для анализа")
        return None

    print("\n" + "=" * 60)
    print("📈 СРАВНИТЕЛЬНЫЙ АНАЛИЗ ПРОГНОЗОВ ПО КАТЕГОРИЯМ")
    print("=" * 60)

    # Создаем DataFrame для анализа
    analysis_data = []

    for category, data in results.items():
        forecast = data['forecast']

        # Берем прогноз на будущий период (последние 30 дней прогноза)
        last_training_date = data['df_prophet']['ds'].max()
        future_forecast = forecast[forecast['ds'] > last_training_date]

        if len(future_forecast) > 0:
            total_forecast = future_forecast['yhat'].sum()
            avg_daily_forecast = future_forecast['yhat'].mean()

            analysis_data.append({
                'Категория': category,
                'Исторических_точек': data['data_points'],
                'Последнее_факт_значение': data['last_actual_value'],
                'Суммарный_прогноз': total_forecast,
                'Средний_дневной_прогноз': avg_daily_forecast,
                'Рост_к_факту_%': ((avg_daily_forecast / data['last_actual_value']) - 1) * 100 if data[
                                                                                                      'last_actual_value'] > 0 else 0,
                'Точность_MAPE_%': data.get('mape', 0)
            })

    if not analysis_data:
        print("❌ Нет данных для анализа прогнозов")
        return None

    # Создаем DataFrame
    df_analysis = pd.DataFrame(analysis_data)

    # Сортируем по суммарному прогнозу
    df_analysis = df_analysis.sort_values('Суммарный_прогноз', ascending=False)

    # Выводим таблицу
    print("📊 Сравнительная таблица прогнозов:")
    display_df = df_analysis.copy()

    # Форматирование чисел
    display_df['Суммарный_прогноз'] = display_df['Суммарный_прогноз'].apply(lambda x: f"{x:,.0f}")
    display_df['Средний_дневной_прогноз'] = display_df['Средний_дневной_прогноз'].apply(lambda x: f"{x:,.0f}")
    display_df['Последнее_факт_значение'] = display_df['Последнее_факт_значение'].apply(lambda x: f"{x:,.0f}")
    display_df['Рост_к_факту_%'] = display_df['Рост_к_факту_%'].apply(lambda x: f"{x:+.1f}%")
    display_df['Точность_MAPE_%'] = display_df['Точность_MAPE_%'].apply(lambda x: f"{x:.1f}%")

    print(display_df.to_string(index=False))

    # Визуализация
    plt.figure(figsize=(14, 10))

    # График 1: Суммарный прогноз
    plt.subplot(2, 1, 1)
    bars = plt.bar(range(len(df_analysis)), df_analysis['Суммарный_прогноз'].astype(float))
    plt.title('Суммарный прогноз по категориям', fontsize=16, fontweight='bold')
    plt.xlabel('Категория')
    plt.ylabel('Прогноз выручки, руб.')
    plt.xticks(range(len(df_analysis)), df_analysis['Категория'], rotation=45, ha='right')

    for bar, value in zip(bars, df_analysis['Суммарный_прогноз'].astype(float)):
        plt.text(bar.get_x() + bar.get_width() / 2.,
                 bar.get_height() + max(df_analysis['Суммарный_прогноз'].astype(float)) * 0.01,
                 f'{value:,.0f}', ha='center', va='bottom', fontsize=10)

    plt.grid(axis='y', alpha=0.3)

    # График 2: Точность прогнозов
    plt.subplot(2, 1, 2)
    colors = ['green' if x <= 20 else 'orange' if x <= 50 else 'red' for x in df_analysis['Точность_MAPE_%']]
    bars = plt.bar(range(len(df_analysis)), df_analysis['Точность_MAPE_%'], color=colors)
    plt.title('Точность прогнозов (MAPE)', fontsize=16, fontweight='bold')
    plt.xlabel('Категория')
    plt.ylabel('Ошибка прогноза, %')
    plt.xticks(range(len(df_analysis)), df_analysis['Категория'], rotation=45, ha='right')
    plt.axhline(y=20, color='red', linestyle='--', alpha=0.7, label='Порог точности (20%)')

    for bar, value in zip(bars, df_analysis['Точность_MAPE_%']):
        plt.text(bar.get_x() + bar.get_width() / 2., bar.get_height() + 1,
                 f'{value:.1f}%', ha='center', va='bottom', fontsize=10)

    plt.legend()
    plt.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    plt.show()

    # Вывод рекомендаций
    print("\n💡 РЕКОМЕНДАЦИИ:")
    best_category = df_analysis.iloc[0]['Категория']
    worst_accuracy = df_analysis[df_analysis['Точность_MAPE_%'] == df_analysis['Точность_MAPE_%'].max()].iloc[0]

    print(f"• Наибольший потенциал роста: {best_category}")
    print(f"• Наименее точный прогноз: {worst_accuracy['Категория']} ({worst_accuracy['Точность_MAPE_%']:.1f}% ошибки)")

    # Проверяем точность прогнозов
    accurate_forecasts = df_analysis[df_analysis['Точность_MAPE_%'] <= 20]
    if len(accurate_forecasts) > 0:
        print(f"• Надежные прогнозы (MAPE ≤ 20%): {', '.join(accurate_forecasts['Категория'].tolist())}")

    return df_analysis


def evaluate_prophet_model(model, forecast, df_prophet):
    """
    Оценка качества модели Prophet на исторических данных.
    Возвращает MAPE (Mean Absolute Percentage Error)
    """
    try:
        # Соединяем фактические данные с прогнозом
        df_eval = df_prophet.merge(forecast[['ds', 'yhat']], on='ds', how='inner')

        # Вычисляем ошибки
        df_eval['error'] = df_eval['y'] - df_eval['yhat']
        df_eval['ape'] = (abs(df_eval['error']) / df_eval['y']) * 100

        # Убираем бесконечные значения и деление на ноль
        df_eval = df_eval[(df_eval['y'] > 0) & (df_eval['ape'] < float('inf'))]

        if len(df_eval) > 0:
            mape = df_eval['ape'].mean()
            return mape
        else:
            return float('nan')

    except Exception as e:
        print(f"⚠️ Ошибка при оценке модели: {e}")
        return float('nan')