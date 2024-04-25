import yfinance as yf


def fetch_stock_data(ticker, period='1mo'):
    ''' Загрузка исторических данных об акциях за период.
    по умолчанию период 1 месяц'''
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    '''Расчет скользящего среднего цены закрытия акций '''
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    '''Вычисляет и выводит среднюю цену закрытия акций
    за заданный период.
    '''
    average_price = data['Close'].mean()
    return f'Average closing price of shares for a given period: {average_price}'


def notify_if_strong_fluctuations(data, ticker, period, threshold=10):
    '''
    Анализирует данные и уведомляет пользователя,
    если цена акций колебалась более чем на заданный процент за период.
     Функция будет вычислять максимальное и минимальное значения цены закрытия и сравнивать разницу с заданным порогом.
     Если разница превышает порог (по умолчанию threshold = 10), пользователь получает уведомление
    :param data: data from fetch_stock_data
    :param ticker: name of shares
    :param period: period from fetch_stock_data
    :param threshold: int
    :return: print fluctuation with ticker and period
    '''

    max_price = data['Close'].max()  # макс цена закрытия
    min_price = data['Close'].min()  # мин цена закрытия

    # вычисляем колебания  с округлением до десятых
    fluctuation = round((((max_price - min_price) / min_price) * 100), 1)

    if fluctuation > threshold:
        print(f'There is a strong fluctuation: {fluctuation} \n'
              f'in the closing price of the shares: {ticker} \n'
              f'during the mentioned period: {period} ')

