from factory import LoginManagerFlask, AppFlask

app = AppFlask().instance
login_manager = LoginManagerFlask().instance
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = "error"


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


@login_manager.user_loader
def load_user(id):
    user = get_user_by_id(id)
    if user is None:
        return None
    usr_obj = SessionUser(user["id"], user["email"])
    return usr_obj
