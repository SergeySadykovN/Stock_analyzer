import matplotlib.pyplot as plt
import pandas as pd
import log

# Установка Plotly как бэкенда для графиков в pandas
pd.options.plotting.backend = "plotly"


def create_and_save_plot(data: pd.DataFrame, ticker: str, period: str, style_choice: str = None,
                         filename: str = None, ):
    # применяем стиль к графику, по умолчанию стандартный
    if style_choice:
        plt.figure(figsize=(10, 6))
        plt.style.use(style_choice)
    else:
        plt.style.use('classic')

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            plt.plot(dates, data['Close'].values, label='Close Price')
            plt.plot(dates, data['Moving_Average'].values, label='Moving Average')
            plt.plot(dates, data['RSI'].values, label='RSI')
            plt.plot(dates, data['MACD'].values, label='MACD')
        else:
            log.warning_log("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        plt.plot(data['Date'], data['Close'], label='Close Price')
        plt.plot(data['Date'], data['Moving_Average'], label='Moving Average')
        plt.plot(data, data['RSI'].values, label='RSI')
        plt.plot(data, data['MACD'].values, label='MACD')

    plt.title(f"{ticker} Цена акций с течением времени")
    plt.xlabel("Дата")
    plt.ylabel("Цена")
    plt.legend()

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.savefig(filename)
    print(f"График сохранен как {filename}")


def view_plotly(data: pd.DataFrame):
    graph = data.plot()
    type_view_graph = input("Вид графика (0 = в окне, 1 = интерактивный в браузере): ")
    if type_view_graph == '1':
        graph.show()
    elif type_view_graph == '0':
        plt.show()
    else:
        log.warning_log("Некорректный ввод")
