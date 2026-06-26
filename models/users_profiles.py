from config.db import get_result_dict


class UserProfileModel:

    @staticmethod
    def find_by_login_id(login_id: int):
        query = 'SELECT name, budget, phone, profession, alert from user_profiles WHERE login_id = %s'
        param = (login_id,)
        result = get_result_dict(query, param)
        return result[0]

    @staticmethod
    def create(login_id:int):
        query = 'INSERT INTO user_profiles (login_id) VALUES (%s)'
        param = (login_id,)
        get_result_dict(query, param)


    @staticmethod
    def update(login_id, name, budget, phone, profession, alert):
        query = 'UPDATE user_profiles set name=%s, budget=%s, phone=%s, profession=%s, alert=%s where login_id=%s'
        param = (name, budget, phone, profession, alert, login_id)
        get_result_dict(query, param)

    @staticmethod
    def get_budget(login_id: int):
        query = 'SELECT budget FROM user_profiles WHERE login_id = %s'
        param = (login_id,)
        result =  get_result_dict(query, param)
        return result[0]["budget"]
