import sqlite3



def initialise():
    con = sqlite3.connect('PET.db')
    con.execute("CREATE TABLE user (\
    id INTEGER PRIMARY KEY AUTOINCREMENT,\
    email varchar(20) NOT NULL,\
    password varchar(20) NOT NULL\
    );")
    con.commit()
    con.close()


def fetchUserById(id):
    con = sqlite3.connect('PET.db')
    cur = con.cursor()
    query = 'SELECT * FROM user WHERE id = ?'
    param = (id,)
    result_set = []
    for i in cur.execute(query,param):
        result_set.append(i)
    return result_set

def fetchUserByEmail(email):
    con = sqlite3.connect('PET.db')
    cur = con.cursor()
    query = 'SELECT * FROM user WHERE email = ?'
    param = (email,)
    result_set = []
    for i in cur.execute(query,param):
        result_set.append(i)
    return result_set

def insert_user(email, password):
    con = sqlite3.connect('PET.db')
    cur = con.cursor()
    query = 'INSERT INTO user (email,password) VALUES (?, ?)'
    param = (email, password)
    res = cur.execute(query,param)
    con.commit()
    con.close()
    return res


# print(insert_user("jagdish@gmail.com", "jagadish2139"))
# initialise()

# print(fetchUserById(2))



