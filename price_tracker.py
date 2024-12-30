EMAIL = input("Enter sender email address: ")
PASSWORD = input("Enter sender email password (app password): ")
RECIPIENT_EMAIL = input("Enter receiver email address: ")
target_price=int(input("Enter target price: "))

# Define the URL of the Amazon product page
URL=input("Enter the URL of the product: ")

import requests
from bs4 import BeautifulSoup

import csv

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

import matplotlib.pyplot as plt

import datetime
import time

# Define headers to mimic a browser request and avoid potential blocking
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Accept-Encoding":"gzip, deflate",
    "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "DNT":"1",
    "Connection":"close",
    "Upgrade-Insecure-Requests":"1"
}

# Make a GET request to the specified URL with the defined headers
page = requests.get(URL, headers=headers)

# Parse the page content with BeautifulSoup
soup1 = BeautifulSoup(page.content, 'html.parser')
soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

# Extract the product title using the HTML element's ID
title = soup2.find(id='title').get_text().strip()

# Extract the product price components: currency_symbol, whole, decimal, and fractional parts
currency_symbol = soup2.find('span', class_='a-price-symbol').get_text().strip()
price1 = soup2.find('span', class_='a-price-whole').get_text().strip().split()[0]
price2 = soup2.find('span', class_='a-price-decimal').get_text().strip()
price3 = soup2.find('span', class_='a-price-fraction').get_text().strip()

# Combine the price components into a single price string
price = (price1 + price2 + price3)

# Print the extracted title and price
print(title)
print(f'{currency_symbol}{price}')

# Get today's date
today=datetime.datetime.today()
print(today)

# Define the header for the CSV file
header = ['Title', f'Price (in {currency_symbol})', 'Date-Time']

# Create a list of data to write into the CSV
data = [title, price, today]

# Open a new CSV file in write mode with UTF-8 encoding
with open('WebScraperDataset.csv', 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)  # Create a CSV writer object
    writer.writerow(header)  # Write the header row to the CSV
    writer.writerow(data)    # Write the data row to the CSV

import pandas as pd

# Read the CSV file into a DataFrame
df=pd.read_csv(r'WebScraperDataset.csv')

print(df)

def check_price():

    page=requests.get(URL,headers=headers)

    # Parse the page content with BeautifulSoup
    soup1=BeautifulSoup(page.content,'html.parser')
    soup2=BeautifulSoup(soup1.prettify(),'html.parser')

    # Extract the product title using the HTML element's ID
    title=soup2.find(id='title').get_text().strip()

    # Extract the product price components: whole, decimal, and fractional parts  
    price1 = soup2.find('span', class_='a-price-whole').get_text().strip().split()[0]
    price2 = soup2.find('span', class_='a-price-decimal').get_text().strip()
    price3 = soup2.find('span', class_='a-price-fraction').get_text().strip()

    # Combine the price components into a single price string
    price=(price1 + price2 + price3)

    # Get today's date
    today=datetime.datetime.today()
    
    # Create a list of data to write into the CSV
    data = [title, price,today]

    # Open for reading and appending (writing at end of file) mode with UTF-8 encoding
    with open('WebScraperDataset.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)
    
    # Read the CSV file into a DataFrame
    df=pd.read_csv(r'WebScraperDataset.csv')

    print(df)

    #plot the data
    visualize_data('WebScraperDataset.csv')

    #check mail conditions
    old=float(df.iat[-2,1])
    if float(price) < old:
        yes="Price Drop Email Sent!"
        no="Failed to send Price Drop email:"
        send_email_alert(yes, no, "Price Drop Alert!", "The price of {} has dropped to {}{}. Check it out here: {}".format(title, currency_symbol, price, URL))
    if float(price) <= target_price:
        yes="Target Price Email Sent!"
        no="Failed to send Target Price email:"
        send_email_alert(yes, no, "Target Price Alert!", "The price of {} has dropped to {}{} reaching your target price of {}{}. Check it out here: {}".format(title, currency_symbol, price, currency_symbol, target_price, URL))

# Function to visualize price trends
'''the server pauses when the graph is open. close graph window to proceed. so as a workaround the graph closes after 5 secs'''
def visualize_data(file_name):
    try:
        # Read the data from the CSV file
        df = pd.read_csv(file_name, names=['Title', f'Price (in {currency_symbol})', 'Date-Time'], header=None, skiprows=1)
        df[f'Price (in {currency_symbol})'] = df[f'Price (in {currency_symbol})'].astype(float)  # Ensure it's numeric

        # Enable interactive mode
        plt.ion()

        # Plot the data
        fig, ax = plt.subplots()
        ax.plot(df["Date-Time"], df[f'Price (in {currency_symbol})'], marker="o", linestyle="-", color="b")
        ax.set_title("Price Trend Over Time")
        ax.set_xlabel("Date-TIme")
        ax.set_ylabel(f'Price (in {currency_symbol})')
        ax.grid(True)
        
        # Show the plot
        plt.show()
        plt.pause(5)
        plt.close()
        
    except Exception as e:
        print(f"Error visualizing data: {e}")

#send mail
def send_email_alert(yes, no, subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        print(yes)
    except Exception as e:
        print(no, e)
   
# Infinite loop to continuously check the product price at regular intervals
while True:
    check_price()  # Call the function to scrape the current price and title from the specified URL
    time.sleep(30)  # Pause execution for 86400 seconds (24 hours) before checking again