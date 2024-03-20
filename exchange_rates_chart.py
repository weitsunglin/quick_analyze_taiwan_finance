import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

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

    # 繁中
    font_path = "C:\\Windows\\Fonts\\msjh.ttc"
    font_properties = FontProperties(fname=font_path, size=12)
    
    # 確保日期格式正確，並將其設置為索引
    df['Date'] = pd.to_datetime(df['Date'], format='%Y%m%d')
    df.set_index('Date', inplace=True)
    
    # 將匯率數據轉換為浮點數
    df = df.astype(float)
    
    # 繪製走勢圖
    plt.figure(figsize=(10, 6))
    plt.plot(df.index, df['USD/NTD'], label='USD/NTD')
    plt.plot(df.index, df['RMB/NTD'], label='RMB/NTD')
    plt.title('台幣每日匯率走勢', fontproperties=font_properties)
    plt.xlabel('日期', fontproperties=font_properties)
    plt.ylabel('匯率', fontproperties=font_properties)
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # 顯示圖表
    plt.savefig(f'C:\\Users\\User\\Desktop\\project\\quick_analyze_taiwan_finance\\exchange_rates_chart.png')
else:
    print("Failed to retrieve data, status code:", response.status_code)
