import json
import uuid
from typing import List, Dict
from Product import *
from CProductList import *


class Cart:
    def __init__(self):
        self.cart = {}  # {product_id: {'qty': int, 'price': float}}
        self.product_list = ProductList()
        TAX_RATE = 0.1

    def get_cart(self):
        return self.cart

    def add_product(self, product_id: str, quantity: int = 1) -> bool:
        product = self.product_list.get_product_by_id(product_id)
        if not product:
            return False

        current_quantity = self.cart[product_id]['qty'] if product_id in self.cart else 0
        if current_quantity + quantity > product.stock:
            return False
        """Kiểm tra số lượng tồn kho"""
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

            """Cập nhật số lượng tồn kho"""
            product.stock -= quantity
            return True

        return False

    def update_item_quantity(self, product_id: str, quantity_change: int):
        if product_id in self.cart:
            self.cart[product_id]['qty'] += quantity_change
            if self.cart[product_id]['qty'] <= 0:
                self.remove_product(product_id)

    def remove_product(self, product_id: str) -> bool:
        if product_id in self.cart:
            product = self.product_list.get_product_by_id(product_id)
            if product:
                product.stock += self.cart[product_id]['qty']  # Hoàn lại số lượng vào kho
                self.product_list.save_products()  # Lưu thay đổi tồn kho vào file

            del self.cart[product_id]  # Xóa sản phẩm khỏi giỏ hàng
            return True
        return False
    def has_item(self, product_id: str) -> bool:
        return product_id in self.cart

    def clear(self):
        self.cart.clear()

    def get_total(self) -> float:
        total = 0.0
        tax = 0.0  # Khởi tạo trước
        total_after_tax = 0.0

        for item in self.cart.values():
            total += item['unit_price'] * item['qty']
            tax = total* 0.1
            total_after_tax = total + tax
        return total, tax, total_after_tax

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
            print("⚠Lỗi: Không tìm thấy file cart.json.")
            self.cart.items = {}



    def checkout(self) -> float: #Nằm trong giao diện
        if not self.cart.items:
            return -1,0,0  # Giỏ hàng trống, không thực hiện thanh toán
        total, tax, total_after_tax = self.get_total()  # Tính tổng tiền
        if total > 0:
            """ Lưu thông tin giỏ hàng vào file cart.json"""
            self.save_cart(total)
            self.save_cart(total_after_tax)
            """ Xóa giỏ hàng sau khi thanh toán"""
            return total, tax, total_after_tax
        return -1,0,0

    def save_cart(self, total: float):
        try:
            with open("data/cart.json", "r") as file:
                cart_data = json.load(file)
        except FileNotFoundError:
            cart_data = []
        """Thêm hóa đơn mới vào danh sách"""
        bill = {
            "items": self.to_dict(),  # Lấy thông tin giỏ hàng
            "total": total,  # Tổng tiền
        }
        cart_data.append(bill)
        """Lưu lại danh sách hóa đơn vào file cart.json"""
        with open("data/cart.json", "w") as file:
            json.dump(cart_data, file, indent=4)

