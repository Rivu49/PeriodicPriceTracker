import streamlit as st
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import datetime
import matplotlib.pyplot as plt

# App Title
st.title("Price Tracker")

# User Inputs
URL = st.text_input("Product URL")
EMAIL = st.text_input("Sender Email (Optional)")
PASSWORD = st.text_input("Email Password (Optional)", type="password")
RECIPIENT_EMAIL = st.text_input("Recipient Email (Optional)")
TARGET_PRICE = st.number_input("Enter Target Price (Optional)")

# Function to scrape product details
def scrape_web(URL):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
        "Accept-Encoding": "gzip, deflate",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
    }
    page = requests.get(URL, headers=headers)
    soup1 = BeautifulSoup(page.content, "html.parser")
    soup2 = BeautifulSoup(soup1.prettify(), "html.parser")

    try:
        title = soup2.find(id="title").get_text().strip()
        currency_symbol = soup2.find("span", class_="a-price-symbol").get_text().strip()
        price1 = soup2.find("span", class_="a-price-whole").get_text().strip().split()[0]
        price2 = soup2.find("span", class_="a-price-decimal").get_text().strip()
        price3 = soup2.find("span", class_="a-price-fraction").get_text().strip()
        price = currency_symbol + price1 + price2 + price3
        return title, price
    except Exception as e:
        st.error("Error scraping data: {}".format(e))
        return None, None

# Function to check price and update CSV
def check_price():
    title, price = scrape_web(URL)
    if title and price:
        today = datetime.datetime.today()
        data = [title, price, today]
        file_name = "WebScraperDataset.csv"

        # Write or append to CSV
        try:
            with open(file_name, "a+", newline="", encoding="UTF8") as f:
                writer = csv.writer(f)
                writer.writerow(data)
            df = pd.read_csv(file_name)
            st.dataframe(df)
        except Exception as e:
            st.error(f"Error updating CSV: {e}")

        # Load and visualize data
        visualize_data(file_name)

        # Price comparison and email alert
        try:
            df = pd.read_csv(file_name)
            old_price = float(df.iloc[-2, 1][1:])  # Get the previous price
            new_price = float(price[1:])  # Current price
            if new_price < old_price:
                yes="Price Drop Email Sent!"
                no="Failed to send Price Drop email:"
                send_email_alert(yes, no, "Price Drop Alert!", "The price of {} has dropped to {}. Check it out here: {}".format(title, price, URL))
            if new_price <= TARGET_PRICE:
                yes="Target Price Email Sent!"
                no="Failed to send Target Price email:"
                send_email_alert(yes, no, "Target Price Alert!", "The price of {} has dropped to {} reaching your target price of {}. Check it out here: {}".format(title, price, TARGET_PRICE, URL))
        except Exception as e:
            st.warning("No previous data for comparison.")

# Function to visualize price trends
def visualize_data(file_name):
    try:
        df = pd.read_csv(file_name, names=["Title", "Price", "Date-Time"], header=None, skiprows=1)
        df["Price"] = df["Price"].str.extract(r'(\d+\.\d+)').astype(float)  # Convert price to numeric

        # Plot the data
        fig, ax = plt.subplots()
        ax.plot(df["Date-Time"], df["Price"], marker="o", linestyle="-", color="b")
        ax.set_title("Price Trend Over Time")
        ax.set_xlabel("Date-Time")
        ax.set_ylabel("Price")
        ax.grid(True)
        st.pyplot(fig)

        # Display data
        st.dataframe(df)
    except Exception as e:
        st.error(f"Error visualizing data: {e}")

# Function to send email
def send_email_alert(yes, no, subject, body):
    # Validate email credentials
    if not EMAIL or not PASSWORD or not RECIPIENT_EMAIL:
        st.error("Email credentials are missing. Please provide sender email, password, and recipient email.")
        return
    
    msg = MIMEMultipart()
    msg["From"] = EMAIL
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        st.success(yes)
    except Exception as e:
        st.error(no, e)

# Button to trigger price check
if st.button("Check Price"):
    check_price()