from datetime import datetime
import os

class Receipt:
    def __init__(self, order_id, items, total, payment_method, tax_rate=0.1):
        self.order_id = order_id
        self.items = items  # List of CartItems
        self.total = total
        self.payment_method = payment_method
        self.tax_rate = tax_rate
        self.timestamp = datetime.now()

    def get_tax_amount(self):
        return self.total * self.tax_rate

    def get_grand_total(self):
        return self.total + self.get_tax_amount()

    def generate_receipt_text(self):
        lines = []
        lines.append("=" * 40)
        lines.append(f"RECEIPT #{self.order_id}")
        lines.append(f"Date: {self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("=" * 40)

        # Add items
        lines.append(f"{'Item':<30}{'Qty':<5}{'Price':<10}")
        lines.append("-" * 40)
        for item in self.items:
            lines.append(f"{item.product.name:<30}{item.quantity:<5}{item.get_subtotal():>10.2f}")

        # Add totals
        lines.append("-" * 40)
        lines.append(f"{'Subtotal':<30}{'':<5}{self.total:>10.2f}")
        lines.append(f"{'Tax (' + str(int(self.tax_rate * 100)) + '%)':<30}{'':<5}{self.get_tax_amount():>10.2f}")
        lines.append(f"{'TOTAL':<30}{'':<5}{self.get_grand_total():>10.2f}")
        lines.append("-" * 40)
        lines.append(f"Payment Method: {self.payment_method}")
        lines.append("=" * 40)
        lines.append("Thank you for your purchase!")

        return "\n".join(lines)

    def save_to_file(self, directory="receipts"):
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = f"{directory}/receipt_{self.order_id}_{self.timestamp.strftime('%Y%m%d%H%M%S')}.txt"
        with open(filename, 'w') as f:
            f.write(self.generate_receipt_text())

        return filename