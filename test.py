import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from io import StringIO

# 初始化一个空的DataFrame来存储每天的数据
df_monthly = pd.DataFrame()

# 股票代码和开始日期
stock_no = '2330'
start_date = datetime(2021, 5, 1)
end_date = datetime(2021, 5, 31)

# 循环获取一个月内每天的数据
current_date = start_date
while current_date <= end_date:
    date_str = current_date.strftime('%Y%m%d')
    url = f"http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date={date_str}&stockNo={stock_no}"
    
    response = requests.get(url)
    if response.status_code == 200:
        # 读取CSV数据到DataFrame
        data = pd.read_csv(StringIO(response.text), header=1, skipfooter=5, engine='python')
        if not data.empty:
            df_monthly = pd.concat([df_monthly, data], ignore_index=True)
    
    current_date += timedelta(days=1)

# 预处理和清洗数据
df_monthly = df_monthly.dropna()
df_monthly['日期'] = pd.to_datetime(df_monthly['日期'].str.replace('年', '-', regex=False).str.replace('月', '-', regex=False).str.replace('日', '', regex=False), format='%Y-%m-%d')
df_monthly['收盤價'] = pd.to_numeric(df_monthly['收盤價'].str.replace(',', '', regex=False), errors='coerce')

# 绘制收盘价走势图
plt.figure(figsize=(10, 6))
plt.plot(df_monthly['日期'], df_monthly['收盤價'], marker='o', linestyle='-')
plt.title(f'Stock No. {stock_no} Closing Price in May 2021')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.grid(True)
plt.xticks(rotation=45)

# 保存走势图到本地
save_path = f'C:\\Users\\User\\Desktop\\project\\quick_analyze_stock\\{stock_no}_closing_price_may_2021.png'
plt.savefig(save_path)
plt.close()

print(f"Chart has been saved to {save_path}")
