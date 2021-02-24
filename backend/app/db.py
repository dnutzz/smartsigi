import datetime

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
    cursor.execute('''SELECT datetime, temp FROM snapshots WHERE label_id=%s ORDER BY datetime DESC LIMIT 100;''', (label_id, ))
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
        cursor.execute('''SELECT label_id, temp, datetime  FROM snapshots WHERE label_id=%s ORDER BY datetime DESC;''', (label, ))
        res = cursor.fetchone()
        arr.append({"label_id": res[0], "temp": res[1], "datetime": res[2]})
    return arr

def getTempTrendByLabelId(mysql, label_id):
    labels = getDistinctLabelIds(mysql)
    ret = {"12h": [], "6h": [], "2h": []}
    cursor = mysql.get_db().cursor()
    intervals = [12, 6, 2]
    for interval in intervals:
        cursor.execute('''SELECT temp, `datetime`  FROM snapshots WHERE label_id =%s AND `datetime` > DATE_SUB(NOW(),INTERVAL %s HOUR) ORDER BY id DESC;''', (label_id,interval ))
        res = cursor.fetchall()
        for row in res:
            ret[f'{interval}h'].append(row[0])
    return ret

def addAlarm(mysql, label_id, temp, expo_push_token):
    cursor = mysql.get_db().cursor()
    cursor.execute('''INSERT INTO alarms(label_id, temp, expo_push_token, datetime, notified) VALUES(%s, %s, %s, now(), 0);''', (label_id, temp, expo_push_token))
    cursor.execute('''SELECT LAST_INSERT_ID();''')
    res = cursor.fetchone()
    mysql.get_db().commit()
    return res[0]

def getAlarmByLabelId(mysql, label_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('''SELECT temp, expo_push_token, notified FROM alarms WHERE label_id=%s ORDER BY datetime DESC;''', (label_id, ))
    res = cursor.fetchone()
    if(res):
        return {"temp": res[0], "expo_push_token": res[1], "notified": res[2]}
    else:
        return None;

def updateAlarmNotifiedByLabelId(mysql, label_id, status):
    cursor = mysql.get_db().cursor()
    cursor.execute('''UPDATE alarms SET notified='%s' WHERE label_id=%s;''', (status, label_id, ))
    mysql.get_db().commit()

def removeAlarmByLabelIdAndToken(mysql, label_id, expo_push_token):
    cursor = mysql.get_db().cursor()
    cursor.execute('''DELETE FROM alarms WHERE (label_id=%s AND expo_push_token=%s);''', (label_id, expo_push_token, ))
    mysql.get_db().commit()
  
