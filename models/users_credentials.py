from config.db import get_result, get_result_dict


class UserModel:
    @staticmethod
    def create(email: str, password: str):
        query = 'INSERT INTO user_credentials (email, password) VALUES (%s, %s)'
        param = (email, password)
        get_result(query, param)

    @staticmethod
    def find_by_id(user_id: int):
        query = 'SELECT * FROM user_credentials WHERE id = %s'
        param = (user_id,)
        res = get_result(query, param)
        if res:
            res = res[0]
            return {
                "id": res[0],
                "email": res[1],
                "password": res[2]
            }
        return res

    @staticmethod
    def find_by_email(email: str):
        query = 'SELECT * FROM user_credentials WHERE email = %s'
        param = (email,)
        res = get_result(query, param)
        if res:
            res = res[0]
            return {
                "id": res[0],
                "email": res[1],
                "password": res[2]
            }
        return res

    @staticmethod
    def get_count():
        query = 'SELECT count(email) FROM user_credentials'
        result = get_result_dict(query)
        return result[0]["count"]
