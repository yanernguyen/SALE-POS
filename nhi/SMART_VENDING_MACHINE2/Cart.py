import json
import uuid
from typing import List, Dict
from Product import *


class Cart:
    def __init__(self):
        self.items = {}  # {product_id: {'qty': int, 'price': float}}

    def add_item(self, product: Product, quantity: int):
        if not isinstance(product, Product):
            raise ValueError("Invalid product object")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")

        if product.id not in self.items:
            self.items[product.id] = {
                'name': product.name,
                'qty': quantity,
                'unit_price': product.price,
                'image': product.image
            }
        else:
            self.items[product.id]['qty'] += quantity

    def update_item_quantity(self, product_id: str, quantity_change: int):
        if product_id in self.items:
            self.items[product_id]['qty'] += quantity_change
            if self.items[product_id]['qty'] <= 0:
                self.remove_item(product_id)

    def remove_item(self, product_id: str):
        if product_id in self.items:
            self.items.pop(product_id)

    def has_item(self, product_id: str) -> bool:
        return product_id in self.items

    def clear(self):
        self.items.clear()

    def get_total(self) -> float:
        total = 0.0
        for item in self.items.values():
            total += item['unit_price'] * item['qty']
        return total

    def to_dict(self) -> list:
        return [
            {
                'product_id': product_id,  # Thêm product_id vào dữ liệu trả về
                'name': item['name'],
                'qty': item['qty'],
                'unit_price': item['unit_price'],
                'image': item['image']
            }
            for product_id, item in self.items.items()  # Duyệt qua cả product_id và item
        ]


    def __str__(self):
        return "\n".join([
            f"{item['name']} x {item['qty']} - {item['unit_price']} VND"
            for item in self.items.values()
        ])

