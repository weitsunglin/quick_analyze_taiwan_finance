from bs4 import BeautifulSoup
import requests

def scrape_stock_price(stock_code):
    # 目標網頁URL
    url = f'https://www.cnyes.com/twstock/{stock_code}'

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        stock_price = soup.find('h3', class_='jsx-2312976322 rise')

        if not stock_price:
            stock_price = soup.find('h3', class_='jsx-2312976322 fall')
        
        if stock_price:
            return f'{stock_code}　'+stock_price.text
        else:
            return f'Stock Price for {stock_code}: Not found'

    else:
        return f'Failed to retrieve webpage for {stock_code}'

# List of stock codes to scrape
stock_codes = ['00937b', '00919', '3293']

# Scrape each stock code
for code in stock_codes:
    print(scrape_stock_price(code))
