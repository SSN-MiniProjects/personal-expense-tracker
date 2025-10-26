from models.transactions import TransactionModel
from models.users_credentials import UserModel
from models.users_events import EventModel
from models.users_profiles import UserProfileModel


class TransactionService:

    @staticmethod
    def get_by_id(login_id: int, transaction_id: int):
        result = TransactionModel.get(login_id, transaction_id)
        data = []
        for item in result:
            data.append({
                "id": item[0],
                "transaction": item[1],
                "mode": item[2],
                "datestamp": item[3],
                "category": item[4],
                "event": item[5],
                "note": item[6]
            })
        return data

    @staticmethod
    def is_existed_by_id(login_id: int, transaction_id: int):
        result = TransactionService.get_by_id(login_id, transaction_id)
        return False if len(result) == 0 else True

    @staticmethod
    def create(login_id, amount, mode, category, datestamp, note, event):
        TransactionModel.create(login_id, amount, mode, category, datestamp, note, event)

    @staticmethod
    def get_by_login_id(login_id: int):
        result = TransactionModel.get_all(login_id)
        data = []
        for item in result:
            event_id = item[6]
            event_names = EventModel.get_name(event_id)
            event_name = event_names[0][0] if event_names else None

            data.append({
                "id": item[0],
                "transaction": float(item[1]),
                "mode": item[2],
                "datestamp": item[3],
                "note": item[4],
                "category": item[5],
                "event": event_name
            })
        return data

    @staticmethod
    def delete(transaction_id: int):
        TransactionModel.delete(transaction_id)

    @staticmethod
    def update(transaction_id, amount, mode, category, datestamp, note, event):
        TransactionModel.update(transaction_id, amount, mode, category, datestamp, note, event)

    @staticmethod
    def get_user_spent(login_id: int):
        result = TransactionModel.get_sum_transactions(login_id)
        if result:
            return result[0][1]
        return 0