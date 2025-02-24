from model.Cart import Product, Cart


class SmartMartFunctions:
    def __init__(self):
        self.products = [
            Product("Coca-Cola", "Beverages", 1.5, 10),
            Product("Pepsi", "Beverages", 1.5, 8),
            Product("Sandwich", "Fast Food", 3.0, 5),
            Product("Chips", "Snacks", 2.0, 15),
            Product("Toothpaste", "Personal Care", 4.0, 7),
        ]
        self.cart = Cart()

    def search_products(self, keyword):
        return [product for product in self.products if keyword.lower() in product.name.lower()]

    def add_to_cart(self, product_name):
        for product in self.products:
            if product.name == product_name:
                if product.stock > 0:
                    self.cart.add_item(product, 1)
                    return True
                else:
                    return False
        return False

    def remove_from_cart(self, product_name):
        for product in self.products:
            if product.name == product_name:
                self.cart.remove_item(product)
                return True
        return False

    def checkout(self):
        total = self.cart.get_total(self.products)
        self.cart.clear()
        return total