from tkinter import *
import re
import sys
import requests
from bs4 import BeautifulSoup
from smtplib import SMTP_SSL as SMTP
from email.mime.text import MIMEText

window = Tk()
window.title("My App")
window.geometry("500x370")
window.resizable(False, False)

window.iconbitmap("applogo.ico")

title_image = PhotoImage(file="applogo.png")

title_label = Label(image=title_image)

instructions_label = Label(text="Enter the product name and email below and click Submit to submit the form:")

product_name_label = Label(text="Product Name:")
product_name_var = StringVar()
product_name_field = Entry(textvariable=product_name_var, width=30)

email_label = Label(text="Email:")
email_var = StringVar()
email_field = Entry(textvariable=email_var, width=30)

error_label = Label(fg="red")
done_label = Label(fg="green")

def on_button_click():
  done_label.config(text="")
  product_name = product_name_var.get()
  email = email_var.get()
  
  if len(product_name) == 0:
    error_label.config(text="Please enter a product name.")
    return
  elif len(product_name) > 50:
    error_label.config(text="The product name must be 50 characters or less.")
    return
  
  if len(email) == 0:
    error_label.config(text="Please enter an email.")
    return
  elif len(email) > 50:
    error_label.config(text="The email must be 50 characters or less.")
    return
  elif not re.match(r"[^@]+@[^@]+\.[^@]+", email):
    error_label.config(text="Please enter a valid email.")
    return
  
  error_label.config(text="")
  product_name_var.set("")
  email_var.set("")
  make_raport(product_name, email)

def make_raport(product_name, email):
    productsEmail = []
    
    URL = "https://www.emag.ro/search/" + product_name + "?ref=effective_search"

    headers = {"User-Agent":'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}
    page = requests.get(URL, headers=headers)

    soup = BeautifulSoup(page.content, 'html.parser')

    title = soup.find_all(class_=re.compile("title-phrasing"))[0].get_text().strip()

    if "0 rezultate pentru" in title:
        error_label.config(text="No results found for your entry.")
        return
    
    products = soup.find_all(class_=re.compile("card-v2-title"))
    
    for product in products[:10]:
        product_url = product.get("href")

        pageProduct = requests.get(product_url, headers=headers)

        soupProduct = BeautifulSoup(pageProduct.content, 'html.parser')

        titleProduct = soupProduct.find_all(class_=re.compile("page-title"))[0].get_text().strip()
        ratingProduct = soupProduct.find_all(class_=re.compile("rating-text"))[0].get_text().strip()
        priceProduct = soupProduct.find_all(class_=re.compile("product-new-price"))[0].get_text()

        converted_price = float(priceProduct.split(",")[0])
        converted_rating = 1
        try:
            converted_rating = float(ratingProduct.split(" ")[0])
        except:
            converted_rating = 1

        productsEmail.append({
            'name': titleProduct,
            'price': converted_price,
            'rating': converted_rating,
            'link': product_url,
        })

    productsEmail.sort(key=lambda x: x['price'] / x['rating'])

    recommendation = productsEmail[0]

    send_mail(productsEmail[:4], recommendation, email, product_name)

def send_mail(productsEmail, recommendation, email, search):
    SMTPserver = 'mail.bluffs.ro'
    sender =     'test@bluffs.ro'
    destination = [email]

    USERNAME = "test@bluffs.ro"
    PASSWORD = "5OD;9QI9a;q0"

    text_subtype = 'html'

    content = "<p>Results for your search: " + search +"</p>"
    for product in productsEmail:
       content += f"<p><a href='{product['link']}'>{product['name']}</a> - {str(product['price'])} lei - {str(product['rating'])} rating</p>"
    content += f"<p>Considering the Price/Rating ratio we recommend to you to give a look at: <a href='{recommendation['link']}'>{recommendation['name']}</a></p>"

    subject = "Search Results for " + search

    try:
        msg = MIMEText(content, text_subtype)
        msg['Subject'] = subject
        msg['From'] = sender

        conn = SMTP(SMTPserver)
        conn.set_debuglevel(False)
        conn.login(USERNAME, PASSWORD)
        try:
            conn.sendmail(sender, destination, msg.as_string())
            done_label.config(text="Report sent successfully.")
        finally:
            conn.quit()
    except:
        sys.exit( "mail failed; %s" % "CUSTOM_ERROR" )

button = Button(text="Submit", command=on_button_click, fg="white", bg="#3498db", font=("Arial", 14, "bold"), activebackground="#2980b9")

title_label.pack()
instructions_label.pack()
product_name_label.pack()
product_name_field.pack()
email_label.pack()
email_field.pack()
error_label.pack()
done_label.pack()
button.pack(pady=20)

window.mainloop()
