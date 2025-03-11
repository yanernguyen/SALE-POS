class Product:
    """
    Class representing a product in the vending machine
    """
    _id_counter = 1  # Class variable to keep track of the next available ID

    @classmethod
    def generate_id(cls, prefix="P"):
        """
        Generate a unique ID for a product

        Args:
            prefix (str): Prefix for the ID (default: "P")

        Returns:
            str: A unique ID in the format "P001", "P002", etc.
        """
        new_id = f"{prefix}{cls._id_counter:03d}"
        cls._id_counter += 1
        return new_id

    def __init__(self, name, price, category, description="", stock=10, image_path=None, id=None):
        """
        Initialize a new Product

        Args:
            name (str): Product name
            price (float): Product price
            category (str): Category ID
            description (str, optional): Product description. Defaults to "".
            stock (int, optional): Initial stock quantity. Defaults to 10.
            image_path (str, optional): Path to product image. Defaults to None.
            id (str, optional): Custom ID for the product. If None, an ID will be generated.
        """
        self.id = id if id is not None else self.generate_id()
        self.name = name
        self.price = price
        self.category = category
        self.description = description
        self.stock = stock
        self.image_path = image_path

    def decrease_stock(self, quantity=1):
        """Decrease stock by given quantity"""
        if self.stock >= quantity:
            self.stock -= quantity
            return True
        return False

    def increase_stock(self, quantity=1):
        """Increase stock by given quantity"""
        self.stock += quantity

    def to_dict(self):
        """Convert product to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "category": self.category,
            "description": self.description,
            "stock": self.stock,
            "image_path": self.image_path
        }

    @classmethod
    def from_dict(cls, data):
        """Create product from dictionary"""
        return cls(
            name=data["name"],
            price=data["price"],
            category=data["category"],
            description=data.get("description", ""),
            stock=data.get("stock", 10),
            image_path=data.get("image_path"),
            id=data["id"]
        )