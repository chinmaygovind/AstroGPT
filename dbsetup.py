import sqlite3

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except:
        print("oopsie an error occurred")

    return connection

con = create_connection("mydb.sqlite")
cur = con.cursor()
cur.execute("CREATE TABLE queries(requestID, results, timestamp)")
