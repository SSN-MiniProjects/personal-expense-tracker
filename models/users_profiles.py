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
        result = get_result(query, param).fetchone()
        if result is not None:
            return {
                "name": result[0],
                "budget": result[1],
                "phone": result[2],
                "profession": result[3],
                "alert": result[4]
            }

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
        result = get_result(query, param).fetchone()
        if result is not None:
            return {
                "total_expense": result[0],
                "budget": result[1]
            }
        return result
