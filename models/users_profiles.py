from config.db import (
    connect_db
)

from models.login_credentials import(
    get_user_by_email
)

def get_user_profile(email):
    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]
    query = 'SELECT name, budget, phone, profession, alert from user_profiles WHERE login_id = %s'
    param = (login_id,)
    cursor.execute(query,param)
    result = cursor.fetchone()
    if result is not None:
        return {
            "name" : result[0],
            "budget" : result[1],
            "phone" : result[2],
            "profession" : result[3],
            "alert" : result[4]
        }
    conn.commit()
    cursor.close()
    conn.close()
    return result

def add_user_profile(login_id):
    conn = connect_db()
    cursor = conn.cursor()
    query = 'INSERT INTO user_profiles (login_id) VALUES (%s)'
    param = (login_id,)
    res = cursor.execute(query,param)
    conn.commit()
    cursor.close()
    conn.close()

def update_user_profile(email, name, budget, phone, profession, alert):
    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]
    query = 'UPDATE user_profiles set name=%s, budget=%s, phone=%s, profession=%s, alert=%s where login_id=%s'
    param = (name, budget, phone, profession, alert, login_id)
    res = cursor.execute(query,param)
    conn.commit()
    cursor.close()
    conn.close()

def get_spent_and_budget(email):
    conn = connect_db()
    cursor = conn.cursor()
    login_id = get_user_by_email(email)["id"]
    query = 'SELECT total_spent, budget FROM user_profiles WHERE login_id = %s'
    param = (login_id,)
    cursor.execute(query,param)
    result = cursor.fetchone()
    if result is not None:
        return {
            "total_expense" : result[0],
            "budget" : result[1]
        }
    cursor.close()
    conn.close()
    return result