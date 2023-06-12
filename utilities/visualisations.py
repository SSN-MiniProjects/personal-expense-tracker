from models.transactions import (
    get_month_expense,
    get_annual_expense,
    get_category_expense
)


def get_month_graph_data(email, given_date):
    result = get_month_expense(email, given_date.strftime("%Y-%m-%d"))
    labels = []
    data = []
    for item in result:
        labels.append(item["day"])
        data.append(int(item["sum"]))
    return [labels,data]


def get_year_graph_data(email, given_date):
    result = get_annual_expense(email, given_date.strftime("%Y-%m-%d"))
    labels = []
    data = []
    for item in result:
        labels.append(item["month"])
        data.append(int(item["sum"]))
    return [labels, data]

def get_category_graph_data(email, given_date):
    result = get_category_expense(email, given_date.strftime("%Y-%m-%d"))
    labels = []
    data = []
    for item in result:
        labels.append(item["category"])
        data.append(int(item["sum"]))
    return [labels, data]

