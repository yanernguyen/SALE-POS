from CartItem import *

class ShoppingCart:
    """
    Class representing a shopping cart
    """

    def __init__(self):
        self.items = {}  # Dictionary of product_id: CartItem

    def add_item(self, product, quantity=1):
        """Add product to cart or increase quantity if already in cart"""
        if product.id in self.items:
            self.items[product.id].increase_quantity(quantity)
        else:
            self.items[product.id] = CartItem(product, quantity)

    def remove_item(self, product_id):
        """Remove item from cart completely"""
        if product_id in self.items:
            del self.items[product_id]
            return True
        return False

    def update_quantity(self, product_id, quantity):
        """Update quantity of an item in the cart"""
        if product_id in self.items:
            if quantity <= 0:
                return self.remove_item(product_id)
            self.items[product_id].quantity = quantity
            return True
        return False

    def clear(self):
        """Clear all items from cart"""
        self.items = {}

    def get_total(self):
        total = 0
        for item in self.items.values():
            total += item.get_subtotal()
        return total

    def get_item_count(self):
        count = 0
        for item in self.items.values():
            count += item.quantity
        return count

    def get_items(self):
        return list(self.items.values())
