import pandas as pd
import requests
from io import StringIO
from datetime import datetime, timedelta

# 函式：將民國年轉換為西元年
def roc_to_ad(date_str):
    year, month, day = map(int, date_str.split('/'))
    return f"{year + 1911}/{month:02d}/{day:02d}"

# 創建日期列表
dates = [(datetime.today() - timedelta(days=x)).strftime('%Y/%m/%d') for x in range(1, 30)]

# URL前半部分
base_url = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d='

# 迴圈遍歷日期列表，爬取和存儲每一天的股價資訊
for date in dates:
    # 轉換日期格式至網址所需的民國年格式
    roc_date = roc_to_ad(date).split('/')
    roc_date_str = f"{int(roc_date[0]) - 1911}/{roc_date[1]}/{roc_date[2]}"
    
    # 完整URL
    url = f"{base_url}{roc_date_str}&s=0,asc,0"
    
    # 發送請求
    r = requests.get(url)
    if r.ok:
        # 處理原始文本數據
        lines = r.text.replace('\r', '').split('\n')
        # 使用pandas讀取和處理數據
        df = pd.read_csv(StringIO("\n".join(lines[3:])), header=None)
        # 設置列名和索引
        df.columns = list(map(lambda l: l.replace(' ',''), lines[2].split(',')))
        df.index = df['代號']
        df = df.drop(['代號'], axis=1)
        # 存儲數據
        df.to_csv(f'stock_prices_{date.replace("/", "-")}.csv')
    else:
        print(f"Failed to fetch data for {date}")
