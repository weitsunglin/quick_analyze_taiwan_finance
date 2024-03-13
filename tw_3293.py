import requests

link = 'http://www.tpex.org.tw/web/stock/aftertrading/daily_close_quotes/stk_quote_download.php?l=zh-tw&d=107/02/09&s=0,asc,0'
r = requests.get(link)
r.ok

lines = r.text.replace('\r', '').split('\n')

import pandas as pd
from io import StringIO
df = pd.read_csv(StringIO("\n".join(lines[3:])), header=None)
df.head()

df.columns = list(map(lambda l: l.replace(' ',''), lines[2].split(',')))
df.index = df['代號']
df = df.drop(['代號'], axis=1)
df.head()

df.to_csv('test.csv')
pd.read_csv('test.csv', index_col='代號').head()