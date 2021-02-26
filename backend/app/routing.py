from app import app
from flaskext.mysql import MySQL
from flask import request, make_response, Response, json, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from cerberus import Validator
from . import db

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'smartsigiUser'
app.config['MYSQL_DATABASE_PASSWORD'] = 'smartsigiUserPassword'
app.config['MYSQL_DATABASE_DB'] = 'smartsigi'


mysql = MySQL()
mysql.init_app(app)


# REST API
@app.route("/api/hello")
def hello():
    return jsonify({'hello': 'world'})

@app.route("/api/getSnapshotsByLabelId/<label_id>", methods=['GET'])
def getSnapshotsByLabelId(label_id):
    try:
        snapshotsByLabelId = db.getSnapshotsByLabelId(mysql, label_id)
        return jsonify(snapshotsByLabelId)
    except ValueError as e:
        return make_response(Response(), 500)

@app.route("/api/getLastSnapshotByLabelId/<label_id>", methods=['GET'])
def getLastSnapshotByLabelId(label_id):
    try:
        lastSnapshot = db.getLastSnapshotByLabelId(mysql, label_id)
        return jsonify(lastSnapshot)
    except ValueError as e:
        return make_response(Response(), 500)

@app.route("/api/getBasicInfos", methods=['GET'])
def getBasicInfos():
    try:
        basicInfos = db.getBasicInfos(mysql)
        return jsonify(basicInfos)
    except ValueError as e:
        return make_response(Response(), 500)


@app.route("/api/getTempTrendByLabelId/<label_id>", methods=['GET'])
def getTempTrendByLabelId(label_id):
    try:
        tempTrend = db.getTempTrendByLabelId(mysql, label_id)
        return jsonify(tempTrend)
    except ValueError as e:
        return make_response(Response(), 500)




# Returns array of distinct label_ids
@app.route("/api/getDistinctLabelIds", methods=['GET'])
def getDistinctLabelIds():
    try:
        labelIds = db.getDistinctLabelIds(mysql)
        return jsonify(labelIds)
    except ValueError as e:
        return make_response(Response("Something wrong."), 500)

# Add snapshot
@app.route("/api/addSnapshot", methods=['POST'])
def addSnapshot():
    schema = {
        'label_id': {
            'type': 'string',
            'required': True
        },
        'temp': {
            'type': 'number',
            'required': True
        },
        'debug': {
            'type': 'dict',
            'required': True
        }
    }
    v = Validator(schema)
    data = request.get_json()
    if (not v.validate(data)):
        return make_response(Response("Bad Request"), 400)

    try:
        debugData = json.dumps(data["debug"])
        res = db.addSnapshot(mysql, data["label_id"], data["temp"], debugData)
        # Check if Alarm is existing and valid to send a notification
        alarm = db.getAlarmByLabelId(mysql, data["label_id"])
        
        if(alarm and (alarm["notified"] == '' or alarm["notified"] == '0') and (data["temp"] < alarm["temp"])):
            db.updateAlarmNotifiedByLabelId(mysql, data["label_id"], 1)
            ret_custom_name = db.getCustomLabelName(mysql, data["label_id"], alarm["uid"])
            custom_name = ""
            if ret_custom_name:
                custom_name = ret_custom_name
            else:
                custom_name = data["label_id"]
           
            message = {
                "to": alarm["expo_push_token"],
                "title": 'Temperatur Alarm',
                "body": f"Sensor {custom_name} hat das gesetzte Limit von {alarm['temp']}°C unterschritten. Der aktuelle Wert ist {data['temp']}°C",
            }
            headers = {
                    'Accept': 'application/json',
                    'Accept-encoding': 'gzip, deflate',
                    'Content-Type': 'application/json',  
            }
            postData = requests.post('https://exp.host/--/api/v2/push/send', data=json.dumps(message), headers=headers)
            print(postData)
   
        if(alarm and alarm["notified"] == '1' and (alarm["temp"] <= data["temp"])):
            db.updateAlarmNotifiedByLabelId(mysql, data["label_id"], 0)
        return make_response(Response("Snapshot Number: " + json.dumps(res)), 201)
    except ValueError as e:
        return make_response(Response("Could not save data."), 400)

# Add alarm
@app.route("/api/addAlarm", methods=['POST'])
def addAlarm():
    schema = {
        'label_id': {
            'type': 'string',
            'required': True
        },
        'temp': {
            'type': 'number',
            'required': True
        },
        'expo_push_token': {
            'type': 'string',
            'required': True
        },
        'uid': {
            'type': 'string',
            'required': True
        }
    }
    v = Validator(schema)
    data = request.get_json()
    if (not v.validate(data)):
        return make_response(Response("Bad Request"), 400)

    try:
        res = db.addAlarm(mysql, data["label_id"], data["temp"], data["expo_push_token"], data["uid"])
        return make_response(Response("Alarm: " + json.dumps(res)), 201)
    except ValueError as e:
        return make_response(Response("Could not save data."), 400)

@app.route("/api/removeAlarm", methods=['POST'])
def removeAlarm():
    schema = {
        'label_id': {
            'type': 'string',
            'required': True
        },
        'expo_push_token': {
            'type': 'string',
            'required': True
        }
    }
    v = Validator(schema)
    data = request.get_json()
    if (not v.validate(data)):
        return make_response(Response("Bad Request"), 400)
    try:
        res = db.removeAlarmByLabelIdAndToken(mysql, data["label_id"], data["expo_push_token"])
        return make_response(Response("Alarm removed" , 201))
    except ValueError as e:
        return make_response(Response("Could not save data."), 400)
        

# Add custom label name
@app.route("/api/addCustomLabelName", methods=['POST'])
def addCustomLabelName():
    schema = {
        'label_id': {
            'type': 'string',
            'required': True
        },
        'uid': {
            'type': 'string',
            'required': True
        },
        'custom_label_name': {
            'type': 'string',
            'required': True
        }
    }
    v = Validator(schema)
    data = request.get_json()
    if (not v.validate(data)):
        return make_response(Response("Bad Request"), 400)

    try:
        res = db.addCustomLabelName(mysql, data["label_id"], data["uid"], data["custom_label_name"])
        return make_response(Response("Label renamed."), 201)
    except ValueError as e:
        return make_response(Response("Could not save data."), 400)