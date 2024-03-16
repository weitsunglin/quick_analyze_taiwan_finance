import requests
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO
from datetime import datetime, timedelta

# 定义开始和结束日期
start_date = datetime(2024, 3, 1)
end_date = datetime(2024, 3, 31)

# 准备存储每天的收盘价数据
dates = []
closing_prices = []

# 循环获取一个月内每天的数据
current_date = start_date
while current_date <= end_date:
    # 格式化日期
    date_str = current_date.strftime("%Y%m%d")
    
    # 构建URL
    url = f"https://www.twse.com.tw/exchangeReport/MI_INDEX?response=csv&date={date_str}&type=1216"
    
    # 发送GET请求
    response = requests.get(url)
    
    # 检查请求是否成功
    if response.status_code == 200:
        # 将响应的CSV文本转换为DataFrame
        data = pd.read_csv(StringIO(response.text), header=1)
        
        # 检查DataFrame是否包含收盘价列
        if '收盤價' in data.columns:
            # 提取当天的收盘价并存储
            closing_price = data['收盤價'][0]
            dates.append(current_date)
            closing_prices.append(closing_price)
    
    # 移动到下一天
    current_date += timedelta(days=1)

# 转换为DataFrame
df = pd.DataFrame({'Date': dates, 'ClosingPrice': closing_prices})

# 绘制走势图
plt.figure(figsize=(10, 6))
plt.plot(df['Date'], df['ClosingPrice'], marker='o', linestyle='-', color='b')
plt.title('Closing Prices in March 2024')
plt.xlabel('Date')
plt.ylabel('Closing Price')
plt.xticks(rotation=45)
plt.tight_layout()

# 保存图表到本地路径
save_path = 'C:/Users/User/Desktop/project/quick_analyze_stock/closing_prices_march_2024.png'
plt.savefig(save_path)

plt.show()
