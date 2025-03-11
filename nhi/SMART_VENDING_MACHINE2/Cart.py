import json
import uuid
from typing import List, Dict
from Product import *
from CProductList import *


class Cart:
    def __init__(self):
        self.cart = {}  # {product_id: {'qty': int, 'price': float}}
        self.product_list = ProductList()

    def get_cart(self):
        return self.cart

    def add_item(self, product: Product, quantity: int):
        if not isinstance(product, Product):
            raise ValueError("Invalid product object")
        if not isinstance(quantity, int) or quantity <= 0:
            raise ValueError("Quantity must be a positive integer")

        if product.id not in self.cart:
            self.cart[product.id] = {
                'name': product.name,
                'qty': quantity,
                'unit_price': product.price,
                'image': product.image
            }
        else:
            self.cart[product.id]['qty'] += quantity

    def update_item_quantity(self, product_id: str, quantity_change: int):
        if product_id in self.cart:
            self.cart[product_id]['qty'] += quantity_change
            if self.cart[product_id]['qty'] <= 0:
                self.remove_item(product_id)

    def remove_item(self, product_id: str):
        if product_id in self.cart:
            self.cart.pop(product_id)

    def has_item(self, product_id: str) -> bool:
        return product_id in self.cart

    def clear(self):
        self.cart.clear()

    def get_total(self) -> float:
        total = 0.0
        for item in self.cart.values():
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
            for product_id, item in self.cart.items()  # Duyệt qua cả product_id và item
        ]


    def __str__(self):
        return "\n".join([
            f"{item['name']} x {item['qty']} - {item['unit_price']} VND"
            for item in self.cart.values()
        ])

    def load_cart(self):
        try:
            with open("data/cart.json", "r") as file:
                cart_data = json.load(file)
                if cart_data:  # Kiểm tra nếu file không rỗng
                    last_cart = cart_data[-1]  # Lấy hóa đơn cuối cùng
                    if "items" in last_cart and "total" not in last_cart:  # Kiểm tra nếu đây là giỏ hàng chưa thanh toán
                        self.cart.items = last_cart["items"]  # Tải giỏ hàng vào bộ nhớ
                    else:
                        self.cart.items = {}  # Nếu không có giỏ hàng chưa thanh toán, để trống
                else:
                    self.cart.items = {}
        except FileNotFoundError:
            print("⚠️ Lỗi: Không tìm thấy file cart.json.")
            self.cart.items = {}

    def remove_from_cart(self, product_id: str) -> bool:
        """Xóa sản phẩm khỏi giỏ hàng theo ID."""
        product = self.product_list.get_product_by_id(product_id)
        if product in self.cart.items:  # Kiểm tra nếu sản phẩm có trong giỏ hàng
            self.remove_item(product)  # Xóa sản phẩm khỏi giỏ hàng
            product.stock += 1  # Tăng lại số lượng tồn kho
            self.product_list.save_products()  # Lưu thay đổi tồn kho vào file
            return True
        return False  # Không xóa được (không tìm thấy sản phẩm trong giỏ hàng)

    def checkout(self) -> float: #Nằm trong giao diện
        if not self.cart.items:
            return 0  # Giỏ hàng trống, không thực hiện thanh toán
        total = self.get_total()  # Tính tổng tiền
        if total > 0:
            # Lưu thông tin giỏ hàng vào file cart.json
            self.save_cart(total)
            # Xóa giỏ hàng sau khi thanh toán
            return total
        return 0

    def save_cart(self, total: float):
        try:
            with open("data/cart.json", "r") as file:
                cart_data = json.load(file)
        except FileNotFoundError:
            cart_data = []
        # Thêm hóa đơn mới vào danh sách
        bill = {
            "items": self.to_dict(),  # Lấy thông tin giỏ hàng
            "total": total,  # Tổng tiền
        }
        cart_data.append(bill)
        # Lưu lại danh sách hóa đơn vào file cart.json
        with open("data/cart.json", "w") as file:
            json.dump(cart_data, file, indent=4)

    def add_to_cart(self, product_id: str) -> bool:
        product = self.product_list.get_product_by_id(product_id)
        if product.stock > 0:  # Kiểm tra sản phẩm có tồn tại và còn hàng
            self.add_item(product, 1)  # Thêm sản phẩm vào giỏ hàng
            return True
        return False