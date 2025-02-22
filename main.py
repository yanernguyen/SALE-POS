# Solution 1: A basic console-based POS system
# This solution provides a simple text-based POS system where the user can input item details and process a sale.

class Item:
    def __init__(self, name, price):
        self.name = name  # Name of the item
        self.price = price  # Price of the item

class Cart:
    def __init__(self):
        self.items = []  # List to store items added to the cart

    def add_item(self, item, quantity):
        # Adds item to the cart with specified quantity
        self.items.append((item, quantity))

    def remove_item(self, item_name):
        # Removes item from the cart based on item name
        self.items = [item for item in self.items if item[0].name != item_name]

    def calculate_total(self):
        # Calculates the total price of all items in the cart
        return sum(item.price * quantity for item, quantity in self.items)  # Fixed item.price reference

    def display_cart(self):
        # Displays the cart details
        print("\nItems in Cart:")
        for item, quantity in self.items:
            print(f"{item.name}: {quantity} x ${item.price:.2f} = ${item.price * quantity:.2f}")
        print(f"Total: ${self.calculate_total():.2f}")

class POSSystem:
    def __init__(self):
        self.cart = Cart()  # Initialize the cart

    def add_item_to_cart(self):
        # Allows user to add an item to the cart
        name = input("Enter item name: ")
        price = float(input(f"Enter price of {name}: $"))
        quantity = int(input(f"Enter quantity of {name}: "))
        item = Item(name, price)
        self.cart.add_item(item, quantity)
        print(f"Added {quantity} x {name} to cart.")

    def remove_item_from_cart(self):
        # Allows user to remove an item from the cart
        item_name = input("Enter item name to remove: ")
        self.cart.remove_item(item_name)
        print(f"Removed {item_name} from cart.")

    def process_payment(self):
        # Handles payment processing and generates a receipt
        self.cart.display_cart()
        payment_method = input("Select payment method (cash/credit): ")
        total_amount = self.cart.calculate_total()
        print(f"Payment of ${total_amount:.2f} made using {payment_method}. Thank you for your purchase!")

    def run(self):
        # Main function to run the POS system
        while True:
            print("\nPOS System")
            print("1. Add Item to Cart")
            print("2. Remove Item from Cart")
            print("3. Process Payment")
            print("4. Exit")

            choice = input("Choose an option: ")
            if choice == '1':
                self.add_item_to_cart()
            elif choice == '2':
                self.remove_item_from_cart()
            elif choice == '3':
                self.process_payment()
                break
            elif choice == '4':
                print("Exiting POS System.")
                break
            else:
                print("Invalid option. Try again.")

# Run the POS system
pos = POSSystem()
pos.run()