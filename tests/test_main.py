import pytest
from fastapi.testclient import TestClient
from api.main import app

# api/test_main.py


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
        product_id = 1
        response = client.post(f"/cart/add/{product_id}")
        assert response.status_code == 200
        assert response.json() == {"message": "Product added to cart"}

class TestShoppingCart:
    def test_list_cart_items(self):
        response = client.get("/cart")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_change_item_quantity(self):
        product_id = 1
        new_quantity = 3
        response = client.put(f"/cart/update/{product_id}", json={"quantity": new_quantity})
        assert response.status_code == 200
        assert response.json() == {"message": "Quantity updated"}

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
            "description": "Test payment"
        }
        response = client.post("/payment", json=payment_data)
        assert response.status_code == 200
        assert response.json() == {"message": "Payment successful"}