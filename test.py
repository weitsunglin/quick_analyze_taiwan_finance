import pandas as pd
import requests
from io import StringIO
from datetime import datetime, timedelta

def roc_to_ad(date_str):
    year, month, day = map(int, date_str.split('/'))
    return f"{year + 1911}/{month:02d}/{day:02d}"

dates = [(datetime.today() - timedelta(days=x)).strftime('%Y/%m/%d') for x in range(1, 30)]

base_url = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d='

for date in dates:
    roc_date = roc_to_ad(date).split('/')
    roc_date_str = f"{int(roc_date[0]) - 1911}/{roc_date[1]}/{roc_date[2]}"
    
    url = f"{base_url}{roc_date_str}&s=0,asc,0"
    
    try:
        r = requests.get(url)
        if r.ok:
            lines = r.text.replace('\r', '').split('\n')
            df = pd.read_csv(StringIO("\n".join(lines[3:])), header=None)
            df.columns = list(map(lambda l: l.replace(' ',''), lines[2].split(',')))
            df.index = df['代號']
            df = df.drop(['代號'], axis=1)
            df.to_csv(f'stock_prices_{date.replace("/", "-")}.csv')
        else:
            print(f"Failed to fetch data for {date}")
    except Exception as e:
        print(f"An error occurred while processing {date}: {e}")
