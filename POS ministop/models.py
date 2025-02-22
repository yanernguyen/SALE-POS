# models.py
class Item:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item, quantity):
        self.items.append((item, quantity))

    def remove_item(self, item_name):
        self.items = [item for item in self.items if item[0].name != item_name]

    def calculate_total(self):
        return sum(item.price * quantity for item, quantity in self.items)

    def display_cart(self):
        cart_details = "Items in Cart:\n"
        for item, quantity in self.items:
            cart_details += f"{item.name}: {quantity} x ${item.price:.2f} = ${item.price * quantity:.2f}\n"
        cart_details += f"\nTotal: ${self.calculate_total():.2f}"
        return cart_details
