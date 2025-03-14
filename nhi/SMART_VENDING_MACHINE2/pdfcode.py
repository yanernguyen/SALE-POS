from fpdf import FPDF
from datetime import datetime
from Cart import *


class ReceiptPDF(FPDF):
    def header(self):
        self.set_font("Times", style="B", size=18)
        self.cell(200, 10, "HÓA ĐƠN MUA HÀNG", ln=True, align="C")
        self.ln(5)


def generate_receipt(cart):
    pdf = ReceiptPDF()
    pdf.add_page()

    pdf.set_font("Times", size=12)

    """Thông tin hóa đơn """
    pdf.cell(200, 10, f"Ngày: {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True, align="R")
    pdf.ln(5)

    """Bảng sản phẩm """
    pdf.set_font("Times", style="B", size=12)
    pdf.cell(80, 8, "Sản phẩm", border=1, align="C")
    pdf.cell(30, 8, "Số lượng", border=1, align="C")
    pdf.cell(40, 8, "Giá", border=1, align="C")
    pdf.cell(40, 8, "Thành tiền", border=1, align="C")
    pdf.ln()

    """Nội dung giỏ hàng """
    pdf.set_font("Times", size=12)
    total, tax, total_after_tax = cart.get_total()

    for product_id, item in cart.get_cart().items():
        name = item["name"]
        qty = item["qty"]
        price = item["unit_price"]
        total_price = qty * price

        pdf.cell(80, 8, name, border=1)
        pdf.cell(30, 8, str(qty), border=1, align="C")
        pdf.cell(40, 8, f"{price:,.0f} đ", border=1, align="R")
        pdf.cell(40, 8, f"{total_price:,.0f} đ", border=1, align="R")
        pdf.ln()

    """Tổng tiền và thuế """
    pdf.ln(5)
    pdf.set_font("Times", style="B", size=12)

    pdf.cell(150, 8, "Tổng tiền hàng:", border=0, align="R")
    pdf.cell(40, 8, f"{total:,.0f} đ", border=0, align="R")
    pdf.ln()

    pdf.cell(150, 8, "Thuế (10%):", border=0, align="R")
    pdf.cell(40, 8, f"{tax:,.0f} đ", border=0, align="R")
    pdf.ln()

    pdf.cell(150, 8, "Tổng tiền sau thuế:", border=0, align="R")
    pdf.cell(40, 8, f"{total_after_tax:,.0f} đ", border=0, align="R")
    pdf.ln(10)

    pdf.set_font("Times", size=12)
    pdf.cell(200, 10, "Cảm ơn quý khách đã mua hàng!", ln=True, align="C")

    """Xuất PDF """
    pdf.output("receipt.pdf")


"""Kiểm tra xuất hóa đơn """
cart = Cart()
cart.add_product("p01", 2)
cart.add_product("p02", 1)
generate_receipt(cart)
