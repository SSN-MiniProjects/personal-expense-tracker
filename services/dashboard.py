import datetime
import calendar
from models.transactions import TransactionModel
from models.users_credentials import UserModel
from models.users_profiles import UserProfileModel


class ExpenseSumType:
    DAY = 'DAY'
    MONTH = 'MONTH'
    YEAR = 'YEAR'


class GraphData:

    @staticmethod
    def get_daily(email: str, date: datetime.date):
        login_id = UserModel.find_by_email(email)["id"]
        result = TransactionModel.get_daily_expense(login_id, date)
        day_count = calendar.monthrange(date.year, date.month)[1]
        labels = list(range(1, day_count + 1))
        data = [0] * len(labels)
        for item in result:
            data[item["day"] - 1] = int(item["sum"])
        return {
            "labels": labels,
            "data": data
        }

    @staticmethod
    def get_monthly(email: str, date: datetime.date):
        login_id = UserModel.find_by_email(email)["id"]
        labels = list(calendar.month_abbr)[1:]
        data = [0] * len(labels)
        result = TransactionModel.get_monthly_expense(login_id, date)
        for item in result:
            data[item["month"] - 1] = int(item["sum"])
        return {
            "labels": labels,
            "data": data
        }


class PieChartData:

    @staticmethod
    def get_category(email: str, date: datetime.date):
        login_id = UserModel.find_by_email(email)["id"]
        result = TransactionModel.get_category_expense(login_id, date)
        labels = []
        data = []
        for item in result:
            labels.append(item["category"])
            data.append(int(item["sum"]))
        return {
            "labels": labels,
            "data": data
        }


class ExpenseSum:
    @staticmethod
    def get(email: str, date: datetime.date, expense_type: str):
        result = None
        login_id = UserModel.find_by_email(email)["id"]

        if expense_type == ExpenseSumType.DAY:
            result = TransactionModel.get_day_expense(login_id, date)
        elif expense_type == ExpenseSumType.MONTH:
            result = TransactionModel.get_month_expense(login_id, date)
        elif expense_type == ExpenseSumType.YEAR:
            result = TransactionModel.get_year_expense(login_id, date)

        return result[0][0] if result else 0


class DashboardService:

    @staticmethod
    def get_graph_data(email: str):
        current_date = datetime.date.today()
        return {
            "daily": GraphData.get_daily(email, current_date),
            "monthly": GraphData.get_monthly(email, current_date)
        }

    @staticmethod
    def get_pie_data(email: str):
        current_date = datetime.date.today()
        return {
            "category": PieChartData.get_category(email, current_date)
        }

    @staticmethod
    def get_card_data(email: str):
        current_date = datetime.date.today()
        result = UserProfileModel.get_spent_and_budget(email)
        budget_percentage = round(result["total_expense"] / result["budget"] * 100, 2) if result["budget"] > 0 else -1

        return {
            "expense": {
                "today": ExpenseSum.get(email, current_date, ExpenseSumType.DAY),
                "current_month": ExpenseSum.get(email, current_date, ExpenseSumType.MONTH),
                "current_year": ExpenseSum.get(email, current_date, ExpenseSumType.YEAR),
                "total": result["total_expense"]
            },
            "budget_percentage": budget_percentage,
            "user_count": UserModel.get_count()
        }
