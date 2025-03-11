from Product import Product
import json
import os
from Category import *
from Item import *


class InventoryManager:
    def __init__(self, data_file="inventory.json"):
        self.products = {}  # Dictionary of product_id: Product
        self.categories = {}  # Dictionary of category_id: Category
        self.data_file = data_file
        self.load_data()

    def add_product(self, product):
        self.products[product.id] = product

    def remove_product(self, product_id):
        if product_id in self.products:
            del self.products[product_id]
            return True
        return False

    def get_product(self, product_id):
        return self.products.get(product_id)

    def add_category(self, category):
        self.categories[category.id] = category

    def remove_category(self, category_id):
        if category_id in self.categories:
            del self.categories[category_id]
            return True
        return False

    def get_category(self, category_id):
        return self.categories.get(category_id)

    def get_products_by_category(self, category):
        category = category.strip().lower()  # Chuẩn hóa chuỗi category
        return [
            product for product in self.products.values()
            if product.category.strip().lower() == category
        ]

    def search_products(self, query):
        query = query.lower()
        result = []
        for product in self.products.values():
            if (query in product.name.lower() or
                    (product.description and query in product.description.lower())):
                result.append(product)
        return result

    def save_data(self):
        data = {
            "products": [p.to_dict() for p in self.products.values()],
            "categories": [c.to_dict() for c in self.categories.values()]
        }

        with open(self.data_file, 'w') as f:
            json.dump(data, f, indent=2)

    import json

    def load_products_from_json(self, file_path):
        """Tải danh sách sản phẩm từ file JSON."""
        try:
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

                # Kiểm tra xem file JSON có chứa danh sách "products" không
                if "products" not in data:
                    raise ValueError("File JSON không có danh sách 'products'!")

                # Chuyển dữ liệu JSON thành danh sách đối tượng Product
                self.products = []
                for item in data["products"]:
                    try:
                        # Kiểm tra xem các trường bắt buộc có tồn tại không
                        required_fields = ["id", "name", "price", "category"]
                        for field in required_fields:
                            if field not in item:
                                raise ValueError(f"Thiếu trường bắt buộc '{field}' trong sản phẩm!")

                        # Tạo đối tượng Product từ dữ liệu JSON
                        product = Product(
                            id=item["id"],
                            name=item["name"],
                            price=item["price"],
                            category=item["category"],
                            description=item.get("description", ""),  # Trường không bắt buộc
                            stock=item.get("stock", 0),  # Trường không bắt buộc, mặc định là 0
                            image_path=item.get("image")  # Trường không bắt buộc
                        )
                        self.products.append(product)
                    except Exception as e:
                        print(f"Lỗi khi tạo sản phẩm từ dữ liệu JSON: {e}")
                        continue

                print(f"Đã tải {len(self.products)} sản phẩm từ {file_path}")

        except FileNotFoundError:
            print(f"Lỗi: Không tìm thấy file {file_path}")
        except json.JSONDecodeError:
            print(f"Lỗi: File {file_path} không phải là JSON hợp lệ!")
        except ValueError as ve:
            print(f"Lỗi dữ liệu: {ve}")
        except Exception as e:
            print(f"Lỗi không xác định: {e}")





