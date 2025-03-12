import json
from datetime import datetime
from Product import Product
from CProductList import ProductList

# Khởi tạo danh sách sản phẩm
product_list = ProductList()

# Admin thực hiện các thao tác
admin_name = "admin1"

# 📌 1. Kiểm tra sản phẩm trước khi cập nhật
print("📌 Danh sách sản phẩm trước khi cập nhật:")
for product in product_list.products:
    print(f"{product.id} - {product.name} - {product.stock} sản phẩm")

# 📌 2. Admin cập nhật số lượng sản phẩm
product_id = "SP_0002"  # ID của sản phẩm muốn cập nhật
quantity = 5  # Thêm 5 sản phẩm vào kho

print(f"\n🔄 Admin '{admin_name}' cập nhật số lượng sản phẩm {product_id} (+{quantity})")
success = product_list.update_product_stock(product_id, quantity, admin_name)

if success:
    print("✅ Cập nhật thành công!")
else:
    print("❌ Cập nhật thất bại, sản phẩm không tồn tại.")

# 📌 3. Kiểm tra sản phẩm sau khi cập nhật
print("\n📌 Danh sách sản phẩm sau khi cập nhật:")
for product in product_list.products:
    print(f"{product.id} - {product.name} - {product.stock} sản phẩm")

# 📌 4. Kiểm tra lịch sử nhập hàng
print("\n📜 Lịch sử nhập hàng:")
try:
    with open("data/history.json", "r", encoding="utf-8") as file:
        history = json.load(file)
        for entry in history[-5:]:  # Hiển thị 5 lịch sử nhập hàng gần nhất
            print(f"{entry['time']} - {entry['admin']} - {entry['action']} {entry['product_id']} ({entry['quantity']})")
except (FileNotFoundError, json.JSONDecodeError):
    print("❌ Không tìm thấy lịch sử nhập hàng.")

