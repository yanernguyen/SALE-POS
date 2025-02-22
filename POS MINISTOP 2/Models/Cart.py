class Cart:
    def __init__(self):
        self.items = []

    def add_item(self, item, quantity=1):
        for i, (cart_item, qty) in enumerate(self.items):
            if cart_item.name == item.name:
                self.items[i] = (cart_item, qty + quantity)
                return
        self.items.append((item, quantity))

    def remove_item(self, item_name):
        self.items = [item for item in self.items if item[0].name != item_name]

    def calculate_total(self):
        return sum(item.price * quantity for item, quantity in self.items)

    def display_cart(self):
        cart_details = "\nItems in Cart:\n"
        for item, quantity in self.items:
            cart_details += f"{item.name}: {quantity} x ${item.price:.2f} = ${item.price * quantity:.2f}\n"
        cart_details += f"Total: ${self.calculate_total():.2f}"
        return cart_details