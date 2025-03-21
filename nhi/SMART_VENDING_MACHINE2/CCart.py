import json
import uuid
from typing import List, Dict
from CProduct import *
from CProductList import *


class Cart:
    def __init__(self):
        self.cart = {}
        self.product_list = ProductList()


    def add_product(self, product_id: str, quantity: int = 1):
        product = self.product_list.get_product_by_id(product_id)
        if not product:
            return False

        current_quantity = self.cart[product_id]['qty'] if product_id in self.cart else 0
        if current_quantity + quantity > product.stock:
            return False

        if product.stock >= quantity:
            if product.id not in self.cart:
                self.cart[product.id] = {
                    'name': product.name,
                    'qty': quantity,
                    'unit_price': product.price,
                    'image': product.image
                }
            else:
                self.cart[product.id]['qty'] += quantity

            product.stock -= quantity
            return True

        return False

    def remove_product(self, product_id: str) -> bool:
        if product_id in self.cart:
            product = self.product_list.get_product_by_id(product_id)
            if product:
                product.stock += self.cart[product_id]['qty']

            del self.cart[product_id]
            return True
        return False

    def clear(self):
        self.cart.clear()

    def get_total(self) -> float:
        total = 0.0
        tax = 0.0
        total_after_tax = 0.0

        for item in self.cart.values():
            total += item['unit_price'] * item['qty']
            tax = total* 0.1
            total_after_tax = total + tax
        return total, tax, total_after_tax

    def to_dict(self):
        return [
            {
                'product_id': product_id,
                'name': item['name'],
                'qty': item['qty'],
                'unit_price': item['unit_price'],
                'image': item['image']
            }
            for product_id, item in self.cart.items()
        ]

    def load_cart(self):
        try:
            with open("data/cart.json", "r") as file:
                cart_data = json.load(file)
                if cart_data:
                    last_cart = cart_data[-1]
                    if "items" in last_cart and "total" not in last_cart:
                        self.cart.items = last_cart["items"]
                    else:
                        self.cart.items = {}
                else:
                    self.cart.items = {}
        except FileNotFoundError:
            print("Lỗi")
            self.cart.items = {}

    def checkout(self):
        if not self.cart.items:
            return -1,0,0
        total, tax, total_after_tax = self.get_total()
        if total > 0:
            self.save_cart(total, tax, total_after_tax)
            return total, tax, total_after_tax
        return -1,0,0

    def save_cart(self, total: float, tax: float, total_after_tax: float):
        try:
            with open("data/cart.json", "r") as file:
                cart_data = json.load(file)
        except FileNotFoundError:
            cart_data = []

        bill = {
            "items": self.to_dict(),
            "total": total,
            "tax" : tax,
            "total_after_tax": total_after_tax

        }
        cart_data.append(bill)

        with open("data/cart.json", "w") as file:
            json.dump(cart_data, file, indent=4)

