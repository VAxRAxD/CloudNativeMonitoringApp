import sqlite3

def createTable():
    conn=sqlite3.connect('servers.db.sqlite3')
    conn.execute(
        '''
        CREATE TABLE "Servers" (
        "Id"	INTEGER,
        "Ip"	TEXT NOT NULL,
        "Username"	TEXT NOT NULL,
        PRIMARY KEY("Id" AUTOINCREMENT  )
        );
        '''
    )
    conn.commit()
    conn.close()

if __name__ == '__main__':
    createTable()