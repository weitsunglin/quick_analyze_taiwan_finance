
from yahoo_fin.stock_info import *

stock_no = '0050.TW'

data = get_data(stock_no , start_date = '2021/01/01')
data.head()