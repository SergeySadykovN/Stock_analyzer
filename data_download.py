import yfinance as yf


def fetch_stock_data(ticker, period='1mo'):
    stock = yf.Ticker(ticker)
    data = stock.history(period=period)
    return data


def add_moving_average(data, window_size=5):
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    '''вычисляет и выводит среднюю цену закрытия акций
    за заданный период.
    '''
    average_period = data['Close'].mean()
    return print(f'Average closing price of shares for a given period: {average_period}')
