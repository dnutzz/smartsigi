import datetime

class create_dict(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value

def getDistinctLabelIds(mysql):
    arr = []
    cursor = mysql.get_db().cursor()
    cursor.execute('''SELECT DISTINCT label_id FROM snapshots''')
    rows = cursor.fetchall()
    for row in rows:
        arr.append(row[0])
    return arr

def getSnapshotsByLabelId(mysql, label_id):
    arr = []
    cursor = mysql.get_db().cursor()
    cursor.execute('''SELECT datetime, temp FROM snapshots WHERE label_id=%s ORDER BY datetime DESC;''', (label_id, ))
    rows = cursor.fetchall()
    for row in rows:
        arr.append({"datetime": row[0], "temp": row[1]})
    return arr

def addSnapshot(mysql, label_id, temp, debug):
    cursor = mysql.get_db().cursor()
    cursor.execute('''INSERT INTO snapshots(label_id, temp, debug, datetime) VALUES(%s, %s, %s, now());''', (label_id, temp, debug))
    cursor.execute('''SELECT LAST_INSERT_ID();''')
    res = cursor.fetchone()
    mysql.get_db().commit()
    return res[0]

def getLastSnapshotByLabelId(mysql, label_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('''SELECT temp, datetime FROM snapshots WHERE label_id=%s ORDER BY datetime DESC;''', (label_id, ))
    res = cursor.fetchone()
    return {"temp": res[0], "datetime": res[1]}

def getBasicInfos(mysql):
    labels = getDistinctLabelIds(mysql)
    arr = []
    cursor = mysql.get_db().cursor()
    for label in labels:
        cursor.execute('''SELECT label_id, temp, datetime  FROM snapshots WHERE label_id=%s ORDER BY datetime DESC''', (label, ))
        res = cursor.fetchone()
        arr.append({"label_id": res[0], "temp": res[1], "datetime": res[2]})
    return arr


