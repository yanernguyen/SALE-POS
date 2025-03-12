from Product import *
from typing import List, Optional

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