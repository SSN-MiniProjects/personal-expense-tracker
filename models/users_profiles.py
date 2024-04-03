from config.db import (
    get_result
)

from models.users_credentials import (
    UserModel
)


class UserProfileModel:

    @staticmethod
    def find_by_email(email:str):
        login_id = UserModel.find_by_email(email)["id"]
        query = 'SELECT name, budget, phone, profession, alert from user_profiles WHERE login_id = %s'
        param = (login_id,)
        result = get_result(query, param)
        return result

    @staticmethod
    def create(login_id:int):
        query = 'INSERT INTO user_profiles (login_id) VALUES (%s)'
        param = (login_id,)
        get_result(query, param)


    @staticmethod
    def update(email, name, budget, phone, profession, alert):
        login_id = UserModel.find_by_email(email)["id"]
        query = 'UPDATE user_profiles set name=%s, budget=%s, phone=%s, profession=%s, alert=%s where login_id=%s'
        param = (name, budget, phone, profession, alert, login_id)
        get_result(query, param)

    @staticmethod
    def get_spent_and_budget(email):
        login_id = UserModel.find_by_email(email)["id"]
        query = 'SELECT total_spent, budget FROM user_profiles WHERE login_id = %s'
        param = (login_id,)
        result = get_result(query, param)
        if result:
            result = result[0]
            return {
                "total_expense": result[0],
                "budget": result[1]
            }
        return result

    @staticmethod
    def increase_spent(amount: float, login_id: int):
        query = 'update user_profiles set total_spent=total_spent+%s where login_id=%s;'
        param = (amount, login_id,)
        get_result(query, param)

    @staticmethod
    def decrease_spent(amount: float, login_id: int):
        query = 'update user_profiles set total_spent=total_spent-%s where login_id=%s;'
        param = (amount, login_id,)
        get_result(query, param)
