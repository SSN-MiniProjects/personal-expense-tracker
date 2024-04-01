from config.db import get_result
from models.users_credentials import UserModel


class EventModel:

    @staticmethod
    def find_by_email_name(email: str, event_name: str):
        login_id = UserModel.find_by_email(email)["id"]
        query = 'SELECT * from user_events where login_id=%s and name=%s'
        param = (login_id, event_name)
        res = get_result(query, param)
        return res.fetchone()

    @staticmethod
    def find_by_email_id(email: str, event_id: int):
        login_id = UserModel.find_by_email(email)["id"]
        query = 'SELECT id, name, budget, spent from user_events where id=%s and login_id=%s'
        param = (event_id, login_id)
        result = get_result(query, param).fetchall()
        data = []
        for item in result:
            data.append({
                "id": item[0],
                "name": item[1],
                "budget": item[2],
                "spent": item[3],
            })
        return data

    @staticmethod
    def create(email: str, name: str, budget: float):
        login_id = UserModel.find_by_email(email)["id"]
        name = name.strip()
        query = 'INSERT INTO user_events (login_id, name, budget ) VALUES (%s,%s,%s)'
        param = (login_id, name, budget)
        get_result(query, param)

    @staticmethod
    def find_all(email: str):
        login_id = UserModel.find_by_email(email)["id"]
        query = 'SELECT id, name,budget,spent from user_events where login_id=%s'
        param = (login_id,)
        result = get_result(query, param)
        data = []
        for item in result:
            data.append({
                "id": item[0],
                "name": item[1],
                "budget": item[2],
                "spent": item[3],
            })
        return data

    @staticmethod
    def update(event_id: int, name: str, budget: float):
        name = name.strip()
        query = 'update user_events set name=%s,budget=%s where id=%s'
        param = (name, budget, event_id)
        get_result(query, param)

    @staticmethod
    def delete(event_id: int):
        query = 'delete from user_events where id=%s'
        param = (event_id,)
        get_result(query, param)

        # delete the transactions having this event id
        query = 'delete from user_transactions where event_id=%s'
        param = (event_id,)
        cursor.execute(query, param)

