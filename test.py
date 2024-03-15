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
    
    # Initialize lists to hold cleaned and converted data
    prices = []
    dates = []
    
    # Process price elements
    for price in prices_elements:
        try:
            # Attempt to remove commas and convert to float
            cleaned_price = price.text.replace(',', '').replace('%', '')
            prices.append(float(cleaned_price))
        except ValueError:
            # If conversion fails, skip this value
            continue
    
    # Process date elements (assuming all date texts are valid)
    dates = [date.text for date in dates_elements][:len(prices)]  # Match dates to the number of valid prices
    
    # Ensure we have matching lengths for dates and prices
    if len(prices) != len(dates):
        print("Mismatch in lengths of dates and prices. Please check the data extraction logic.")
    else:
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
