import hashlib

import phonenumbers
from wtforms.validators import StopValidation, ValidationError

from models.users_credentials import UserModel
from models.users_profiles import UserProfileModel


class UserService:

    @staticmethod
    def register(email: str, password: str):
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        UserModel.create(email, hashed_password)
        login_id = UserModel.find_by_email(email)["id"]
        UserProfileModel.create(login_id)

    @staticmethod
    def is_existed(email: str):
        return True if UserModel.find_by_email(email) else False

    @staticmethod
    def get(email: str):
        return UserModel.find_by_email(email)

    @staticmethod
    def validate_password(email: str, password: str):
        hashed_password = hashlib.sha256(password.encode('utf-8')).hexdigest()
        user = UserModel.find_by_email(email)
        return user["password"] == hashed_password


class UserProfileService:

    @staticmethod
    def get(login_id: int):
        return UserProfileModel.find_by_login_id(login_id)

    @staticmethod
    def update(login_id, name, budget, phone, profession, alert):
        return UserProfileModel.update(login_id, name, budget, phone, profession, alert)

    @staticmethod
    def is_valid_phone(phone_number: str):
        try:
            p = phonenumbers.parse(phone_number)
            if phonenumbers.is_valid_number(p):
                return True
        except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
            pass
        return False
