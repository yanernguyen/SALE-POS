import bcrypt
import os
from datetime import datetime, timedelta

class AdminSecurity:
    _pepper = os.getenv('PEPPER_SECRET', 'default_pepper_value').encode()  # Load từ biến môi trường

    @classmethod
    def verify_login(cls, input_password: str, stored_creds: dict) -> bool:
        """Xác thực mật khẩu admin với cơ chế salt+pepper"""
        try:
            salt = bytes.fromhex(stored_creds['salt'])
            hashed_password = stored_creds['hash'].encode()
            combined = input_password.encode() + salt + cls._pepper
            return bcrypt.checkpw(combined, hashed_password)
        except Exception as e:
            """ Log lỗi nếu cần"""
            return False

    @staticmethod
    def check_password_expiry(admin_data: dict) -> bool:
        """Kiểm tra hạn sử dụng mật khẩu (90 ngày)"""
        try:
            last_updated = datetime.fromisoformat(admin_data['last_updated'])
            return datetime.now() < (last_updated + timedelta(days=90))
        except (KeyError, ValueError):
            return False

class SecurityLogger:
    @staticmethod
    def log_failed_attempt(username: str, ip: str):
        entry = f"[{datetime.now()}] Failed login: {username} from {ip}"
        try:
            with open('security.log', 'a') as f:
                f.write(entry + "\n")
        except IOError as e:
            print(f"Error writing to log: {e}")
