import matplotlib.pyplot as plt
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


def evaluate_prophet_model(model, forecast, df_prophet):
    """
    Простая оценка качества модели на исторических данных.
    Расчет MAPE (Mean Absolute Percentage Error)
    """
    # Соединяем факт и прогноз
    df_eval = df_prophet.merge(forecast[['ds', 'yhat']], on='ds', how='inner')

    # Вычисляем ошибку
    df_eval['error'] = df_eval['y'] - df_eval['yhat']
    df_eval['ape'] = (abs(df_eval['error']) / df_eval['y']) * 100

    # Усредняем ошибку (исключаем деление на 0 и бесконечные значения)
    df_eval = df_eval[df_eval['y'] > 0]
    mape = df_eval['ape'].mean()

    print(f"📊 Ошибка прогноза на исторических данных (MAPE): {mape:.2f}%")
    print("💡 Интерпретация MAPE:")
    print("   <10% - Отличная точность")
    print("   10%-20% - Хорошая точность")
    print("   20%-50% - Приемлемая точность")
    print("   >50% - Неточный прогноз")

    return mape


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
