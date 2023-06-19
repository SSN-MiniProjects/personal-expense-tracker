from config.db import (
    connect_db
)

from models.login_credentials import (
    get_user_by_email
)


def add_transaction(email, transaction, mode, category, datestamp, note):
    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]
    query = 'INSERT INTO user_transactions (login_id,transaction,mode,category,datestamp,note) VALUES (%s,%s,%s,%s,%s,%s)'
    param = (login_id, transaction, mode, category, datestamp, note)
    cursor.execute(query, param)
    query = 'update user_profiles set total_spent=total_spent+%s where login_id=%s;'
    param = (transaction, login_id,)
    cursor.execute(query, param)
    conn.commit()
    cursor.close()
    conn.close()


def get_transactions(email):
    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]
    query = 'SELECT transaction, mode, datestamp, note FROM user_transactions WHERE login_id = %s'
    param = (login_id,)
    cursor.execute(query, param)
    result = cursor.fetchall()
    d = []
    for item in result:
        d.append({
            "transaction" : float(item[0]),
            "mode" : item[1],
            "datestamp" : item[2],
            "note" : item[3]
        })
    cursor.close()
    conn.close()
    return d


# get daywise expenses in a given month and given year of an user
def get_daily_expense(email,required_month_str): #use format yyyy-mm-dd
    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]
    query = '''
        select sum(transaction), extract(day from datestamp)
        from 
        public.user_transactions
        where login_id = %s AND (date_part('month', datestamp) = extract(month from timestamp %s))
        AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
        group by datestamp
    '''
    param = (login_id, required_month_str, required_month_str)
    cursor.execute(query,param)
    result = cursor.fetchall()
    d = []
    for item in result:
        d.append({
            "sum" : item[0],
            "day" : int(item[1])
        })
    cursor.close()
    conn.close()
    return d

# get monthwise expenses in a given year of an user
def get_monthly_expense(email, required_year_str):  # use format yyyy-mm-dd

    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]
    query = '''
        select sum(transaction), extract(month from datestamp)
        from 
        public.user_transactions
        where login_id = %s AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
        group by  extract(month from datestamp)
    '''
    param = (login_id, required_year_str)
    cursor.execute(query, param)
    result = cursor.fetchall()
    d = []
    for item in result:
        d.append({
            "sum" : item[0],
            "month" : int(item[1])
        })
    cursor.close()
    conn.close()
    return d


# get categorywise expenses in given month and given year of an user
def get_category_expense(email, required_month_str): #use format yyyy-mm-dd
    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]
    query = '''
        select sum(transaction), category
        from 
        public.user_transactions
        where login_id = %s AND (date_part('month', datestamp) = extract(month from timestamp %s)) 
        AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
        group by category
    '''
    param = (login_id, required_month_str, required_month_str)
    cursor.execute(query,param)
    result = cursor.fetchall()
    d = []
    for item in result:
        d.append({
            "sum" : item[0],
            "category" : item[1]
        })
    cursor.close()
    conn.close()
    return d


# get specific day expense
def get_day_expense(email, required_date):
    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]
    query = '''
        select sum(transaction) from 
        public.user_transactions
        where login_id = %s AND datestamp =  %s 
        group by datestamp
    '''
    param = (login_id, required_date)
    cursor.execute(query,param)
    res = cursor.fetchone()
    return res[0]

# get specific month expense
def get_month_expense(email, required_date):
    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]
    query = '''select sum(transaction)
        from 
        public.user_transactions
        where login_id = %s AND (date_part('month', datestamp) = extract(month from timestamp %s))
        AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
        group by date_part('month', datestamp)'''
    param = (login_id, required_date, required_date)
    cursor.execute(query,param)
    res = cursor.fetchone()
    return res[0]


# get specific year expense
def get_year_expense(email, required_date):
    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]
    query = '''select sum(transaction)
        from 
        public.user_transactions
        where login_id = %s AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
        group by date_part('year', datestamp)'''
    param = (login_id, required_date)
    cursor.execute(query,param)
    res = cursor.fetchone()
    return res[0]