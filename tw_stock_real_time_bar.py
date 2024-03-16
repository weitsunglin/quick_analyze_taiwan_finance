import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import os
from matplotlib.font_manager import FontProperties

def scrape_stock_price(stock_code):
    url = f'https://www.cnyes.com/twstock/{stock_code}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        stock_price = soup.find('h3', class_='jsx-2312976322 rise')
        if not stock_price:
            stock_price = soup.find('h3', class_='jsx-2312976322 fall')

        if not stock_price:
            stock_price = soup.find('h3', class_='jsx-2312976322')

        if stock_price:
            price_text = stock_price.text.split()[0].replace(',', '')
            try:
                price = float(price_text)
                return stock_code, price
            except ValueError:
                return stock_code, None
        else:
            return stock_code, None
    else:
        return stock_code, None

original_stock_codes = ['3293', '2376', '2454', '2330', '2308']
scraped_data = [scrape_stock_price(code) for code in original_stock_codes]

# Filter out None prices and separate codes and prices
filtered_data = [(code, price) for code, price in scraped_data if price is not None]
stock_codes, prices = zip(*filtered_data)  # This unpacks the filtered list into two tuples

font = FontProperties(fname=r"c:\windows\fonts\simsun.ttc", size=14)

plt.figure(figsize=(10, 6))

min_price = min(prices) * 0.9
max_price = max(prices) * 1.1


bars = plt.bar(stock_codes, prices, color='blue')
plt.xlabel('股票代號', fontproperties=font)
plt.ylabel('價格 (nt)', fontproperties=font)
plt.title('台灣小海豹嚴選監控中', fontproperties=font)
plt.xticks(rotation=45)
plt.ylim(min_price, max_price)  # 設定y軸範圍

for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval + (max_price - min_price) * 0.01, f'{yval:.2f}', ha='center', va='bottom', fontproperties=font)

directory = "C:/Users/User/Desktop/project/quick_analyze_stock/"
if not os.path.exists(directory):
    os.makedirs(directory)

save_path = os.path.join(directory, "stock_prices.png")
plt.savefig(save_path)
