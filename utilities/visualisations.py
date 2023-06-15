from models.transactions import (
    get_month_expense,
    get_annual_expense,
    get_category_expense
)

import calendar


def get_month_graph_data(email, given_date):

    # get current month day count
    day_count = calendar.monthrange(given_date.year, given_date.month)[1]

    # get all days as labels
    labels = list(range(1,day_count+1))

    # assign initial spent to zero for all days
    data = [0]*len(labels)

    result = get_month_expense(email, given_date.strftime("%Y-%m-%d"))

    # based on result from db, update the expense corresponding to its day
    for item in result:
        data[item["day"]-1] = int(item["sum"])

    return [labels,data]


def get_year_graph_data(email, given_date):
    
    # assign labels to 12 months and their expenses to 0
    labels = list(range(1,13))
    data = [0]*len(labels)

    result = get_annual_expense(email, given_date.strftime("%Y-%m-%d"))
    # based on result from db, update the expense corresponding to its day
    for item in result:
        data[item["month"]-1] = int(item["sum"])

    return [labels, data]

def get_category_graph_data(email, given_date):
    result = get_category_expense(email, given_date.strftime("%Y-%m-%d"))
    labels = []
    data = []
    for item in result:
        labels.append(item["category"])
        data.append(int(item["sum"]))
    return [labels, data]

