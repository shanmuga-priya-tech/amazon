from flask import Flask,jsonify
from flask_cors import CORS
from bs4 import BeautifulSoup
from pymongo import MongoClient
import os
import json

app=Flask(__name__)
CORS(app,origins="http://localhost:8080")
client=MongoClient(" ")
app.db=client.amazon


# Read the HTML file
with open("index.html", "r", encoding="utf-8") as file:
    html_content = file.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(html_content, "html.parser")

laptop_container = soup.find_all("div", class_="puis-card-container s-card-container s-overflow-hidden aok-relative puis-include-content-margin puis puis-v3vtwxgppca0z12v18v51zrqona s-latency-cf-section s-card-border")

product_Name = ""
img_url= ""
original_price = ""
current_price = ""
star_rating = ""

for container in laptop_container:
    # Try to find product name
    product_name_span = container.find("span", class_="a-size-medium a-color-base a-text-normal")
    if product_name_span:
        product_Name = product_name_span.text.strip()

    #try to find img link
    img_relative_url=container.find("img")["src"]
    filename = os.path.basename(img_relative_url)
    if img_relative_url:
            img_url=f"https://m.media-amazon.com/images/I/{filename}"

    
    # Try to find original price
    original_price_span = container.find("span", class_="a-price a-text-price")
    if original_price_span:
        original_price_text = original_price_span.find("span").text.strip()
        original_price_text = original_price_text.replace("₹", "")
        original_price = original_price_text
    
        

    # Try to find current price
    current_price_span = container.find("span", class_="a-price-whole")
    if current_price_span:
        current_price = current_price_span.text.strip()
        

    # Try to find star rating
    star_rating_span = container.find("span", class_="a-icon-alt")
    if star_rating_span:
        star_rating_text = star_rating_span.text.strip()
        star_rating = star_rating_text.split()[0]#3.9 out of 5 rating


    product_details={
        "Product_name":product_Name,
        "img_url":img_url,
        "Original_price": original_price,
        "Current_price": current_price,
        "Star_rating":star_rating
    }
    app.db.products.insert_one(product_details)

@app.route("/amazon/laptops",methods=["GET"])
def laptop_details():
    try:
        laptop=list(app.db.products.find())
        return jsonify ({"products": json.loads(json.dumps( laptop, default=str))}),200
    except Exception as e:
            print(e)
            return jsonify({"message": "Internal server error"}), 500
    
    

