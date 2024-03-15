import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import pandas as pd

# URL of the page
url = 'https://www.cnyes.com/twstock/ps_historyprice.aspx?code=2356'

# Send a GET request
response = requests.get(url)

if response.status_code == 200:
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extracting prices and dates using BeautifulSoup
    prices_elements = soup.find_all('td', class_='rt')
    dates_elements = soup.find_all('td', class_='cr')
    
    # Pair dates with prices before filtering
    date_price_pairs = [(date.text, price.text.replace(',', '').replace('%', '')) for date, price in zip(dates_elements, prices_elements)]
    
    # Filter out pairs where the price is not a valid float
    valid_pairs = [(date, price) for date, price in date_price_pairs if price.lstrip('-').replace('.', '', 1).isdigit()]
    
    # Separate the valid pairs back into dates and prices
    dates, prices = zip(*valid_pairs)  # This creates two tuples: one with dates and one with prices
    
    # Convert prices to floats
    prices = [float(price) for price in prices]
    
    # Convert dates and prices into a DataFrame
    df = pd.DataFrame({
        'Date': pd.to_datetime(dates),
        'Price': prices
    })
    
    # Plotting the data
    plt.figure(figsize=(10, 5))
    plt.plot(df['Date'], df['Price'], marker='o', linestyle='-', color='b')
    plt.title('Price Trend')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.xticks(rotation=45)
    plt.tight_layout()
    
    # Save the plot to a file without showing it
    plt.savefig('price_trend.png')
else:
    print("Failed to retrieve data")
