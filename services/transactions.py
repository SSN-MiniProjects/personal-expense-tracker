from models.transactions import TransactionModel
from models.users_credentials import UserModel
from models.users_events import EventModel
from models.users_profiles import UserProfileModel


def add_spent(event: int, amount: float):
    if event is not None:
        EventModel.increase_spent(amount, event)


def remove_spent(event: int, amount: float):
    if event is not None:
        EventModel.decrease_spent(amount, event)


class TransactionService:

    @staticmethod
    def get_by_email_id(user_email: str, transaction_id: int):
        login_id = UserModel.find_by_email(user_email)["id"]
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
    def is_existed_by_id(email: str, transaction_id: int):
        result = TransactionService.get_by_email_id(email, transaction_id)
        return False if len(result) == 0 else True

    @staticmethod
    def create(user_email, amount, mode, category, datestamp, note, event):
        login_id = UserModel.find_by_email(user_email)["id"]
        TransactionModel.create(login_id, amount, mode, category, datestamp, note, event)
        UserProfileModel.increase_spent(amount, login_id)
        if event is not None:
            EventModel.increase_spent(amount, event)

    @staticmethod
    def get_by_email(user_email: str):
        login_id = UserModel.find_by_email(user_email)["id"]
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
    def delete(email: str, transaction_id: int):
        login_id = UserModel.find_by_email(email)["id"]
        data = TransactionModel.get_event_amount(transaction_id)
        amount = data["amount"]
        event_id = data["event_id"]
        UserProfileModel.decrease_spent(amount, login_id)
        if event_id is not None:
            EventModel.decrease_spent(amount, event_id)
        TransactionModel.delete(transaction_id)

    @staticmethod
    def update(transaction_id, email, amount, mode, category, datestamp, note, event):
        login_id = UserModel.find_by_email(email)["id"]
        data = TransactionModel.get_event_amount(transaction_id)
        previous_amount = data["amount"]
        previous_event_id = data["event_id"]

        if previous_event_id != event:
            remove_spent(previous_event_id, previous_amount)
            add_spent(event, amount)

        else:
            diff = amount - previous_amount
            if diff < 0:
                UserProfileModel.decrease_spent(diff, login_id)
                remove_spent(previous_event_id, diff)
            else:
                UserProfileModel.increase_spent(diff, login_id)
                add_spent(previous_event_id, diff)

        TransactionModel.update(transaction_id, amount, mode, category, datestamp, note, event)
