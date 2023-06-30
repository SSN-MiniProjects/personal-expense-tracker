from config.db import (
    connect_db
)

from models.login_credentials import (
    get_user_by_email
)


def add_transaction(email, transaction, mode, category, datestamp, note, event):
    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]
    note = note.strip()
    
    if event == "None":
        query = 'INSERT INTO user_transactions (login_id,transaction,mode,category,datestamp,note) VALUES (%s,%s,%s,%s,%s,%s)'
        param = (login_id, transaction, mode, category, datestamp, note)
        cursor.execute(query, param)

    else:
        query = 'INSERT INTO user_transactions (login_id,transaction,mode,category,datestamp,note, event_id) VALUES (%s,%s,%s,%s,%s,%s,%s)'
        param = (login_id, transaction, mode, category, datestamp, note, event)
        cursor.execute(query, param)
        query = 'update user_events set spent=spent+%s where id=%s'
        param = (transaction, event,)
        cursor.execute(query, param)
    
    query = 'update user_profiles set total_spent=total_spent+%s where login_id=%s;'
    param = (transaction, login_id,)
    cursor.execute(query, param)    
    conn.commit()
    cursor.close()
    conn.close()

def update_transaction_by_id(t_id, email, transaction, mode, category, datestamp, note, event):
    
    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]
    note = note.strip()

    query = "select transaction, event_id from user_transactions where id = %s"
    param = (t_id, )
    cursor.execute(query, param)
    res = cursor.fetchone()
    prev_amnt = res[0]
    prev_event_id = res[1]
    current_event_id = None if event == 'None' else event


    ## UPDATE TRANSACTION ##
    
    query ='''update user_transactions 
    set transaction=%s,
    mode = %s,category=%s,datestamp=%s,note=%s,event_id=%s where id= %s'''
    param = (transaction, mode, category, datestamp, note, current_event_id, t_id)
    cursor.execute(query, param)



    ## UPDATE EVENTS ###
    # if previous and current event is same, deduct previous transaction and add current transaction to event spent
    if prev_event_id == event:
        query = 'update user_events set spent=spent -%s + %s where id=%s'
        param = (prev_amnt,transaction, event,)
        cursor.execute(query, param)
    
    else:
        # deduct the previous transaction from previous event spent only if previous event is not None
        if prev_event_id is not None:
            query = 'update user_events set spent=spent -%s where id=%s'
            param = (prev_amnt, prev_event_id,)
            cursor.execute(query, param)

        # add the current transaction to current event spent only if current event is not None
        if current_event_id is not None:
            query = 'update user_events set spent=spent +%s where id=%s'
            param = (transaction, current_event_id,)
            cursor.execute(query, param)


    
    ## UPDATE USER PROFILE ##
    query = 'update user_profiles set total_spent=total_spent -%s + %s where login_id=%s;'
    param = (prev_amnt,transaction, login_id,)
    cursor.execute(query, param)    
    
    
    conn.commit()
    cursor.close()
    conn.close()



def delete_transaction_by_id(t_id, email):
    
    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]

    query = "select transaction, event_id from user_transactions where id = %s"
    param = (t_id, )
    cursor.execute(query, param)
    res = cursor.fetchone()
    prev_amnt, event_id = res
    
    if event_id is not None:

        # decrease prev amount in spent of user_events
        query ='''update user_events 
        set spent=spent-%s
        where id=%s
        '''
        param = (prev_amnt, event_id)
        cursor.execute(query, param)

    # decrease prev amount in total_spent of user_profiles
    query = 'update user_profiles set total_spent=total_spent -%s where login_id=%s;'
    param = (prev_amnt, login_id,)
    cursor.execute(query, param)   

    # remove the particular transaction
    query = 'delete from user_transactions where id=%s;'
    param = (t_id,)
    cursor.execute(query, param)   
    conn.commit()

    cursor.close()
    conn.close()
def get_transaction_by_id(t_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = 'SELECT id, transaction, mode, datestamp, category, event_id, note FROM user_transactions WHERE id=%s'
    param = (t_id,)
    cursor.execute(query, param)
    result = cursor.fetchall()
    d = []
    for item in result:
        d.append({
            "id" : item[0],
            "transaction" : item[1],
            "mode" : item[2],
            "datestamp" : item[3],
            "category" : item[4],
            "event" : item[5],
            "note" : item[6]
        })
    cursor.close()
    conn.close()
    return d

def get_transactions(email):
    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]
    query = 'SELECT id, transaction, mode, datestamp, note, category, event_id FROM user_transactions WHERE login_id = %s order by datestamp desc'
    param = (login_id,)
    cursor.execute(query, param)
    result = cursor.fetchall()
    d = []
    for item in result:
        event_id = item[6]
        query = 'select name from user_events where id=%s'
        param = (event_id,)
        cursor.execute(query, param)
        event_name = cursor.fetchone()
        if event_name is not None:
            event_name = event_name[0]

        d.append({
            "id" : item[0],
            "transaction" : float(item[1]),
            "mode" : item[2],
            "datestamp" : item[3],
            "note" : item[4],
            "category" : item[5],
            "event" : event_name
        })
    cursor.close()
    conn.close()
    return d


def get_transactions_by_event(event_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = 'SELECT id, transaction, mode, datestamp, category, note FROM user_transactions WHERE event_id = %s order by datestamp desc'
    param = (event_id,)
    cursor.execute(query, param)
    result = cursor.fetchall()
    d = []
    for item in result:
        d.append({
            "id" : item[0],
            "transaction" : item[1],
            "mode" : item[2],
            "datestamp" : item[3],
            "category" : item[4],
            "note" : item[5]
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
    if res is None:
        return 0
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
    if res is None:
        return 0
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
    if res is None:
        return 0
    return res[0]