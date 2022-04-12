import mysql
import csv
import pandas as pd
from flask import Flask, render_template, request, jsonify

# install mysql-connector-python
import mysql.connector as connection
from mysql.connector import DatabaseError


class sql():
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.mydb = connection.connect(host=self.host, user=self.user, passwd=self.password, use_pure=True)
        self.cur = self.mydb.cursor()

    def db_connection(self, dbname):
        self.dbname = dbname
        query = f"Create database {self.dbname}"
        self.cur.execute(query)
        print(f"Database '{self.dbname}' is created")


app = Flask(__name__)


@app.route('/mysql/oops_createdb/', methods=['POST'])
def db_connect():
    if request.method == 'POST':
        hostn = request.json['hostname']
        userr = request.json['userID']
        password = request.json['pwd']
        dbn = request.json['dbn']
        try:
            sqlcreate = sql(hostn, userr, password)
            sqlcreate.db_connection(dbn)
            return jsonify(f"Database {dbn} is created")

        except Exception as err:
            return jsonify('Error: ' + str(err))


if __name__ == '__main__':
    app.run(debug=True)
