import sqlite3

def viewData():
    conn=sqlite3.connect('servers.db.sqlite3')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM SERVERS;")
    data=cursor.fetchall()
    print(data)
    cursor.close()
    conn.close()

viewData()