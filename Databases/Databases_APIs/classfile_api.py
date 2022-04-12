import mysql
import csv
import pandas as pd
from flask import Flask, render_template, request, jsonify

# install mysql-connector-python
import mysql.connector as connection
from mysql.connector import DatabaseError
import classfile

app = Flask(__name__)

@app.route('/mysql/oops_createdb2/', methods=['POST'])
def db_connect():
    if request.method == 'POST':
        hostn = request.json['hostname']
        userr = request.json['userID']
        password = request.json['pwd']
        dbn = request.json['dbn']
        try:
            sqlcreate = classfile.sql(hostn, userr, password)
            sqlcreate.db_connection(dbn)
            return jsonify(f"Database {dbn} is created")

        except Exception as err:
            return jsonify('Error: ' + str(err))


if __name__ == '__main__':
    app.run(debug=True)
