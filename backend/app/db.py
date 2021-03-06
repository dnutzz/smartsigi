import datetime

def getDistinctLabelIds(mysql):
    arr = []
    cursor = mysql.get_db().cursor()
    cursor.execute('''SELECT label_id FROM labels;''')
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
    if(res):
        return {"temp": res[0], "datetime": res[1]}
    else:
        return None

def getBasicInfos(mysql):
    labels = getDistinctLabelIds(mysql)
    arr = []
    cursor = mysql.get_db().cursor()
    for label in labels:
        cursor.execute('''SELECT label_id, temp, datetime  FROM snapshots WHERE label_id=%s ORDER BY datetime DESC;''', (label, ))
        res = cursor.fetchone()
        if(res):
            arr.append({"label_id": res[0], "temp": res[1], "datetime": res[2]})
    return arr

def getTempTrendByLabelId(mysql, label_id):
    # ret = {"12h": [], "6h": [], "2h": []}
    ret = {"1h": []}
    cursor = mysql.get_db().cursor()
    intervals = [1]
    for interval in intervals:
        cursor.execute('''SELECT temp, `datetime` FROM snapshots WHERE label_id =%s AND `datetime` > DATE_SUB(NOW(),INTERVAL %s HOUR) ORDER BY id DESC;''', (label_id,interval ))
        res = cursor.fetchall()
        if res:
            for row in res:
                ret[f'{interval}h'].append(row[0])
    return ret

def addAlarm(mysql, label_id, temp, expo_push_token, uid):
    cursor = mysql.get_db().cursor()
    cursor.execute('''INSERT INTO alarms(uid, label_id, temp, expo_push_token, datetime, notified) VALUES(%s, %s, %s, %s, now(), 0);''', (uid, label_id, temp, expo_push_token))
    cursor.execute('''SELECT LAST_INSERT_ID();''')
    res = cursor.fetchone()
    mysql.get_db().commit()
    return res[0]

def getAlarmByLabelId(mysql, label_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('''SELECT temp, expo_push_token, notified, uid FROM alarms WHERE label_id=%s ORDER BY datetime DESC;''', (label_id, ))
    res = cursor.fetchone()
    if(res):
        return {"temp": res[0], "expo_push_token": res[1], "notified": res[2], "uid": res[3]}
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
  
def addCustomLabelName(mysql, label_id, uid, custom_label_name):
    cursor = mysql.get_db().cursor()
    cursor.execute('''SELECT id from custom_labels WHERE (label_id=%s AND uid=%s);''',(label_id, uid,))
    res = cursor.fetchone()
    if res:
        cursor.execute('''UPDATE custom_labels SET custom_label_name=%s WHERE (label_id=%s AND uid=%s);''', (custom_label_name, label_id,uid ))
        mysql.get_db().commit()
        return "Updated"
    else:    
        cursor.execute('''INSERT INTO custom_labels(label_id, uid, custom_label_name) VALUES(%s, %s, %s);''', (label_id, uid, custom_label_name))
        cursor.execute('''SELECT LAST_INSERT_ID();''')
        res = cursor.fetchone()
        mysql.get_db().commit()
        return res[0]

def getCustomLabelName(mysql, label_id, uid):
    cursor = mysql.get_db().cursor()
    cursor.execute('''SELECT custom_label_name FROM custom_labels WHERE label_id=%s AND uid=%s ORDER BY id DESC;''', (label_id,uid))
    res = cursor.fetchone()
    if(res):
        return res[0]
    return None;
    
def getCustomLabelsByUid(mysql, uid):
    cursor = mysql.get_db().cursor()
    ret = {}
    cursor.execute('''SELECT label_id, custom_label_name FROM custom_labels WHERE uid=%s ORDER BY id DESC;''', (uid))
    res = cursor.fetchall()
    for row in res:
        ret[row[0]] = row[1]
    return ret

def addLabel(mysql, label_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('''INSERT INTO labels(label_id) VALUES(%s);''', (label_id,))
    cursor.execute('''SELECT LAST_INSERT_ID();''')
    res = cursor.fetchone()
    mysql.get_db().commit()
    return res[0]
