import datetime

from config.db import (
    get_result
)
from models.users_credentials import UserModel


class TransactionModel:

    @staticmethod
    def create(login_id, transaction, mode, category, datestamp, note, event):
        note = note.strip()
        query = ('INSERT INTO user_transactions (login_id,transaction,mode,category,datestamp,note, event_id) '
                 'VALUES (%s,%s,%s,%s,%s,%s,%s)')
        param = (login_id, transaction, mode, category, datestamp, note, event)
        print(param)
        get_result(query, param)

    @staticmethod
    def update(transaction_id, transaction, mode, category, datestamp, note, event):
        note = note.strip()
        query = '''update user_transactions 
        set transaction=%s,
        mode = %s,category=%s,datestamp=%s,note=%s,event_id=%s where id= %s'''
        param = (transaction, mode, category, datestamp, note, event, transaction_id)
        get_result(query, param)

    @staticmethod
    def get_event_amount(transaction_id: int):
        query = "select transaction, event_id from user_transactions where id = %s"
        param = (transaction_id,)
        amount, event_id = get_result(query, param)[0]
        return {
            "amount": amount,
            "event_id": event_id
        }

    @staticmethod
    def delete(transaction_id: int):
        query = 'delete from user_transactions where id=%s;'
        param = (transaction_id,)
        get_result(query, param)

    @staticmethod
    def get(login_id: int, transaction_id: int) -> list:
        query = ('SELECT id, transaction, mode, datestamp, category, event_id, note FROM user_transactions '
                 'WHERE id=%s and login_id=%s')
        param = (transaction_id, login_id)
        result = get_result(query, param)
        return result

    @staticmethod
    def get_all(login_id: int) -> list:
        query = ('SELECT id, transaction, mode, datestamp, note, category, event_id FROM user_transactions WHERE '
                 'login_id = %s order by datestamp desc')
        param = (login_id,)
        result = get_result(query, param)
        return result

    @staticmethod
    def get_by_event(event_id: int) -> list[dict]:
        query = ('SELECT id, transaction, mode, datestamp, category, note FROM user_transactions WHERE event_id = %s '
                 'order by datestamp desc')
        param = (event_id,)
        result = get_result(query, param)
        return result


    # get daywise expenses in a given month and given year of an user
    @staticmethod
    def get_daily_expense(login_id: int, required_month_str: datetime.date):  # use format yyyy-mm-dd
        query = '''
            select sum(transaction), extract(day from datestamp)
            from 
            public.user_transactions
            where login_id = %s AND (date_part('month', datestamp) = extract(month from timestamp %s))
            AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
            group by datestamp
        '''
        param = (login_id, required_month_str, required_month_str)

        result = get_result(query, param)
        d = []
        for item in result:
            d.append({
                "sum": item[0],
                "day": int(item[1])
            })
        return d

    # get monthwise expenses in a given year of an user
    @staticmethod
    def get_monthly_expense(login_id: int, required_year_str: datetime.date):  # use format yyyy-mm-dd
        query = '''
            select sum(transaction), extract(month from datestamp)
            from 
            public.user_transactions
            where login_id = %s AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
            group by  extract(month from datestamp)
        '''
        param = (login_id, required_year_str)
        result = get_result(query, param)
        d = []
        for item in result:
            d.append({
                "sum": item[0],
                "month": int(item[1])
            })
        return d

    # get categorywise expenses in given month and given year of an user
    @staticmethod
    def get_category_expense(login_id: int, required_month_str: datetime.date):  # use format yyyy-mm-dd
        query = '''
            select sum(transaction), category
            from 
            public.user_transactions
            where login_id = %s AND (date_part('month', datestamp) = extract(month from timestamp %s)) 
            AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
            group by category
        '''
        param = (login_id, required_month_str, required_month_str)
        result = get_result(query, param)
        d = []
        for item in result:
            d.append({
                "sum": item[0],
                "category": item[1]
            })
        return d

    @staticmethod
    def get_day_expense(login_id: int, required_date: datetime.date):
        query = '''
            select sum(transaction) from 
            public.user_transactions
            where login_id = %s AND datestamp =  %s 
            group by datestamp
        '''
        param = (login_id, required_date)
        res = get_result(query, param)
        return res

    @staticmethod
    def get_month_expense(login_id: int, required_date: datetime.date):
        query = '''select sum(transaction)
            from 
            public.user_transactions
            where login_id = %s AND (date_part('month', datestamp) = extract(month from timestamp %s))
            AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
            group by date_part('month', datestamp)'''
        param = (login_id, required_date, required_date)
        res = get_result(query, param)
        return res

    # get specific year expense
    @staticmethod
    def get_year_expense(login_id: int, required_date: datetime.date):
        query = '''select sum(transaction)
            from 
            public.user_transactions
            where login_id = %s AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
            group by date_part('year', datestamp)'''
        param = (login_id, required_date)
        res = get_result(query, param)
        return res
