import os 
import psycopg2

def connect_db():
    conn = psycopg2.connect(
        dbname = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASS"),
        host = os.getenv("DB_HOST"),
        port = "5432"
    )
    return conn

def init_db():
    createUserCredentials = "CREATE TABLE IF NOT EXISTS user_credentials (\
        id INT GENERATED BY DEFAULT AS IDENTITY NOT NULL PRIMARY KEY,\
        email VARCHAR(50) NOT NULL,\
        password VARCHAR(100) NOT NULL);"

    createUserProfile = "CREATE TABLE IF NOT EXISTS user_profiles (\
        id INT GENERATED BY DEFAULT AS IDENTITY NOT NULL PRIMARY KEY,\
        login_id INT NOT NULL,\
        name VARCHAR(30),\
        budget INT DEFAULT 0,\
        total_spent NUMERIC DEFAULT 0,\
        phone VARCHAR(30),\
        profession VARCHAR(30),\
        alert BOOLEAN DEFAULT FALSE,\
        FOREIGN KEY (login_id) REFERENCES USER_CREDENTIALS(id) ON DELETE CASCADE);"
    createUserTransactions = "CREATE TABLE IF NOT EXISTS user_transactions (\
        id INT GENERATED BY DEFAULT AS IDENTITY NOT NULL PRIMARY KEY,\
        login_id INT NOT NULL,\
        transaction NUMERIC NOT NULL,\
        mode VARCHAR(10),\
        category VARCHAR(20),\
        datestamp DATE,\
        note VARCHAR(50),\
        FOREIGN KEY (login_id) REFERENCES USER_CREDENTIALS(id) ON DELETE CASCADE);"

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(createUserCredentials)
    cursor.execute(createUserProfile)
    cursor.execute(createUserTransactions)
    conn.commit()
    cursor.close()
    conn.close()
