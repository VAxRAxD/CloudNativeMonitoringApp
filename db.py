import sqlite3


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
    cursor.execute("SELECT * FROM SERVERS;")
    description=list(map(lambda x: x[0], cursor.description))
    data=cursor.fetchall()
    servers=convertJson(description,data)
    cursor.close()
    conn.close()
    return servers

def addData(ip,name):
    conn=sqlite3.connect('serversdb.sqlite3')
    cursor=conn.cursor()
    cursor.execute("INSERT INTO Servers (Ip, Username) VALUES (?, ?);",(ip,name))
    cursor.close()
    conn.commit()
    conn.close()

print(viewData())
addData('44.202.103.183','ubuntu')
print(viewData())