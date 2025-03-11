from ShoppingCart import ShoppingCart
from InventoryManager import *
from PaymentMethod import *
from Receipt import *
import uuid
from datetime import datetime

class VendingMachine:
    def __init__(self):
        self.cart = ShoppingCart()
        self.inventory = InventoryManager()
        self.payment_methods = {
            "cash": CashPayment(),
            "card": CardPayment()
        }
        self.transaction_history = []

    def add_to_cart(self, product_id, quantity=1):
        product = self.inventory.get_product(product_id)
        if product and product.stock >= quantity:
            self.cart.add_item(product, quantity)
            return True
        return False

    def has_item(self, product_id):
        return product_id in self.cart

    def remove_from_cart(self, product_id):
        return self.cart.remove_item(product_id)

    def update_cart_quantity(self, product_id, quantity):
        return self.cart.update_quantity(product_id, quantity)

    def clear_cart(self):
        self.cart.clear()

    def checkout(self, payment_method_key):
        if not self.cart.items:
            return False, "Cart is empty"

        payment_method = self.payment_methods.get(payment_method_key)
        if not payment_method:
            return False, "Invalid payment method"

        # Calculate total with tax
        tax_rate = 0.1  # 10% tax
        total = self.cart.get_total()
        grand_total = total + (total * tax_rate)

        # Process payment
        payment_success = payment_method.process_payment(grand_total)
        if not payment_success:
            return False, "Payment failed"

        # Update inventory
        for item in self.cart.get_items():
            item.product.decrease_stock(item.quantity)

        # Generate receipt
        order_id = str(uuid.uuid4())[:8]
        receipt = Receipt(
            order_id=order_id,
            items=self.cart.get_items(),
            total=total,
            payment_method=payment_method.get_payment_type(),
            tax_rate=tax_rate
        )

        # Save receipt
        receipt_file = receipt.save_to_file()

        # Add to transaction history
        self.transaction_history.append({
            "order_id": order_id,
            "timestamp": datetime.now().isoformat(),
            "total": grand_total,
            "item_count": self.cart.get_item_count(),
            "payment_method": payment_method.get_payment_type()
        })

        # Clear cart
        self.cart.clear()

        # Save updated inventory
        self.inventory.save_data()

        return True, {
            "receipt": receipt.generate_receipt_text(),
            "receipt_file": receipt_file,
            "order_id": order_id
        }

    def get_all_categories(self):
        return list(self.inventory.categories.values())

    def get_products_by_category(self, category_id):
        return self.inventory.get_products_by_category(category_id)

    def search_products(self, query):
        return self.inventory.search_products(query)

