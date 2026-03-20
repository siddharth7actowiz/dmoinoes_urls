from config import *
import mysql.connector

def make_connection():
    conn = mysql.connector.connect(**DB_CONFIG)
    return conn
def create_Tables(cursor,TAB,TAB2):
    ddl=f'''CREATE TABLE IF NOT EXISTS {TAB}(
           Citiy_Name VARCHAR(290),
           City_URL TEXT
        );'''
    
    dd2=f'''CREATE TABLE IF NOT EXISTS {TAB2}(
            id  INT AUTO_INCREMENT PRIMARY KEY,
            Store_Name VARCHAR(250),
            Address TEXT ,
            Pincode INT,
            Region VARCHAR(250),
            City VARCHAR(250),
            ETA VARCHAR(250),
            Timing VARCHAR(250),
            Phone_Number VARCHAR(250),
            Cost VARCHAR(250),
            Good_for VARCHAR(250),
            Store_Url TEXT,
            Menu_Url TEXT
        );'''
    cursor.execute(ddl)
    cursor.execute(dd2)





def insert_into_db(data, cursor, con,TABLE_NAME):
    if not data:                          
        print("No data to insert.")
        return
    try:
        cols = ",".join(data[0].keys())
        vals = ",".join(["%s"] * len(data[0].keys()))
        insert_query = f"INSERT INTO {TABLE_NAME} ({cols}) VALUES ({vals});"
        rows = [tuple(p_data.values()) for p_data in data]
        cursor.executemany(insert_query, rows)
        con.commit()
        print(f"{cursor.rowcount} rows inserted.")
    except Exception as e:
        con.rollback()
        print("Error", insert_into_db.__name__, e)

        