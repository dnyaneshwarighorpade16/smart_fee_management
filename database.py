from flask_mysqldb import MySQL
from MySQLdb.cursors import DictCursor

mysql = MySQL()

def init_db(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config['MYSQL_USER'] = 'root'
    app.config['MYSQL_PASSWORD'] = 'Aastha@123'  # put your MySQL password here
    app.config['MYSQL_DB'] = 'smart_fee_management'
    app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # enables dict-style fetches

    mysql.init_app(app)