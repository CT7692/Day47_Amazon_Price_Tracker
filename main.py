import lxml
import smtplib
import os
from bs4 import BeautifulSoup
from security import safe_requests

MY_EMAIL = "jrydel92@gmail.com"
MY_PW = os.environ.get("GMAIL_PW")

def send_email_notif(prod_name, prod_price, str_price):
    target_price = 700
    notification = (f"Subject: LOW PRICE ALERT!\n\nThe price of the {prod_name} "
                    f"has gone down to {str_price}. Buy now!")

    if prod_price <= target_price:
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=MY_EMAIL, password=MY_PW)
            connection.sendmail(from_addr=MY_EMAIL, to_addrs=MY_EMAIL, msg=notification)
    return notification


def make_soup(product_url):
    request_header = {
        "Accept-Language": "en-US",
        "User-Agent": "Chrome/120.0.0.0"
    }

    response = safe_requests.get(product_url,headers=request_header)
    soup = BeautifulSoup(response.text, 'lxml')
    return soup
my_url = ("https://www.amazon.com/"
                                 "Neumann-Diaphragm-Microphone-Suspension-Shockmount/"
                                 "dp/B0753KLBT4/ref=sr_1_8?crid=20K0SQ7WG6913&keywords=neumann+microphone"
                                 "&qid=1707423867&sprefix=neumann+%2Caps%2C366&"
                                 "sr=8-8&ufe=app_do%3Aamzn1.fos.2b70bf2b-6730-4ccf-ab97-eb60747b8daf")

my_soup = make_soup(my_url)
product = my_soup.find(id="productTitle").getText().lstrip().rstrip()
str_price = my_soup.find(name="span", class_="aok-offscreen").getText().strip()
price = float(str_price.strip('$'))
email = send_email_notif(product, price, str_price)
