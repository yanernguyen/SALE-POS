import json
from typing import Optional


class Product:
    _next_id = 1  # Biến class quản lý ID

    def __init__(self, name: str, category: str, price: float,
                 stock: int, image: str = None, id: str = None):
        # Xử lý ID
        if id is None:
            self.id = f"SP_{Product._next_id:04d}"  # Format: SP_0001
            Product._next_id += 1
        else:
            self.id = id
            numeric_part = int(id.split('_')[1])
            if numeric_part >= Product._next_id:
                Product._next_id = numeric_part + 1

        # Các thuộc tính khác giữ nguyên
        self.name = name
        self.category = category
        self.price = price
        self.stock = stock
        self.image = image

    def __str__(self):
        return f"[{self.id}] {self.name} (${self.price}) - {self.stock} in stock"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "category": self.category,
            "image": self.image,
        }

    def is_valid(self) -> bool:
        return (
                isinstance(self.name, str) and self.name.strip() != "" and
                isinstance(self.category, str) and self.category.strip() != "" and
                self.price > 0 and
                self.stock >= 0
        )

    def update_price(self, new_price: float):
        if new_price > 0:
            self.price = new_price
            return self.price
        else:
            raise ValueError("Giá sản phẩm phải lớn hơn 0.")

    def update_stock(self, new_stock: int):
        if new_stock >= 0:
            self.stock = new_stock
            return self.stock
        else:
            raise ValueError("Số lượng tồn kho không được âm.")

    def update_image(self, new_image: str):
        if isinstance(new_image, str) and new_image.endswith(('.jpg', '.png', '.jpeg')):
            self.image = new_image
        else:
            raise ValueError("Hình ảnh phải là file có định dạng .jpg, .png hoặc .jpeg.")
