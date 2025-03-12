
class Admin:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password  # Mật khẩu ở đây có thể mã hóa nếu cần

    def to_dict(self):
        """Chuyển đối tượng Admin thành dictionary để lưu vào JSON"""
        return {"username": self.username, "password": self.password}


