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
    query = 'SELECT * FROM user_transactions WHERE login_id = %s'
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
def get_month_expense(email,required_month_str): #use format yyyy-mm-dd
    conn = connect_db()
    cursor = conn.cursor()
    login_id = fetchUserByEmail(email)[0]
    query = '''
        select sum(transaction) as TRANSACTION, extract(day from datestamp) as DT
        from 
        public.user_transactions
        where login_id = %s AND (date_part('month', datestamp) = extract(month from timestamp %s))
        AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
        group by datestamp
    '''
    param = (login_id, required_month_str, required_month_str)
    cursor.execute(query,param)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


# get monthwise expenses in a given year of an user
def get_annual_expense(email, required_year_str):  # use format yyyy-mm-dd

    conn = connect_db()
    cursor = conn.cursor()
    login_id = fetchUserByEmail(email)[0]
    query = '''
        select sum(transaction) as TRANSACTION, extract(month from datestamp) as MT
        from 
        public.user_transactions
        where login_id = %s AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
        group by  extract(month from datestamp)
    '''
    param = (login_id, required_year_str)
    cursor.execute(query, param)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


# get categorywise expenses in given month and given year of an user
def get_category_expense(email, required_month_str): #use format yyyy-mm-dd
    conn = connect_db()
    cursor = conn.cursor()
    login_id = fetchUserByEmail(email)[0]
    query = '''
        select sum(transaction) as TRANSACTION, category
        from 
        public.user_transactions
        where login_id = %s AND (date_part('month', datestamp) = extract(month from timestamp %s)) 
        AND (date_part('year', datestamp) = extract(year from timestamp %s)) 
        group by category
    '''
    param = (login_id, required_month_str, required_month_str)
    cursor.execute(query,param)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result
