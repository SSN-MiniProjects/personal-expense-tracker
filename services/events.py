from models.users_events import EventModel


class EventService:

    @staticmethod
    def is_existed(email: str, name: str):
        return EventModel.find_by_email_name(email, name)

    @staticmethod
    def create(email: str, name: str, budget: float):
        EventModel.create(email, name, budget)

    @staticmethod
    def get_event_list(email: str):
        event_list = EventModel.find_all(email)
        events = []
        for event in event_list:
            events.append({
                "id": event["id"],
                "name": event["name"],
                "budget_percentage": round(event["spent"] / event["budget"] * 100, 2)
            })
        return events
