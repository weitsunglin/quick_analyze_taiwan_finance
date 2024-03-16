import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

url = 'https://openapi.twse.com.tw/v1/exchangeReport/STOCK_DAY_ALL'

response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    df = pd.DataFrame(data)
    df['TradeValue'] = pd.to_numeric(df['TradeValue'], errors='coerce')
    top10 = df.sort_values(by='TradeValue', ascending=False).head(10)

    # 设置支持繁体中文的字体
    font_path = "C:\\Windows\\Fonts\\msjh.ttc"  # 字体路径
    font_properties = FontProperties(fname=font_path, size=12)
    plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

    plt.style.use('ggplot')
    ax = top10.plot(kind='bar', x='Name', y='TradeValue', legend=None)
    ax.set_title('Top 10 Stocks by Trade Value', fontproperties=font_properties)
    ax.set_xlabel('Stock Name', fontproperties=font_properties)
    ax.set_ylabel('Trade Value', fontproperties=font_properties)
    ax.set_xticklabels(top10['Name'], fontproperties=font_properties, rotation=45, ha="right")
    
    plt.tight_layout()

    # 保存图表到本地路径
    save_path = 'C:\\Users\\User\\Desktop\\project\\quick_analyze_stock\\top10_stocks_trade_value.png'
    plt.savefig(save_path)
    plt.show()
else:
    print("Failed to retrieve data, status code:", response.status_code)
