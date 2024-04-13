class CommonUtils:

    @staticmethod
    def calculate_budget_percentage(total_spent: float, budget: float):
        return round(total_spent / budget * 100, 2)