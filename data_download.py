import pandas as pd
import yfinance as yf


def log_write_to_file(file_name: str, message: str):
    '''запись в файл лога'''
    with open(file_name, 'a') as file:
        file.write(message + '\n')


def fetch_stock_data(ticker: str, period='1mo', start: [str] = None, end: [str] = None):
    ''' Загрузка исторических данных об акциях за период.
    по умолчанию период 1 месяц
    :param ticker: str
    :param period: str
    :param start: str
    :param end: str
    :return : pd.DataFrame
    '''
    stock = yf.Ticker(ticker)
    if start is not None:
        data = stock.history(period=period, start=start, end=end)
    else:
        data = stock.history(period=period)
    return data


def add_moving_average(data: pd.DataFrame, window_size=5):
    '''Расчет скользящего среднего цены закрытия акций '''
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data: pd.DataFrame, period: str):
    '''Вычисляет и выводит среднюю цену закрытия акций
    за заданный период.
    '''
    average_price = data['Close'].mean()
    return (f'\nСредняя цена закрытия акций {average_price}\n'
            f'за период: {period}')


def notify_if_strong_fluctuations(data: pd.DataFrame, ticker: str, period: str, threshold=10):
    '''
    Анализирует данные и уведомляет пользователя,
    если цена акций колебалась более чем на заданный процент за период.
     Функция будет вычислять максимальное и минимальное значения цены закрытия и сравнивать разницу с заданным порогом.
     Если разница превышает порог (по умолчанию threshold = 10), пользователь получает уведомление
    :param data: DataFrame from fetch_stock_data
    :param ticker: str name of shares
    :param period: str period from fetch_stock_data
    :param threshold: int
    :return: print fluctuation with ticker and period
    '''

    max_price = data['Close'].max()  # макс цена закрытия
    min_price = data['Close'].min()  # мин цена закрытия

    # вычисляем колебания  с округлением до десятых
    fluctuation = round((((max_price - min_price) / min_price) * 100), 1)

    if fluctuation > threshold:
        print(f'\nНаблюдаются сильные колебания: {fluctuation} \n'
              f'в цена закрытия акций: {ticker} \n'
              f'за указанный период: {period} ')


def export_data_to_csv(data: pd.DataFrame, filename: str):
    '''
    Экспорт данных в CSV формате
    :param data: df: pd.DataFrame
    :param filename: str
    :return: *.csv
    '''
    data.to_csv(filename)
    # log_write_to_file(success_log, str(filename))
    print(f'\nДанные сохраняются в {filename}')


def calc_rsi(data: pd.DataFrame):
    ''' Функция рачета RSI
    :param data: pd.DataFrame
    :return: data
    '''
    delta = data['Close'].diff()  # Изменение цены
    up_ema = delta.clip(lower=0).rolling(window=14).mean()  # прирост цены (wimdow=14 recomend)
    down_ema = -1 * delta.clip(upper=0).rolling(window=14).mean()  # падение цены (wimdow=14 recomend)
    rsi = 100 - (100 / (1 + (up_ema / down_ema)))  # расчет RSI
    data['RSI'] = rsi  # добавляем RSI  в DataFrame
    return data

    # print(data['RSI'].values)


def calc_macd(data: pd.DataFrame):
    '''Функция расчета MACD
    :param data: pd..DataFrame
    :return: data
    '''
    short_ema = data['Close'].ewm(span=12).mean()
    long_ema = data['Close'].ewm(span=30).mean()
    data['MACD'] = short_ema - long_ema
    data['Value'] = data['MACD'].ewm(span=10).mean()
    return data
    # print(data)


def calc_deviation(data: pd.DataFrame):
    ''' Функция расчета стандартного отклонения
    :param data: pd..DataFrame
    :return: data
    '''
    st_deviation = data['Close'].std(ddof=1)
    print(f'Стандартное отклонение цены закрытия {st_deviation}')
