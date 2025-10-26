from config.factory import LoginManagerFlask, AppFlask
from models.users_credentials import UserModel


class SessionUser:

    def __init__(self, email, login_id):
        self.email = email
        self.login_id = login_id

    def to_json(self):
        return {
            "email": self.email,
            "login_id": self.login_id,
        }

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_login_id(self):
        return str(self.login_id)



