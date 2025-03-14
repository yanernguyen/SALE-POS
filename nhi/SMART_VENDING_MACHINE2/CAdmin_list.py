from Cadmin import *
import random
import string
import json
import os

class AdminList:
    FILE_PATH = "data/admin_data.json"

    def __init__(self):
        self.admins = []
        self.load_admins()

    def load_admins(self):
        """Tải danh sách admin từ file JSON"""
        if os.path.exists(self.FILE_PATH):
            with open(self.FILE_PATH, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.admins = [Admin(**admin) for admin in data]

    def save_admins(self):
        """Lưu danh sách admin vào file JSON"""
        with open(self.FILE_PATH, "w", encoding="utf-8") as file:
            json.dump([admin.to_dict() for admin in self.admins], file, indent=4)

    def add_admin(self, username: str, password: str):
        """Thêm admin mới"""
        if self.get_admin(username):
            print("Admin đã tồn tại!")
            return False
        self.admins.append(Admin(username, password))
        self.save_admins()
        return True

    def get_admin(self, username: str):
        """Tìm admin theo username"""
        return next((admin for admin in self.admins if admin.username == username), None)

    def check_login(self, username, password):
        """Kiểm tra đăng nhập từ JSON"""
        for admin in self.admins:
            if admin.username == username and admin.password == password:  # Đúng cách truy cập
                return True
                """ Đăng nhập thành công"""
        return False
        """ Sai tài khoản hoặc mật khẩu"""

""" Test thử"""
if __name__ == "__main__":
    admin_list = AdminList()

    """ Thêm admin mới"""
    admin_list.add_admin("admin1", "123456")
    admin_list.add_admin("admin2", "password")

    """ Kiểm tra đăng nhập"""
    print(admin_list.login("admin1", "123456"))  # True
    print(admin_list.login("admin2", "wrongpass"))  # False