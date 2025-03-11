from CAuthSystem import *
from datetime import datetime, timedelta
from CSecurity import *

class Admin:
    def __init__(self, adname: str, creds_data: dict):
        self.adname = adname
        self.metadata = {
            'last_login': None,
            'failed_attempts': 0,
            'last_updated': datetime.now().isoformat()
        }
        self.credentials = creds_data  # Chứa salt/hash

    def update_password(self, new_password: str):
        """Cập nhật mật khẩu mới với salt mới"""
        new_salt = os.urandom(16)
        combined = new_password.encode() + new_salt + AdminSecurity._pepper
        self.credentials = {
            'salt': new_salt.hex(),
            'hash': bcrypt.hashpw(combined, bcrypt.gensalt()).decode()
        }
        self.metadata['last_updated'] = datetime.now().isoformat()
