import data_download as dd
import data_plotting as dplt
import logging

logger = logging.getLogger('Logger')
formatting = '[%(asctime)s] [%(levelname)s]: %(message)s'
logging.basicConfig(level=logging.INFO, format=formatting)
success_log = 'success.log'  # INFO
warning_log = 'warning.log'  # WARNING
error_log = 'error.log'  # ERROR


def log_write_to_file(file_name: str, message: str):
    '''запись в файл лога'''
    with open(file_name, 'a', encoding='utf8') as file:
        file.write(message + '\n')


def main():
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print(
        "Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print(
        "Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc):»")
    if not ticker:
        logging.error(f'Не выбран тикер')
        log_write_to_file(error_log, message=f'Не выбран тикер')

    period = input("Введите период для данных (например, '1mo' для одного месяца) "
                   "или нажмите enter и введите даты начала и конца периода : ")
    start_period = None
    end_period = None
    if not period:
        start_period = input('Начало периода (ГГГГ-ММ-ДД): ')
        end_period = input('Конец периода  (ГГГГ-ММ-ДД): ')

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period, start=start_period, end=end_period)

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Add average closing price
    print(dd.calculate_and_display_average_price(stock_data, period))

    # Notifications if fluctuations exceed the set threshold
    dd.notify_if_strong_fluctuations(stock_data, ticker, period)

    # Calculation RSI, MACD
    dd.calc_rsi(stock_data)
    dd.calc_macd(stock_data)

    # Plot the data
    dplt.create_and_save_plot(stock_data, ticker, period)

    # Export data to csv
    filename = f'Shares_{ticker}_Period_{period}_{start_period}-{end_period}_stock_data.csv'
    dd.export_data_to_csv(stock_data, filename)


if __name__ == "__main__":
    main()
