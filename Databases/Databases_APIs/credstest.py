import mysql
from flask import Flask, render_template, request, jsonify

import creds

# install mysql-connector-python
import mysql.connector as connection
from mysql.connector import DatabaseError

app = Flask(__name__)

"""Here we are connecting to the database but getting credentials from other python file (creds.py) 
instead of getting from the postman (to make sure that no one can see our creds in the postman)"""


@app.route('/mysql/testconnection', methods=['POST'])
def db_connection():
    if (request.method == 'POST'):
        mydb = connection.connect(host=creds.sqlhost, user=creds.sqluser, passwd=creds.sqlpassword, use_pure=True)
    res = mydb.is_connected()
    result = 'The connection to MySQL database is established: ' + str(res)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
