# models/models.py

from pydantic import BaseModel

class Product(BaseModel):
    id: int
    title: str
    price: float
    description: str
    category: str
    image: str

class CartItem(BaseModel):
    product_id: int
    quantity: int

class PaymentRequest(BaseModel):
    amount: int
    currency: str
    source: str

class UpdateCartItem(BaseModel):
    quantity: int