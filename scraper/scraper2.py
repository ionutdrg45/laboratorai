import sys
import requests
from bs4 import BeautifulSoup
from smtplib import SMTP_SSL as SMTP
import re
from email.mime.text import MIMEText

URL = "https://www.emag.ro/camera-auto-xiaomi-70mai-1s-ultracompacta-full-hd-1080p-sony-imx307-wifi-comenzi-vocale-model-2019-midrive-d06/pd/DM6S6WBBM/?ref=profiled_categories_home_7_1&provider=rec&recid=rec_50_a612f26ad798b90770d0f6f1c38409cee09b1b030a220979d1650635f778c857_1665735395&scenario_ID=50"

headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, 'html.parser')

title = soup.find_all(class_=re.compile("page-title"))[0].get_text().strip()
price = soup.find_all(class_=re.compile("product-new-price"))[0].get_text()

converted_price = float(price.split(",")[0])

def check_price():
    if(converted_price < 260):
        send_mail()
    else:
        print("price is still high")

def send_mail():

    SMTPserver = 'mail.bluffs.ro'
    sender =     'test@bluffs.ro'
    destination = ['draganionut307@gmail.com']

    USERNAME = "test@bluffs.ro"
    PASSWORD = "5OD;9QI9a;q0"

    # typical values for text_subtype are plain, html, xml
    text_subtype = 'plain'

    content = "The product {product_title}... has now a lower price. ({product_price} lei)".format(product_title = title, product_price = converted_price)

    subject = "New details about {product_title}..".format(product_title = title[:25])

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender # some SMTP servers will do this automatically, not all

        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
        finally:
            print("successfuly submitted")
            conn.quit()
    except:
        sys.exit( "mail failed; %s" % "CUSTOM_ERROR" ) # give an error message

check_price()