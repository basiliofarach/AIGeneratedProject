# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from api.main import app
from models.models import Product, CartItem, PaymentRequest  # Ensure models are imported

client = TestClient(app)

class TestProductList:
    def test_get_product_list(self):
        response = client.get("/products")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_sort_products_price_low_to_high(self):
        response = client.get("/products?sort=price_asc")
        assert response.status_code == 200
        products = response.json()
        assert all(products[i]['price'] <= products[i+1]['price'] for i in range(len(products)-1))

    def test_sort_products_price_high_to_low(self):
        response = client.get("/products?sort=price_desc")
        assert response.status_code == 200
        products = response.json()
        assert all(products[i]['price'] >= products[i+1]['price'] for i in range(len(products)-1))

    def test_add_to_cart(self):
        cart_item = {"product_id": 1, "quantity": 2}
        response = client.post("/cart", json=cart_item)
        assert response.status_code == 200
        assert response.json() == {"message": "Item added to cart"}

class TestShoppingCart:
    def test_list_cart_items(self):
        response = client.get("/cart")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_change_item_quantity(self):
        product_id = 1
        new_quantity = 3
        response = client.put(f"/cart/{product_id}", json={"quantity": new_quantity})
        assert response.status_code == 200
        assert response.json() == {"message": "Cart updated"}

    def test_get_total_price(self):
        response = client.get("/cart/total")
        assert response.status_code == 200
        assert isinstance(response.json().get("total"), (int, float))

class TestPayment:
    def test_stripe_payment(self):
        payment_data = {
            "amount": 1000,
            "currency": "usd",
            "source": "tok_visa",  # This is a test token provided by Stripe
        }
        response = client.post("/payment", json=payment_data)
        assert response.status_code == 200
        assert response.json()["message"] == "Payment successful"