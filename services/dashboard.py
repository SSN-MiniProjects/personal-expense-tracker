import datetime
import calendar
from models.transactions import TransactionModel
from models.users_credentials import UserModel
from models.users_profiles import UserProfileModel
from services.transactions import TransactionService
from utilities.common import CommonUtils


class ExpenseSumType:
    DAY = 'DAY'
    MONTH = 'MONTH'
    YEAR = 'YEAR'


class GraphData:

    @staticmethod
    def get_daily(login_id: int, date: datetime.date):
        result = TransactionModel.get_daily_expense(login_id, date)
        day_count = calendar.monthrange(date.year, date.month)[1]
        labels = list(range(1, day_count + 1))
        data = [0] * len(labels)
        for item in result:
            data[int(item["day"]) - 1] = int(item["sum"])
        return {
            "labels": labels,
            "data": data
        }

    @staticmethod
    def get_monthly(login_id: int, date: datetime.date):
        labels = list(calendar.month_abbr)[1:]
        data = [0] * len(labels)
        result = TransactionModel.get_monthly_expense(login_id, date)
        for item in result:
            data[int(item["month"]) - 1] = int(item["sum"])
        return {
            "labels": labels,
            "data": data
        }


class PieChartData:

    @staticmethod
    def get_category(login_id: int, date: datetime.date):
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
    def get(login_id: int, date: datetime.date, expense_type: str):
        result = None
        if expense_type == ExpenseSumType.DAY:
            result = TransactionModel.get_day_expense(login_id, date)
        elif expense_type == ExpenseSumType.MONTH:
            result = TransactionModel.get_month_expense(login_id, date)
        elif expense_type == ExpenseSumType.YEAR:
            result = TransactionModel.get_year_expense(login_id, date)
        return result


class DashboardService:

    @staticmethod
    def get_graph_data(login_id: int):
        current_date = datetime.date.today()
        return {
            "daily": GraphData.get_daily(login_id, current_date),
            "monthly": GraphData.get_monthly(login_id, current_date)
        }

    @staticmethod
    def get_pie_data(login_id: int):
        current_date = datetime.date.today()
        return {
            "category": PieChartData.get_category(login_id, current_date)
        }

    @staticmethod
    def get_card_data(login_id: int):
        current_date = datetime.date.today()
        total_spent = TransactionService.get_user_spent(login_id)

        budget = UserProfileModel.get_budget(login_id)
        budget_percentage = CommonUtils.calculate_budget_percentage(total_spent, budget) if budget > 0 else -1
        return {
            "expense": {
                "today": ExpenseSum.get(login_id, current_date, ExpenseSumType.DAY),
                "current_month": ExpenseSum.get(login_id, current_date, ExpenseSumType.MONTH),
                "current_year": ExpenseSum.get(login_id, current_date, ExpenseSumType.YEAR),
                "total": total_spent
            },
            "budget_percentage": budget_percentage,
            "user_count": UserModel.get_count()
        }