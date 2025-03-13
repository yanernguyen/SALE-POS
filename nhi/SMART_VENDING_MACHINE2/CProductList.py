from Product import *
from typing import List, Optional
from datetime import datetime

class ProductList:
    def __init__(self):
        self.products = self.load_products()



    def load_products(self) -> List[Product]:
        products = []
        try:
            with open("data/products.json", "r") as file:
                products_data = json.load(file)

                for data in products_data:
                    product = Product(
                        id=data["id"],
                        name=data["name"],
                        price=data["price"],
                        stock=data["stock"],
                        category=data["category"],
                        image=data["image"]
                    )
                    products.append(product)  # Chuyển đổi dữ liệu JSON thành đối tượng Product
        except FileNotFoundError:
            print("⚠️ Lỗi: Không tìm thấy file products.json.")
        return products

    def save_products(self):
        try:
            with open("data/products.json", "w") as file:
                json.dump([product.to_dict() for product in self.products], file, indent=4)
        except Exception as e:
            print(f"⚠️ Lỗi khi lưu file products.json: {e}")

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

    def reduce_stock(self, product_id: str, quantity: int):
        product = self.get_product_by_id(product_id)
        if product:
            if product.stock >= quantity:
                product.stock -= quantity
                return True  # Giảm stock thành công
            else:
                return False  # Không đủ hàng trong kho
        return None

    # def reduce_stock(self, product_id: str, quantity: int):
    #     product = self.get_product_by_id(product_id)
    #     if product:
    #         print(f"Trước khi trừ stock: {product.name} - {product.stock}")
    #         if product.stock >= quantity:
    #             product.stock -= quantity
    #             print(f"Sau khi trừ stock: {product.name} - {product.stock}")
    #             return True  # Giảm stock thành công
    #         else:
    #             print(f"Lỗi: Không đủ hàng! Stock hiện tại: {product.stock}, cần: {quantity}")
    #             return False  # Không đủ hàng
    #     print(f"Lỗi: Không tìm thấy sản phẩm {product_id}")
    #     return None

    def update_product_stock(self, product_id: str, quantity: int, admin_name: str):
        """Cập nhật số lượng sản phẩm và ghi vào lịch sử nhập hàng."""
        product = self.get_product_by_id(product_id)
        if product:
            product.stock += quantity
            self.save_products()
            self.log_update("Cập nhật số lượng", product, admin_name, quantity)
            return True
        return False



    #Thao tác manager
    # def add_product(self, product: Product, admin_name: str):
    #     """Thêm sản phẩm vào danh sách.""" #KHÔNG DÙNG
    #     self.products.append(product)
    #     self.save_products()
    #     self.log_update("Thêm sản phẩm mới", product, admin_name)



    # def remove_product(self, product_id: str, admin_name: str):
    #     """Xóa sản phẩm khỏi danh sách."""  #KHÔNG DÙNG
    #     product = self.get_product_by_id(product_id)
    #     if product:
    #         self.products.remove(product)
    #         self.save_products()
    #         self.log_update("Xóa sản phẩm", product, admin_name)
    #         return True
    #     return False

    def log_update(self, action: str, product: Product, admin_name: str, quantity: int = None):
        """Ghi lịch sử nhập hàng."""
        log_entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "admin": admin_name,
            "action": action,
            "product_id": product.id,
            "product_name": product.name,
            "quantity": quantity if quantity is not None else "-",
        }
        try:
            with open("data/history.json", "r",encoding="utf-8") as file:
                history = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            history = []

        history.append(log_entry)

        with open("data/history.json", "w",encoding="utf-8") as file:
            json.dump(history, file,ensure_ascii=False, indent=4)