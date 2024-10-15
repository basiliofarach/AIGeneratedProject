# repositories/cart.py
from models.models import UpdateCartItem

class CartRepository:
    def __init__(self):
        self.cart_db = {}

    def add_to_cart(self, product_id, quantity):
        if product_id not in self.cart_db:
            self.cart_db[product_id] = quantity
        else:
            self.cart_db[product_id] += quantity
        return {"message": "Item added to cart"}

    def get_cart(self, products_db):
        cart_items = []
        for product_id, quantity in self.cart_db.items():
            product = next((p for p in products_db if p["id"] == product_id), None)
            if product:
                cart_items.append({"product": product, "quantity": quantity})
        return cart_items

    def update_cart(self, product_id, item: UpdateCartItem):
        if product_id in self.cart_db:
            self.cart_db[product_id] = item.quantity
            return {"message": "Cart updated"}
        else:
            return {"error": "Product not found in cart"}

    def get_cart_total(self, products_db):
        total = sum(next((p["price"] for p in products_db if p["id"] == product_id), 0) * quantity for product_id, quantity in self.cart_db.items())
        return {"total": total}