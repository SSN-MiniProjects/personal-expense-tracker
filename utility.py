from database import get_month_expense,get_annual_expense,global_view_query,get_category_month_expense
from datetime import date



def get_month_graph_data(email,today):
    rs = get_month_expense(email,today.strftime("%Y-%m-%d"))
    labels=[]
    data=[]
    for i in rs:
        labels.append(i["DT"])
        data.append(int(i["TRANSACTION"]))
    
    return [labels,data]

def get_year_graph_data(email,today):
    rs = get_annual_expense(email,today.strftime("%Y-%m-%d"))
    labels=[]
    data=[]
    for i in rs:
        labels.append(i["MT"])
        data.append(int(i["TRANSACTION"]))
    return [labels,data]

def get_category_graph_data(email,today):
    rs = get_category_month_expense(email,today.strftime("%Y-%m-%d"))
    labels=[]
    data=[]
    for i in rs:
        labels.append(i["CATEGORY"])
        data.append(int(i["TRANSACTION"]))
    return [labels,data]
def get_card_details(email):
    rs = global_view_query("SELECT total_spent,BUDGET FROM USER_PROFILES ",email)[0];
    count =  global_view_query('''SELECT COUNT(EMAIL) as "COUNT" FROM USER_CREDENTIALS ''','')[0]["COUNT"];
    print((rs,count))
    return (rs,count)
# Monthly = get_month_graph_data("karthikraja19048@cse.ssn.edu.in",date.today())
# print(sum(Monthly[1]))