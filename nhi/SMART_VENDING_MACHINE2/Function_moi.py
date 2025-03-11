import json
from typing import List, Optional
from Product import Product
from Cart import Cart


class SmartMartFunctions:
    def __init__(self):
        self.products: List[Product] = self.load_products()  # Danh sách các sản phẩm từ file
        self.cart = Cart()  # Giỏ hàng
    def get_cart(self):
        return self.cart

    def load_products(self) -> List[Product]:
        try:
            with open("data/products.json", "r") as file:
                products_data = json.load(file)
                return [Product(**data) for data in products_data]  # Chuyển đổi dữ liệu JSON thành đối tượng Product
        except FileNotFoundError:
            print("⚠️ Lỗi: Không tìm thấy file products.json.")
            return []

    def save_products(self):
        try:
            with open("data/products.json", "w") as file:
                json.dump([product.to_dict() for product in self.products], file, indent=4)
        except Exception as e:
            print(f"⚠️ Lỗi khi lưu file products.json: {e}")

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

    def save_cart(self, total: float):
        try:
            with open("data/cart.json", "r") as file:
                cart_data = json.load(file)
        except FileNotFoundError:
            cart_data = []
        # Thêm hóa đơn mới vào danh sách
        bill = {
            "items": self.cart.to_dict(),  # Lấy thông tin giỏ hàng
            "total": total,  # Tổng tiền
        }
        cart_data.append(bill)
        # Lưu lại danh sách hóa đơn vào file cart.json
        with open("data/cart.json", "w") as file:
            json.dump(cart_data, file, indent=4)

    def search_products(self, keyword: str) -> List[Product]:
        return [product for product in self.products if keyword.lower() in product.name.lower()]

    def filter_product(self, category: str) -> List[Product]:
        return [product for product in self.products if product.category == category]

    def get_product_by_id(self, product_id: str) -> Optional[Product]:
        for product in self.products:
            if product.id == product_id:
                return product
        return None

    def get_product_by_name(self, product_name: str):
        for product in self.products:
            if product.name == product_name:
                return product
        return None

    def add_to_cart(self, product_id: str) -> bool:
        product = self.get_product_by_id(product_id)
        if product.stock > 0:  # Kiểm tra sản phẩm có tồn tại và còn hàng
            self.cart.add_item(product, 1)  # Thêm sản phẩm vào giỏ hàng
            return True
        return False  # Không thêm được (hết hàng hoặc không tìm thấy sản phẩm)


    def remove_from_cart(self, product_id: str) -> bool:
        """Xóa sản phẩm khỏi giỏ hàng theo ID."""
        product = self.get_product_by_id(product_id)
        if product in self.cart.items:  # Kiểm tra nếu sản phẩm có trong giỏ hàng
            self.cart.remove_item(product)  # Xóa sản phẩm khỏi giỏ hàng
            product.stock += 1  # Tăng lại số lượng tồn kho
            self.save_products()  # Lưu thay đổi tồn kho vào file
            return True
        return False  # Không xóa được (không tìm thấy sản phẩm trong giỏ hàng)

    def checkout(self) -> float: #Nằm trong giao diện
        if not self.cart.items:
            return 0  # Giỏ hàng trống, không thực hiện thanh toán
        total = self.cart.get_total()  # Tính tổng tiền
        if total > 0:
            # Lưu thông tin giỏ hàng vào file cart.json
            self.save_cart(total)
            # Xóa giỏ hàng sau khi thanh toán
            return total
        return 0

    def restock_product(self, product_id: str, quantity: int):
        """Thêm hàng cho sản phẩm theo ID."""
        product = self.get_product_by_id(product_id)
        if product:
            product.stock += quantity
            self.save_products()

    def get_stock(self, product_id: str) -> int:
        """Lấy số lượng tồn kho của sản phẩm."""
        product = self.get_product_by_id(product_id)
        return product.stock if product else 0
