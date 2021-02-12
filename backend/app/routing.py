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
        return make_response(Response("Snapshot Number: " + json.dumps(res)), 201)
    except ValueError as e:
        return make_response(Response("Could not save data."), 400)




    