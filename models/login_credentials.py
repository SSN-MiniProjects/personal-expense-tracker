from config.db import (
    connect_db
)

import hashlib

def add_user_credential(email, given_password):
    conn = connect_db()
    cursor = conn.cursor()
    password = hashlib.sha256(given_password.encode('utf-8')).hexdigest()
    query = 'INSERT INTO user_credentials (email, password) VALUES (%s, %s)'
    param = (email, password)
    res = cursor.execute(query,param)
    conn.commit()
    cursor.close()
    conn.close()

def get_user_by_id(id):
    conn = connect_db()
    cursor = conn.cursor()
    query = 'SELECT * FROM user_credentials WHERE id = %s'
    param = (id,)
    cursor.execute(query,param)
    res = cursor.fetchone()
    result = {}
    if res is not None:
        return {
            "id" : res[0],
            "email" : res[1],
            "password" : res[2]
        }
    cursor.close()
    conn.close()
    return res

def get_user_by_email(email): 
    conn = connect_db()
    cursor = conn.cursor()
    query = 'SELECT * FROM user_credentials WHERE email = %s'
    param = (email,)
    cursor.execute(query,param)
    res = cursor.fetchone()
    if res is not None:
        return {
            "id" : res[0],
            "email" : res[1],
            "password" : res[2]
        }
    cursor.close()
    conn.close()
    return res

def get_user_count():
    conn = connect_db()
    cursor = conn.cursor()
    query = 'SELECT count(email) FROM user_credentials'
    cursor.execute(query)
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0]
