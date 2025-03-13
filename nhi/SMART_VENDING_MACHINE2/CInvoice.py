import json
from datetime import datetime
from PyQt6.QtWidgets import QMessageBox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from Cart import Cart
import time
import os

import os
DATA_PATH = os.path.join("data", "invoices.json")
class Invoice:
    def __init__(self, cart: Cart, total: float, tax:float, total_after_tax:float):
        self.cart = cart  # Chuyển giỏ hàng thành danh sách sản phẩm
        self.total = total  # Lấy tổng tiền từ Cart
        self.tax = tax
        self.total_after_tax = total_after_tax
        self.datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        """ Chuyển hóa đơn thành dictionary để lưu JSON """
        return {
            "cart": self.cart.to_dict() if isinstance(self.cart, Cart) else self.cart,
            "datetime": self.datetime,
            "total": self.total,
            "tax": self.tax,
            "total_after_tax":self.total_after_tax
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

    def generate_invoice(self):
        invoices_folder = os.path.join(os.getcwd(), "Invoices")
        if not os.path.exists(invoices_folder):
            os.makedirs(invoices_folder)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # Ví dụ: 20250312_154530
        file_name = f"invoice_{timestamp}.pdf"
        file_path = os.path.join(invoices_folder, file_name)
        invoice_data = self.to_dict()

        c = canvas.Canvas(file_path, pagesize=letter)
        c.setFont("Helvetica", 12)

        # Tiêu đề hóa đơn
        c.drawString(50, 750, "RECEIPT")
        c.drawString(50, 730, f"Date: {invoice_data['datetime']}")

        # Vẽ bảng danh sách sản phẩm
        y_position = 700
        c.drawString(50, y_position, "Product Name")
        c.drawString(150, y_position, "Quantity")
        c.drawString(250, y_position, "Price")
        # c.drawString(350, y_position, "Total")

        y_position -= 20
        for item in invoice_data['cart'].values():
            c.drawString(50, y_position, item['name'])
            c.drawString(150, y_position, str(item['qty']))
            c.drawString(250, y_position, f"{item['unit_price']:,.0f}")
            y_position -= 20

        # Hiển thị tổng tiền
        y_position -= 30
        c.drawString(100, y_position, f"Total: {invoice_data['total']:,.0f}")

        y_position -= 40
        c.drawString(100, y_position, f"Tax: {invoice_data['tax']:,.0f}")

        y_position -= 50
        c.drawString(100, y_position, f"Total after tax: {invoice_data['total_after_tax']:,.0f}")

        c.save()
        print(f"✅ Hóa đơn đã được lưu tại {file_name}")

    # def generate_receipt(self):
    #     receipt_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #     receipt_id = f"SM-{int(time.time())}"
    #     invoice_data = self.to_dict()
    #
    #     # Tạo nội dung hóa đơn
    #     receipt_content = f"===== SMART MART RECEIPT =====\n"
    #     receipt_content += f"Receipt ID: {receipt_id}\n"
    #     receipt_content += f"Date: {receipt_time}\n"
    #     receipt_content += f"---------------------------\n"
    #
    #     for item in invoice_data['cart'].values():
    #         price = item['price'] * item['quantity']
    #         receipt_content += f"{item['name']} x{item['quantity']}: {price:,.0f}đ\n"
    #
    #
    #     receipt_content += f"---------------------------\n"
    #     receipt_content += f"Total: {invoice_data['total']:,.0f}đ\n"
    #     receipt_content += f"Thank you for shopping!\n"
    #
    #     # Lưu hóa đơn vào file hoặc hiển thị
    #     self.show_receipt(receipt_content)
    #     self.save_receipt_to_history(receipt_id, receipt_content, total)
    #
    #     return receipt_content
