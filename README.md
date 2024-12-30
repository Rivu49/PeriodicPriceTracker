# Price_Tracker

## Purpose

This application tracks the product price periodically and notifies the user of price drop.

## Tech Stack

- **Streamlit**: For creating a user-friendly web interface.
- **requests**: For making HTTP/HTTPS requests in a simple user friendly way.
- **BeautifulSoup**: For web scrapping.
- **csv** and **pandas**: For data manipulation.
- **email.mime**: To create and handle MIME (Multipurpose Internet Mail Extensions) objects.
- **smtplib**: To send emails using the Simple Mail Transfer Protocol.
- **matplotlib**: For plotting of graph.

## Key Features

- Tracks the price and stores the data in a csv file.
- Shows a graph of Price vs Date-Time.
- Sends mail on price drops or on reaching target price.

## Installation

To run this application locally, follow these steps:

1. **Download the files**
    
2. **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```
    
3. **Run price_tracker**

## Usage

Once the application is running, enter the required parameters to get a notification on price drops or reaching target price.

### Input Parameters

- **URL**: URL of the product.
- **Sender Email (Optional)**: Email of the sender.
- **Email Password (Optional)**: Email (app) password of the sender.
- **Recipient Email (Optional)**: Email of the receiver.
- **Target Price**: Target Price of the user.
