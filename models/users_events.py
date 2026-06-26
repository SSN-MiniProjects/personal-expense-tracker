from config.db import get_result, get_result_dict
from models.transactions import TransactionModel
from models.users_credentials import UserModel


class EventModel:

    @staticmethod
    def total_spent(login_id: int, event_id: int):
        event_spent = TransactionModel.get_sum_event_transactions(login_id, event_id)
        return event_spent

    @staticmethod
    def find_by_name(login_id: int, event_name: str):
        query = 'SELECT * from user_events where login_id=%s and name=%s'
        param = (login_id, event_name)
        res = get_result(query, param)
        return res

    @staticmethod
    def find_by_event_id(login_id: int, event_id: int) -> list:
        query = 'SELECT id, name, budget from user_events where id=%s and login_id=%s'
        param = (event_id, login_id)
        return get_result(query, param)

    @staticmethod
    def create(login_id: int, name: str, budget: float):
        name = name.strip()
        query = 'INSERT INTO user_events (login_id, name, budget ) VALUES (%s,%s,%s)'
        param = (login_id, name, budget)
        get_result(query, param)

    @staticmethod
    def find_all(login_id: int):
        query = 'SELECT id, name, budget from user_events where login_id=%s'
        param = (login_id,)
        result = get_result_dict(query, param)
        return [] if not result else result

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

    @staticmethod
    def get_name(event_id: int):
        query = 'select name from user_events where id=%s'
        param = (event_id,)
        return get_result(query, param)
