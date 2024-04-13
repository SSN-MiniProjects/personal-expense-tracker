import calendar
from datetime import date

from flask_login import login_required, current_user
import humanize
from config.factory import AppFlask
from services.dashboard import DashboardService
from flask import render_template

app = AppFlask().instance

def view_dashboard():
    user_email = current_user.email
    card_data = DashboardService.get_card_data(user_email)
    card_data_dict = {
        "TotalExpense": humanize.intcomma(card_data["expense"]["total"]),
        "TodayExpense": humanize.intcomma(card_data["expense"]["today"]),
        "CurrentMonthExpense": humanize.intcomma(card_data["expense"]["current_month"]),
        "CurrentYearExpense": humanize.intcomma(card_data["expense"]["current_year"]),
        "BudgetPercentage": card_data["budget_percentage"],
        "UserCount": humanize.intcomma(card_data["user_count"]),
    }
    graph_data = DashboardService.get_graph_data(user_email)
    pie_chart_data = DashboardService.get_pie_data(user_email)
    graph_data_dict = {
        "ChartArea": {"labels": graph_data["daily"]["labels"], "data": graph_data["daily"]["data"]},
        "ChartPie": {"labels": pie_chart_data["category"]["labels"], "data": pie_chart_data["category"]["data"]},
        "ChartBar": {"labels": graph_data["monthly"]["labels"], "data": graph_data["monthly"]["data"]}
    }

    return render_template('dashboard.html', GraphData=graph_data_dict, CardData=card_data_dict)
