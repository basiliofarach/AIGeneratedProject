# repositories/product.py

import requests

class ProductRepository:
    def __init__(self):
        self.products_db = []

    def fetch_products(self):
        response = requests.get("https://fakestoreapi.com/products")
        if response.status_code == 200:
            self.products_db = response.json()

    def get_products(self, sort=None):
        if sort == "price_asc":
            return sorted(self.products_db, key=lambda x: x["price"])
        elif sort == "price_desc":
            return sorted(self.products_db, key=lambda x: x["price"], reverse=True)
        return self.products_db