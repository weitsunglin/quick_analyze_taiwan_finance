import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from matplotlib.font_manager import FontProperties

def fetch_stock_data(date, stock_no):
    url = f"http://www.twse.com.tw/exchangeReport/STOCK_DAY?response=csv&date={date}&stockNo={stock_no}"
    response = requests.get(url)
    dates, prices = [], []
    if response.status_code == 200:
        lines = response.text.split('\n')
        for line in lines:
            if line.count('",') > 8:
                parts = line.split('","')
                if len(parts) >= 7:
                    date_str = parts[0].replace('"', '')
                    try:
                        year, month, day = map(int, date_str.split('/'))
                    except ValueError:
                        continue
                    gregorian_year = year + 1911
                    date = datetime(gregorian_year, month, day)
                    closing_price = float(parts[6].replace(',', ''))
                    dates.append(date)
                    prices.append(closing_price)
    return dates, prices

def get_previous_month(date, months=1):
    month = date.month - months - 1
    year = date.year + month // 12
    month = month % 12 + 1
    day = min(date.day, [31, 29 if year % 4 == 0 else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1])
    return datetime(year, month, day).strftime("%Y%m%d")

def plot_stock_data(dates, prices, stock_no):
    plt.figure(figsize=(10, 6))
    
    count_red = 0
    count_green = 0

    # 繁中
    font_path = "C:\\Windows\\Fonts\\msjh.ttc"
    font_properties = FontProperties(fname=font_path, size=12)

    for i in range(1, len(prices)):
        if prices[i] > prices[i-1]:
            plt.plot([dates[i-1], dates[i]], [prices[i-1], prices[i]], 'r-o')
            count_red += 1
        else:
            plt.plot([dates[i-1], dates[i]], [prices[i-1], prices[i]], 'g-o')
            count_green += 1

    plt.title(f'股票代號{stock_no}長榮收盤價', fontproperties=font_properties)
    plt.xlabel('日期', fontproperties=font_properties)
    plt.ylabel('收盤價', fontproperties=font_properties)
    plt.xticks(rotation=45)
    

    plt.text(dates[0], max(prices), f'漲價:{count_red}次。跌:{count_green}次', fontproperties=font_properties, color='black')
    
    plt.tight_layout()
    plt.savefig(f"C:\\Users\\User\\Desktop\\project\\quick_analyze_taiwan_stock\\{stock_no}_3month_history.png")


if __name__ == "__main__":
    stock_number = "2603"
    current_date = datetime.now()
    current_month_str = current_date.strftime("%Y%m01")
    previous_month_str = get_previous_month(current_date)
    two_months_ago_str = get_previous_month(current_date, 2)

    two_months_ago_dates, two_months_ago_prices = fetch_stock_data(two_months_ago_str, stock_number)
    prev_dates, prev_prices = fetch_stock_data(previous_month_str, stock_number)
    curr_dates, curr_prices = fetch_stock_data(current_month_str, stock_number)

    all_dates = two_months_ago_dates + prev_dates + curr_dates
    all_prices = two_months_ago_prices + prev_prices + curr_prices

    plot_stock_data(all_dates, all_prices, stock_number)