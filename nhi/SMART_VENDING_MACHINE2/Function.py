import json
from typing import List
from Product import Product
from Cart import Cart

class SmartMartFunctions:
    def __init__(self):
        self.products: List[Product] = []
        self.cart = Cart()
        self.load_products()
        self.load_cart()

    '''def load_products(self):
        try:
            with open("data/products.json", "r") as file:
                products_data = json.load(file)
                self.products = {"Beverages": [], "Fast Food": [], "Snacks": [], "Personal Cares": []}
                for product_data in products_data:
                    category = product_data.get("category", "Beverages")
                    self.products[category].append(product_data)
        except FileNotFoundError:
            print("⚠️ Lỗi: Không tìm thấy file products.json.")
            self.products = {}'''

    def load_products(self):
        try:
            with open("data/products.json", "r") as file:
                products_data = json.load(file)
                self.products = {"Beverages": [], "Fast Food": [], "Snacks": [], "Personal Cares": []}
                for product_data in products_data:
                    product = Product(
                        name=product_data["name"],
                        category=product_data["category"],
                        price=product_data["price"],
                        stock=product_data["stock"],
                        image=product_data.get("image", "")
                    )
                    self.products[product.category].append(product)
                print("Dữ liệu sản phẩm đã tải:", self.products)  # In ra dữ liệu để kiểm tra
        except FileNotFoundError:
            print("⚠️ Lỗi: Không tìm thấy file products.json.")
            self.products = {}

    def save_products(self):
        with open("data/products.json", "w") as file:
            json.dump([product.__dict__ for product in self.products], file, indent=4)

    '''def save_products(self):
        products_data = []
        for category, products in self.products.items():
            for product in products:
                products_data.append(product.__dict__)
        with open("data/products.json", "w") as file:
            json.dump(products_data, file, indent=4)'''

    def load_cart(self):
        try:
            with open("data/cart.json", "r") as file:
                cart_data = json.load(file)
                self.cart.items = cart_data
        except FileNotFoundError:
            self.cart.items = {}

    def save_cart(self):
        with open("data/cart.json", "w") as file:
            json.dump(self.cart.items, file, indent=4)

    def get_product_prices(self) -> dict[str, float]:
        prices = {}
        for category, products in self.products.items():
            for product in products:
                prices[product.name] = product.price
        return prices

    def search_products(self, keyword: str) -> List[Product]:
        results = []
        for category, products in self.products.items():
            for product in products:
                if keyword.lower() in product.name.lower():
                    results.append(product)
        return results

    def filter_product(self, category):
        if category in self.products:
            return self.products[category]
        else:
            return []

    '''def get_product_category(self, product_name):
        for category, products in self.products.items():
            for product in products:
                if product["name"] == product_name:
                    return category
        return None'''

    def get_product_category(self, product_name):
        for category, products in self.products.items():
            for product in products:
                if product.name == product_name:
                    return category
        return None

    '''def add_to_cart(self, product_name):
        product = next((p for p in self.products if p.name == product_name), None)
        if product and product.stock > 0:
            self.cart.add_item(product_name, 1)  # Thêm 1 sản phẩm vào giỏ hàng
            product.stock -= 1  # Giảm số lượng tồn kho
            return True
        else:
            return False'''

    def add_to_cart(self, product_name):
        for category, products in self.products.items():
            for product in products:
                if product.name == product_name and product.stock > 0:
                    self.cart.add_item(product_name, 1)  # Thêm 1 sản phẩm vào giỏ hàng
                    product.stock -= 1  # Giảm số lượng tồn kho
                    return True
        return False

    '''def remove_from_cart(self, product_name: str) -> bool:
        if product_name in self.cart.items:
            quantity_removed = self.cart.items[product_name]
            self.cart.remove_item(product_name)

            for product in self.products:
                if product.name == product_name:
                    product.stock += quantity_removed
                    break

            self.save_cart()
            self.save_products()
            return True
        return False'''

    def remove_from_cart(self, product_name: str) -> bool:
        if product_name in self.cart.items:
            quantity_removed = self.cart.items[product_name]
            self.cart.remove_item(product_name)

            # Tìm sản phẩm và cập nhật lại tồn kho
            for category, products in self.products.items():
                for product in products:
                    if product.name == product_name:
                        product.stock += quantity_removed
                        self.save_products()  # Lưu lại thay đổi vào file products.json
                        return True
        return False

    '''def remove_from_cart(self, product_name: str) -> bool:
        if product_name in self.cart.items:
            quantity_removed = self.cart.items[product_name]
            self.cart.remove_item(product_name)

            # Tìm sản phẩm và cập nhật lại tồn kho
            for category, products in self.products.items():
                for product in products:
                    if product.name == product_name:
                        product.stock += quantity_removed
                        self.save_products()  # Lưu lại thay đổi vào file products.json
                        return True
        return False'''

    '''def update_cart_item(self, product_name: str, quantity: int) -> bool:
        if quantity <= 0:
            return self.remove_from_cart(product_name)

        for product in self.products:
            if product.name == product_name:
                if product.stock + self.cart.items.get(product_name, 0) >= quantity:
                    product.stock += self.cart.items.get(product_name, 0) - quantity
                    self.cart.update_item(product_name, quantity)
                    self.save_products()
                    return True
                else:
                    return False
        return False'''

    def update_cart_item(self, product_name: str, quantity: int) -> bool:
        if quantity <= 0:
            return self.remove_from_cart(product_name)

        for category, products in self.products.items():
            for product in products:
                if product.name == product_name:
                    current_quantity = self.cart.items.get(product_name, 0)
                    if product.stock + current_quantity >= quantity:
                        product.stock += current_quantity - quantity
                        self.cart.update_item(product_name, quantity)
                        self.save_products()
                        return True
                    else:
                        return False
        return False

    def checkout(self) -> float:
        if not self.cart.items:
            return -1

        total = self.cart.get_total(self.get_product_prices())
        self.cart.clear()
        self.save_cart()
        return total

