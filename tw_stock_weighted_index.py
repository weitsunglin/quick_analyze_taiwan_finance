import requests
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from bs4 import BeautifulSoup

def fetch_twii_history():
    url = 'https://hk.finance.yahoo.com/quote/%5ETWII/history/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        table = soup.find('table', {'data-test': 'historical-prices'})
        if table:
            dates = []
            close_prices = []
            rows = table.find_all('tr', {'class': 'BdT Bdc($seperatorColor) Ta(end) Fz(s) Whs(nw)'})
            for row in rows:
                data = row.find_all('span')
                if len(data) == 7:
                    date = data[0].text
                    close_price = data[4].text
                    dates.append(date)
                    close_prices.append(float(close_price.replace(',', '')))
            return dates[::-1], close_prices[::-1]  # 反轉列表以獲得正確的趨勢圖順序
        else:
            print("Table not found on the page.")
            return None, None
    else:
        print("Failed to fetch data from the URL.")
        return None, None

def plot_close_price_trend(dates, close_prices):
    plt.figure(figsize=(10, 6))
    plt.plot(dates, close_prices, label='Close Price', marker='o', color='b')
    plt.title('台灣加權股價指數收盤價趨勢圖', fontproperties=font_properties)
    plt.xlabel('日期', fontproperties=font_properties)
    plt.ylabel('收盤價', fontproperties=font_properties)
    plt.xticks([])  # 不顯示 x 軸刻度
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # 顯示第一個和最後一個點的日期
    plt.text(dates[0], close_prices[0], dates[0], fontsize=10, ha='right', va='bottom', fontproperties=font_properties)
    plt.text(dates[-1], close_prices[-1], dates[-1], fontsize=10, ha='right', va='bottom', fontproperties=font_properties)

    plt.savefig(f'C:\\Users\\User\\Desktop\\project\\quick_analyze_taiwan_finance\\tw_stock_weighted_index.png')

if __name__ == "__main__":
    font_path = "C:\\Windows\\Fonts\\msjh.ttc"
    font_properties = FontProperties(fname=font_path, size=12)
    
    dates, close_prices = fetch_twii_history()
    if dates and close_prices:
        plot_close_price_trend(dates, close_prices)