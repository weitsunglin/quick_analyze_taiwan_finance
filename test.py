import requests
import pandas as pd

# 定义URL
url = 'https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL'

# 发送GET请求
response = requests.get(url)

# 检查请求是否成功
if response.status_code == 200:
    # 将JSON响应转换为Python列表
    data = response.json()
    
    # 转换数据为DataFrame
    df = pd.DataFrame(data)
    
    # 确保'TradeValue'列是数值类型，以便排序
    df['TradeValue'] = pd.to_numeric(df['TradeValue'], errors='coerce')
    
    # 根据'TradeValue'排序，并取前10名
    top10 = df.sort_values(by='TradeValue', ascending=False).head(20)
    
    # 打印结果
    print(top10)
else:
    print("Failed to retrieve data, status code:", response.status_code)
