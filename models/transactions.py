import datetime

from config.db import get_result_dict

class TransactionModel:

    @staticmethod
    def create(login_id, transaction, mode, category, datestamp, note, event) -> None:
        note = note.strip()
        query = ('INSERT INTO user_transactions (login_id,transaction,mode,category,datestamp,note, event_id) '
                 'VALUES (%s,%s,%s,%s,%s,%s,%s)')
        param = (login_id, transaction, mode, category, datestamp, note, event)
        get_result_dict(query, param)

    @staticmethod
    def update(transaction_id, transaction, mode, category, datestamp, note, event):
        note = note.strip()
        query = '''update user_transactions 
        set transaction=%s,
        mode = %s,category=%s,datestamp=%s,note=%s,event_id=%s where id= %s'''
        param = (transaction, mode, category, datestamp, note, event, transaction_id)
        get_result_dict(query, param)

    @staticmethod
    def get_event_amount(transaction_id: int):
        query = "select transaction as amount, event_id from user_transactions where id = %s"
        param = (transaction_id,)
        return get_result_dict(query, param)

    @staticmethod
    def delete(transaction_id: int):
        query = 'delete from user_transactions where id=%s;'
        param = (transaction_id,)
        get_result_dict(query, param)

    @staticmethod
    def get(login_id: int, transaction_id: int) -> list:
        query = ('SELECT id, transaction, mode, datestamp, category, event_id as event, note FROM user_transactions '
                 'WHERE id=%s and login_id=%s')
        param = (transaction_id, login_id)
        return get_result_dict(query, param)

    @staticmethod
    def get_all(login_id: int) -> list:
        query = 'select ut.id, ut.login_id, transaction, mode, category, event_id, ue.name as event, ut.datestamp from user_transactions ut left join user_events ue on ut.event_id = ue.id where ut.login_id=%s;'
        param = (login_id,)
        result = get_result_dict(query, param)
        return result

    @staticmethod
    def get_by_event(event_id: int) -> list[dict]:
        query = ('SELECT id, transaction, mode, datestamp, category, note FROM user_transactions WHERE event_id = %s '
                 'order by datestamp desc')
        param = (event_id,)
        result = get_result_dict(query, param)
        return result


    # get daywise expenses in a given month and given year of an user
    @staticmethod
    def get_daily_expense(login_id: int, required_month_str: datetime.date):  # use format yyyy-mm-dd
        query = '''
            select sum(transaction), extract(day from datestamp) as day
            from 
            public.user_transactions
            where login_id = %s AND (date_part('month', datestamp) = extract(month from timestamp %s))
            AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
            group by datestamp
        '''
        param = (login_id, required_month_str, required_month_str)
        return get_result_dict(query, param)

    # get monthwise expenses in a given year of an user
    @staticmethod
    def get_monthly_expense(login_id: int, required_year_str: datetime.date):  # use format yyyy-mm-dd
        query = '''
            select sum(transaction) as sum, extract(month from datestamp) as month
            from 
            public.user_transactions
            where login_id = %s AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
            group by  extract(month from datestamp)
        '''
        param = (login_id, required_year_str)
        return get_result_dict(query, param)

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
        return get_result_dict(query, param)

    @staticmethod
    def get_day_expense(login_id: int, required_date: datetime.date) -> int:
        query = '''
            select sum(transaction) from 
            public.user_transactions
            where login_id = %s AND datestamp =  %s 
            group by datestamp
        '''
        param = (login_id, required_date)
        res = get_result_dict(query, param)
        return 0 if not res else res[0]['sum']

    @staticmethod
    def get_month_expense(login_id: int, required_date: datetime.date):
        query = '''select sum(transaction)
            from 
            public.user_transactions
            where login_id = %s AND (date_part('month', datestamp) = extract(month from timestamp %s))
            AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
            group by date_part('month', datestamp)'''
        param = (login_id, required_date, required_date)
        res = get_result_dict(query, param)
        return 0 if not res else res[0]['sum']

    # get specific year expense
    @staticmethod
    def get_year_expense(login_id: int, required_date: datetime.date):
        query = '''select sum(transaction)
            from 
            public.user_transactions
            where login_id = %s AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
            group by date_part('year', datestamp)'''
        param = (login_id, required_date)
        res = get_result_dict(query, param)
        return 0 if not res else res[0]['sum']

    @staticmethod
    def get_sum_transactions(login_id: int)->list[dict]:
        query = '''select login_id, sum(transaction) as sum from public.user_transactions
                 where login_id = %s
                 group by 1'''
        param = (login_id, )
        return get_result_dict(query, param)

    @staticmethod
    def get_sum_event_transactions(login_id: int, event_id: int):
        query = '''select login_id, event_id, sum(transaction) from public.user_transactions
                 where login_id = %s and event_id = %s
                 group by 1,2'''
        param = (login_id, event_id)
        result = get_result_dict(query, param)
        return 0 if not result else result[0]['sum']