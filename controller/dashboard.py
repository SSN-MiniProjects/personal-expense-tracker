from flask_login import login_required

from config.factory import AppFlask

app = AppFlask().instance


@app.route('/dashboard')
@login_required
def dashboard():
    user_email = current_user.email

    Daily = get_month_graph_data(user_email, date.today())
    Monthly = get_year_graph_data(user_email, date.today())
    Category = get_category_graph_data(user_email, date.today())

    result = get_spent_and_budget(user_email)
    total_spent = result["total_expense"]
    budget = result["budget"]
    budget_percentage = round(total_spent / budget * 100, 2) if budget > 0 else -1
    user_count = get_user_count()
    today_expense = get_day_expense(user_email, date.today().strftime("%Y-%m-%d"))
    current_month_expense = get_month_expense(user_email, date.today().strftime("%Y-%m-%d"))
    current_year_expense = get_year_expense(user_email, date.today().strftime("%Y-%m-%d"))

    month_names = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    CardData = {
        "TotalExpense": humanize.intcomma(total_spent),
        "TodayExpense": humanize.intcomma(today_expense),
        "CurrentMonthExpense": humanize.intcomma(current_month_expense),
        "CurrentYearExpense": humanize.intcomma(current_year_expense),
        "BudgetPercentage": budget_percentage,
        "UserCount": humanize.intcomma(user_count),
    }

    Month_vice_data = [month_names[i - 1] for i in Monthly[0]]

    GraphData = {
        "ChartArea": {"labels": Daily[0], "data": Daily[1]},
        "ChartPie": {"labels": Category[0], "data": Category[1]},
        "ChartBar": {"labels": Month_vice_data, "data": Monthly[1]}
    }
    return render_template('dashboard.html', GraphData=GraphData, CardData=CardData)
