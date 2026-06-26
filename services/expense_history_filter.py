from datetime import datetime
from typing import List, Dict

class ExpenseHistoryFilter:

    def __init__(self, all_expenses):
        self._all_expenses = all_expenses


    def by_date_range(self, start_string: str, end_string: str) -> List[Dict]:
        start_date = datetime.strptime(start_string, "%Y-%m-%d")
        end_date = datetime.strptime(end_string, "%Y-%m-%d")

        filtered_data = []
        for expense in self._all_expenses:
            expense_date = datetime.strptime(str(expense['datestamp']), "%Y-%m-%d")
            if start_date <= expense_date <= end_date:
                filtered_data.append(expense)
        return filtered_data


    def by_amount_range(self, lower_limit: str, upper_limit: str) -> List[Dict]:
        filtered_data = []
        for expense in self._all_expenses:
            expense_amount = expense['transaction']
            if int(lower_limit) <= expense_amount <= int(upper_limit):
                filtered_data.append(expense)
        return filtered_data


    def by_category(self, category: str) -> List[Dict]:
        filtered_data = []
        for expense in self._all_expenses:
            if expense['category'] == category:
                filtered_data.append(expense)
        return filtered_data


    def by_mode(self, mode: str) -> List[Dict]:
        filtered_data = []
        for expense in self._all_expenses:
            if expense['mode'] == mode:
                filtered_data.append(expense)
        return filtered_data

    def by_event(self, event: str) -> List[Dict]:
        filtered_data = []
        for expense in self._all_expenses:
            if expense['event'] == event:
                filtered_data.append(expense)
        return filtered_data
