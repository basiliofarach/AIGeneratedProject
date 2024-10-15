# api/main.py

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import requests
import stripe
from dotenv import load_dotenv
import os
from models.models import Product, CartItem, PaymentRequest  # Updated import

app = FastAPI()

# Stripe configuration
# Load environment variables from .env file
load_dotenv()

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# In-memory database for simplicity
products_db = []
cart_db = {}

# Fetch products from fakestoreapi.com
@app.on_event("startup")
def fetch_products():
    global products_db
    response = requests.get("https://fakestoreapi.com/products")
    if response.status_code == 200:
        products_db = response.json()

# Endpoints
@app.get("/products")
def get_products(sort: str = Query(None, regex="^(price_low_to_high|price_high_to_low)$")):
    if sort == "price_low_to_high":
        sorted_products = sorted(products_db, key=lambda x: x["price"])
    elif sort == "price_high_to_low":
        sorted_products = sorted(products_db, key=lambda x: x["price"], reverse=True)
    else:
        sorted_products = products_db
    return sorted_products

@app.post("/cart")
def add_to_cart(item: CartItem):
    if item.product_id not in cart_db:
        cart_db[item.product_id] = item.quantity
    else:
        cart_db[item.product_id] += item.quantity
    return {"message": "Item added to cart"}

@app.get("/cart")
def get_cart():
    cart_items = []
    for product_id, quantity in cart_db.items():
        product = next((p for p in products_db if p["id"] == product_id), None)
        if product:
            cart_items.append({"product": product, "quantity": quantity})
    return cart_items

@app.put("/cart/{product_id}")
def update_cart(product_id: int, quantity: int):
    if product_id in cart_db:
        cart_db[product_id] = quantity
        return {"message": "Cart updated"}
    else:
        raise HTTPException(status_code=404, detail="Product not found in cart")

@app.get("/cart/total")
def get_cart_total():
    total = sum(next((p["price"] for p in products_db if p["id"] == product_id), 0) * quantity for product_id, quantity in cart_db.items())
    return {"total": total}

@app.post("/payment")
def process_payment(payment_request: PaymentRequest):
    try:
        charge = stripe.Charge.create(
            amount=payment_request.amount,
            currency=payment_request.currency,
            source=payment_request.source,
            description="E-commerce payment"
        )
        return {"message": "Payment successful", "charge": charge}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))