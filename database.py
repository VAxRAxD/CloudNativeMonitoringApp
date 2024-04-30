import sqlite3

def createTable():
    conn=sqlite3.connect('serversdb.sqlite3')
    conn.execute(
        '''
        CREATE TABLE "Servers" (
        "Id"	INTEGER,
        "Ip"	TEXT NOT NULL,
        "Username"	TEXT NOT NULL,
        "Filename" TEXT NOT NULL,
        PRIMARY KEY("Id" AUTOINCREMENT  )
        );
        '''
    )
    conn.commit()
    conn.close()

def convertJson(desp,data):
    servers=list()
    for i in range(len(data)):
        srv=dict()
        for j in range(len(desp)):
            srv[desp[j]]=data[i][j]
        servers.append(srv)
    return servers

def viewData():
    conn=sqlite3.connect('serversdb.sqlite3')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Servers;")
    description=list(map(lambda x: x[0], cursor.description))
    data=cursor.fetchall()
    servers=convertJson(description,data)
    cursor.close()
    conn.close()
    return servers

def addData(ip,name,file):
    conn=sqlite3.connect('serversdb.sqlite3')
    cursor=conn.cursor()
    cursor.execute("INSERT INTO Servers (Ip, Username, Filename) VALUES (?, ?, ?);",(ip,name,file))
    cursor.close()
    conn.commit()
    conn.close()

def delData(ip):
    conn=sqlite3.connect('serversdb.sqlite3')
    cursor=conn.cursor()
    cursor.execute("DELETE FROM Servers WHERE Ip=?;",(ip,))
    cursor.close()
    conn.commit()
    conn.close()

def getUser(ip):
    conn=sqlite3.connect('serversdb.sqlite3')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Servers WHERE IP=?;",(ip,))
    data=cursor.fetchall()
    cursor.close()
    conn.close()
    return data[0][2]

def getFile(ip):
    conn=sqlite3.connect('serversdb.sqlite3')
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM Servers WHERE IP=?;",(ip,))
    data=cursor.fetchall()
    cursor.close()
    conn.close()
    return data[0][3]

if __name__ == '__main__':
    createTable()