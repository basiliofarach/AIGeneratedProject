# api/main.py

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import stripe
import os
from dotenv import load_dotenv
from models.models import Product, CartItem, PaymentRequest, UpdateCartItem
from repositories.product import ProductRepository
from repositories.cart import CartRepository

app = FastAPI()

# Load environment variables from .env file
load_dotenv()

# Stripe configuration
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Initialize repositories
product_repo = ProductRepository()
cart_repo = CartRepository()

# Fetch products from fakestoreapi.com
@app.on_event("startup")
def fetch_products():
    product_repo.fetch_products()

# Endpoints
@app.get("/products")
def get_products(sort: str = Query(None, regex="^(price_asc|price_desc)$")):
    return product_repo.get_products(sort)

@app.post("/cart")
def add_to_cart(item: CartItem):
    return cart_repo.add_to_cart(item.product_id, item.quantity)

@app.get("/cart")
def get_cart():
    return cart_repo.get_cart(product_repo.products_db)

@app.put("/cart/{product_id}")
def update_cart(product_id: int, item: UpdateCartItem):
    result = cart_repo.update_cart(product_id, item)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/cart/total")
def get_cart_total():
    return cart_repo.get_cart_total(product_repo.products_db)

@app.post("/payment")
def process_payment(payment_request: PaymentRequest):
    try:
        # Calculate the total amount from the cart
        cart_total = cart_repo.get_cart_total(product_repo.products_db)
        # Create a charge using Stripe
        charge = stripe.Charge.create(
            amount=int(cart_total["total"] * 100) | payment_request.amount,  # Stripe expects the amount in cents
            currency=payment_request.currency,
            source=payment_request.source,
            description="E-commerce payment"
        )
        
        return {"message": "Payment successful", "charge": charge}
    except stripe.error.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))