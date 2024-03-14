import yfinance as yf

date = '2021-01-01'
stock_no = '3293.TW'

stock = yf.Ticker(stock_no)
stock_data = stock.history(start=date)

print(stock_data)

stock_data.head()