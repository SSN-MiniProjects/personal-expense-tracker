from models.transactions import TransactionModel
from models.users_credentials import UserModel
from models.users_events import EventModel
from models.users_profiles import UserProfileModel
from utilities.common import CommonUtils


class EventService:

    @staticmethod
    def is_existed_by_name(login_id: int, name: str):
        result = EventModel.find_by_name(login_id, name)
        return False if len(result) == 0 else True

    @staticmethod
    def create(login_id: int, name: str, budget: float):
        EventModel.create(login_id, name, budget)

    @staticmethod
    def get_list(login_id: int):
        events = EventModel.find_all(login_id)
        return events

    @staticmethod
    def get_budget_percentage(login_id: int, event_id: int, budget: int):
        event_spent = EventModel.total_spent(login_id, event_id)
        return CommonUtils.calculate_budget_percentage(event_spent, budget)

    @staticmethod
    def is_existed_by_id(login_id: int, event_id: int):
        result = EventService.get(login_id, event_id)
        return False if len(result) == 0 else True

    @staticmethod
    def get(login_id: int, event_id: int) -> list[dict]:
        result = EventModel.find_by_event_id(login_id, event_id)
        data = []
        for item in result:
            data.append({
                "id": item[0],
                "name": item[1],
                "budget": item[2],
                "spent": EventModel.total_spent(login_id, event_id)
            })
        return data


    @staticmethod
    def update(event_id: int, name: str, budget: float):
        EventModel.update(event_id, name, budget)

    @staticmethod
    def delete(id: int):
        EventModel.delete(id)

    @staticmethod
    def get_transactions(event_id: int) -> list[dict]:
        result = TransactionModel.get_by_event(event_id)
        return result