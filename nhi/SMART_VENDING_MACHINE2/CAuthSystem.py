from CSecurity import *

class AuthSystem:
    def __init__(self):
        self.admin_users = {}  # Load từ database/file

    def admin_login_flow(self, username: str, password: str) -> bool:
        """Toàn bộ quy trình đăng nhập admin"""
        if admin_data := self.admin_users.get(username):
            return (
                    AdminSecurity.verify_login(password, admin_data)
                    and AdminSecurity.check_password_expiry(admin_data)
            )
        return False
