from flask_mysqldb import MySQL
from backend import app

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'smartsigiUser'
app.config['MYSQL_PASSWORD'] = 'RU46oR7QEMi3vY'
app.config['MYSQL_DB'] = 'smartsigi'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/api/teststring')
def teststring():
    return "teststring"