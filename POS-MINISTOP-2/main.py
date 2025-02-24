import sys
from PyQt6.QtWidgets import QApplication
from funtion import SmartMartFunctions
from UI import SmartMartUI


class SmartMartApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.functions = SmartMartFunctions()
        self.ui = SmartMartUI(self.functions)

    def save_data(self):
        self.functions.save_products()
        self.functions.save_cart()


def main():
    app = SmartMartApp(sys.argv)
    ret = app.exec()
    app.save_data()  # Save data before exiting
    sys.exit(ret)


if __name__ == "__main__":
    main()