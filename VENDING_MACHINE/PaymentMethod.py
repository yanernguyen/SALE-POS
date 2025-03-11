class CashPayment:
    def process_payment(self, amount):
        # In a real implementation, this would interact with cash handling hardware
        print(f"Processing cash payment of {amount:.2f}")
        return True

    def get_payment_type(self):
        return "Cash"


class CardPayment:
    def process_payment(self, amount):
        # In a real implementation, this would interact with a card reader
        print(f"Processing card payment of {amount:.2f}")
        return True

    def get_payment_type(self):
        return "Card"