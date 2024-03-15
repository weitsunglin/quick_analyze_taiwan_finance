import requests
from bs4 import BeautifulSoup

url = 'https://www.cnyes.com/twstock/ps_historyprice.aspx?code=2356'

response = requests.get(url)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 使用class來找到所有相應的<td>標籤
    prices = soup.find_all('td', class_='rt')
    dates = soup.find_all('td', class_='cr')
    
    # 假設價格和日期是一一對應的，我們可以同時遍歷它們
    for price, date in zip(prices, dates):
        print(f'Date: {date.text}, Price: {price.text}')
else:
    print("Failed to retrieve data")
