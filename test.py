import requests
import pandas as pd
import matplotlib.pyplot as plt

# 定義URL
url = 'https://openapi.taifex.com.tw/v1/DailyForeignExchangeRates'

# 發送GET請求
response = requests.get(url, verify=False)

# 確認請求成功
if response.status_code == 200:
    # 將JSON響應轉換為Python列表
    data = response.json()
    
    # 轉換數據為DataFrame
    df = pd.DataFrame(data)
    
    # 確保日期格式正確，並將其設置為索引
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    df.set_index('Date', inplace=True)
    
    # 將匯率數據轉換為浮點數
    df = df.astype(float)
    
    # 繪製走勢圖
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['USD/NTD'], label='USD/NTD')
    plt.plot(df.index, df['RMB/NTD'], label='RMB/NTD')
    plt.title('Daily Foreign Exchange Rates')
    plt.xlabel('Date')
    plt.ylabel('Rate')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 顯示圖表
    plt.show()
else:
    print("Failed to retrieve data, status code:", response.status_code)
