from models.transactions import TransactionModel
from models.users_credentials import UserModel
from models.users_events import EventModel
from models.users_profiles import UserProfileModel


class EventService:

    @staticmethod
    def is_existed_by_name(email: str, name: str):
        result = EventModel.find_by_email_name(email, name)
        return False if len(result) == 0 else True

    @staticmethod
    def create(email: str, name: str, budget: float):
        EventModel.create(email, name, budget)

    @staticmethod
    def get_list(email: str):
        event_list = EventModel.find_all(email)
        events = []
        for event in event_list:
            events.append({
                "id": event["id"],
                "name": event["name"],
                "budget_percentage": round(event["spent"] / event["budget"] * 100, 2)
            })
        return events


    @staticmethod
    def is_existed_by_id(email: str, event_id : int):
        result = EventModel.find_by_email_id(email, event_id)
        return False if len(result) == 0 else True

    @staticmethod
    def get(email: str, event_id: int) -> list[dict]:
        return EventModel.find_by_email_id(email, event_id)

    @staticmethod
    def update(event_id: int, name: str, budget: float):
        EventModel.update(event_id, name, budget)

    @staticmethod
    def delete(id: int, email: str):
        login_id = UserModel.find_by_email(email)["id"]
        event_expense = EventService.get(email, id)[0]["spent"]
        EventModel.delete(id)
        UserProfileModel.decrease_spent(event_expense, login_id)

    @staticmethod
    def get_transactions(event_id: int)->list[dict]:
        result = TransactionModel.get_by_event(event_id)
        data = []
        for item in result:
            data.append({
                "id": item[0],
                "transaction": item[1],
                "mode": item[2],
                "datestamp": item[3],
                "category": item[4],
                "note": item[5]
            })
        return data