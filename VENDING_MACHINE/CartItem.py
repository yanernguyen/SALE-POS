class CartItem:
    """
    Class representing an item in the shopping cart
    """
    def __init__(self, product, quantity=1):
        self.product = product
        self.quantity = quantity
        
    def increase_quantity(self, amount=1):
        """Increase quantity of this item"""
        self.quantity += amount
        
    def decrease_quantity(self, amount=1):
        """Decrease quantity of this item"""
        if self.quantity > amount:
            self.quantity -= amount
            return True
        return False
        
    @property
    def subtotal(self):
        """Calculate subtotal for this item"""
        return self.product.price * self.quantity
