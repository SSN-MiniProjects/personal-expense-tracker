from config.db import (
    connect_db
)

from models.login_credentials import(
    get_user_by_email
)

def add_user_event(email, name, budget):
    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]
    name = name.strip()

    ## check for same name!
    query = 'SELECT * from user_events where login_id=%s and name=%s'
    param = (login_id, name)
    cursor.execute(query, param)
    res = cursor.fetchone()
    if res is not None:
        raise ValueError("Event already added")

    query = 'INSERT INTO user_events (login_id, name, budget ) VALUES (%s,%s,%s)'
    param = (login_id, name, budget)
    res = cursor.execute(query,param)
    conn.commit()
    cursor.close()
    conn.close()

def get_user_events(email):
    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]
    query = 'SELECT id, name,budget,spent from user_events where login_id=%s'
    param = (login_id,)
    cursor.execute(query, param)
    result = cursor.fetchall()
    d = []
    for item in result:
        d.append({
            "id" : item[0],
            "name" : item[1],
            "budget" : item[2],
            "spent" : item[3],
        })
    cursor.close()
    conn.close()
    return d

def get_event_by_id(id):
    conn = connect_db()
    cursor = conn.cursor()
    query = 'SELECT id, name, budget, spent from user_events where id=%s'
    param = (id,)
    cursor.execute(query, param)
    result = cursor.fetchall()
    d = []
    for item in result:
        d.append({
            "id" : item[0],
            "name" : item[1],
            "budget" : item[2],
            "spent" : item[3],
        })
    cursor.close()
    conn.close()
    return d

def update_event_by_id(event_id, name, budget):
    conn = connect_db()
    cursor = conn.cursor()
    name = name.strip()

    query = 'update user_events set name=%s,budget=%s where id=%s'
    param = (name, budget, event_id)
    cursor.execute(query, param)
    conn.commit()
    cursor.close()
    conn.close()

def delete_event_by_id(event_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = 'delete from user_events where id=%s'
    param = (event_id, )
    cursor.execute(query, param)


    # delete the transactions having this event id
    query = 'delete from user_transactions where event_id=%s'
    param = (event_id, )
    cursor.execute(query, param)


    conn.commit()
    cursor.close()
    conn.close()
