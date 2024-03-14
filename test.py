import pandas as pd
import requests
from io import StringIO
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

# 函式：將民國年轉換為西元年
def roc_to_ad(date_str):
    year, month, day = map(int, date_str.split('/'))
    return f"{year + 1911}/{month:02d}/{day:02d}"

# 創建日期列表
dates = [(datetime.today() - timedelta(days=x)).strftime('%Y/%m/%d') for x in range(30)]

# URL前半部分
base_url = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d='

# 指定個股代號
specific_stock = '3293'

# 存儲日期和收盤價
close_prices = []
valid_dates = []

# 迴圈遍歷日期列表，爬取每一天的股價資訊
for date in dates:
    # 轉換日期格式至網址所需的民國年格式
    roc_date = roc_to_ad(date).split('/')
    roc_date_str = f"{int(roc_date[0]) - 1911}/{roc_date[1]}/{roc_date[2]}"
    
    # 完整URL
    url = f"{base_url}{roc_date_str}&s=0,asc,0"
    
    try:
        r = requests.get(url)
        if r.ok:
            lines = r.text.replace('\r', '').split('\n')
            df = pd.read_csv(StringIO("\n".join(lines[3:])), header=None)
            df.columns = list(map(lambda l: l.replace(' ',''), lines[2].split(',')))
            df['代號'] = df['代號'].astype(str)
            specific_df = df[df['代號'] == specific_stock]
            if not specific_df.empty and '收盤' in specific_df.columns:
                close_prices.append(specific_df.iloc[0]['收盤'])
                valid_dates.append(date)
            else:
                print(f"No data for stock {specific_stock} on {date}")
        else:
            print(f"Failed to fetch data for {date}")
    except Exception as e:
        print(f"An error occurred while processing {date}: {e}")

# 轉換收盤價為數字
close_prices = [float(price) for price in close_prices]

# 繪製曲線圖
plt.figure(figsize=(10, 6))
plt.plot(valid_dates, close_prices, marker='o', linestyle='-', color='b')
plt.title(f'Closing Prices of Stock {specific_stock} Over the Last 30 Days')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
