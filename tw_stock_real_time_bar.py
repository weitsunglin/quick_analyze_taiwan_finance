def scrape_stock_price(stock_code):
    url = f'https://www.cnyes.com/twstock/{stock_code}'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        stock_price = soup.find('h3', class_='jsx-2312976322 rise')
        if not stock_price:
            stock_price = soup.find('h3', class_='jsx-2312976322 fall')
        if stock_price:
            # 假設股票價格是文字中的第一個數字，這可能需要根據實際情況調整
            price_text = stock_price.text.split()[0].replace(',', '')
            try:
                price = float(price_text)
                return stock_code, price
            except ValueError:
                # 如果轉換失敗，可能需要進一步檢查文字格式
                return stock_code, None
        else:
            return stock_code, None
    else:
        return stock_code, None

# 接下來，運行爬蟲並收集價格資料
stock_codes = ['3293', '2376', '2357']
stock_prices = {code: scrape_stock_price(code)[1] for code in stock_codes}


import matplotlib.pyplot as plt

# 確保stock_prices字典已經有值
stock_codes = list(stock_prices.keys())
prices = [price for price in stock_prices.values() if price is not None]

plt.figure(figsize=(10, 6))
plt.bar(stock_codes, prices, color='blue')
plt.xlabel('股票代碼')
plt.ylabel('價格 (nt)')
plt.title('股票價格')
plt.xticks(rotation=45)

# 儲存圖表
save_path = "C:/Users/User/Desktop/project/quick_analyze_stock/stock_prices.png"
plt.savefig(save_path)
