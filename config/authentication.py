from config.factory import LoginManagerFlask, AppFlask
from models.users_credentials import UserModel


class SessionUser:

    def __init__(self, id, email):
        self.id = id
        self.email = email

    def to_json(self):
        return {
            "email": self.email
        }

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)



