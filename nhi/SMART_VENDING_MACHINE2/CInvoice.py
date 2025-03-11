import json
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox
from Cart import Cart

import os
DATA_PATH = os.path.join("data", "invoices.json")
class Invoice:
    def __init__(self, cart: Cart, total: float):
        self.cart = cart  # Chuyển giỏ hàng thành danh sách sản phẩm
        self.total = total  # Lấy tổng tiền từ Cart
        self.datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """ Chuyển hóa đơn thành dictionary để lưu JSON """
        return {
            "cart": self.cart.to_dict() if hasattr(self.cart, "to_dict") else self.cart,
            "datetime": self.datetime,
            "total": self.total
        }

    def save_to_json(self):
        """ Lưu hóa đơn vào file JSON """
        try:
            with open(DATA_PATH, "r", encoding="utf-8") as file:
                invoices = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            invoices = []

        invoices.append(self.to_dict())  # Thêm hóa đơn mới

        with open(DATA_PATH, "w", encoding="utf-8") as file:
            json.dump(invoices, file, indent=4, ensure_ascii=False)
