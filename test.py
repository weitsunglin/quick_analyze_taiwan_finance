import requests
from bs4 import BeautifulSoup

url = 'https://www.cnyes.com/twstock/ps_historyprice.aspx?code=2356'

# 發送HTTP請求
response = requests.get(url)

# 檢查響應狀態碼是否為200（成功）
if response.status_code == 200:
    # 使用BeautifulSoup解析HTML內容
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 根據網頁結構定位到你想要抓取的數據
    # 這裡需要你根據實際的HTML結構來定位和提取數據
    data = soup.find_all('你感興趣的HTML元素或class名稱')
    
    # 處理和打印數據
    for item in data:
        print(item.text)
else:
    print("Failed to retrieve data")

