import mysql
import csv
import pandas as pd
from flask import Flask, render_template, request, jsonify

# install mysql-connector-python
import mysql.connector as connection
from mysql.connector import DatabaseError

app = Flask(__name__)


@app.route('/mysql/connection', methods=['POST'])
def db_connection():
    if (request.method == 'POST'):
        hostn = request.json['hostname']
        userr = request.json['userID']
        password = request.json['pwd']
    mydb = connection.connect(host=hostn, user=userr, passwd=password, use_pure=True)
    res = mydb.is_connected()
    result = 'The connection to MySQL database is established: ' + str(res)
    return jsonify(result)


@app.route('/mysql/dblist', methods=['POST'])
def show_dblist():
    if (request.method == 'POST'):
        hostn = request.json['hostname']
        userr = request.json['userID']
        password = request.json['pwd']
    mydb = connection.connect(host=hostn, user=userr, passwd=password, use_pure=True)
    cur = mydb.cursor()
    cur.execute("SHOW DATABASES")
    result = cur.fetchall()
    return jsonify(result)


@app.route('/mysql/createdb', methods=['POST'])
def create_db():
    if (request.method == 'POST'):
        hostn = request.json['hostname']
        userr = request.json['userID']
        password = request.json['pwd']
        db = request.json['dbname']
    mydb = connection.connect(host=hostn, user=userr, passwd=password, use_pure=True)
    cur = mydb.cursor()
    try:
        cur.execute(f' create database {db}')
        return jsonify('Database created')

    except Exception as err:
        return jsonify('Error: ' + str(err))


# https://stackoverflow.com/questions/2098276/nested-json-objects-do-i-have-to-use-arrays-for-everything
@app.route('/mysql/db/create_table', methods=['POST'])
def create_table():
    if (request.method == 'POST'):
        hostn = request.json['hostname']
        userr = request.json['userID']
        password = request.json['pwd']
        db = request.json['dbname']
        tab = request.json['tablename']

        col1 = request.json['col1']
        col1_name = col1['colname']
        col1_datatype = col1['datatype']
        col1_len = col1['length']

        col2 = request.json['col2']
        col2_name = col2['colname']
        col2_datatype = col2['datatype']
        col2_len = col2['length']

        col3 = request.json['col3']
        col3_name = col3['colname']
        col3_datatype = col3['datatype']
        col3_len = col3['length']

    mydb = connection.connect(host=hostn, user=userr, passwd=password, use_pure=True)
    cur = mydb.cursor()
    try:
        cur.execute(
            f'Create table {db}.{tab} ({col1_name} {col1_datatype}({col1_len}), {col2_name} {col2_datatype}({col2_len}), {col3_name} {col3_datatype}({col3_len}))')
        return jsonify('Table created')

    except Exception as err:
        return jsonify('Error: ' + str(err))


@app.route('/mysql/db/tableslist', methods=['POST'])
def tables_list():
    if (request.method == 'POST'):
        hostn = request.json['hostname']
        userr = request.json['userID']
        password = request.json['pwd']
        db = request.json['dbname']

    mydb = connection.connect(host=hostn, user=userr, passwd=password, use_pure=True)
    cur = mydb.cursor()
    try:
        cur.execute(f'Show tables from {db}')
        result = cur.fetchall()
        return jsonify(result)

    except Exception as err:
        return jsonify('Error: ' + str(err))


@app.route('/mysql/db/table/insertdata', methods=['POST'])
def insert_data():
    if (request.method == 'POST'):
        hostn = request.json['hostname']
        userr = request.json['userID']
        password = request.json['pwd']
        db = request.json['dbname']
        tab = request.json['tablename']
        # v1 = request.json['val1']
        # v2 = request.json['val2']
        # v3 = request.json['val3']
        row1 = request.json['row1']

        mydb = connection.connect(host=hostn, user=userr, passwd=password, use_pure=True)
        cur = mydb.cursor()

        try:
            # cur.execute(f"insert into {db}.{tab} values ({v1},'{v2}','{v3}')")
            cur.execute(f"insert into {db}.{tab} values ({row1['val1']},'{row1['val2']}','{row1['val3']}')")
            mydb.commit()
            return jsonify(f'Values inserted in {db}.{tab}')

        except Exception as err:
            return jsonify('Error: ' + str(err))


@app.route('/mysql/db/table/insertbulkdata', methods=['POST'])
def bulk_insert_data():
    if (request.method == 'POST'):
        hostn = request.json['hostname']
        userr = request.json['userID']
        password = request.json['pwd']
        db = request.json['dbname']
        tab = request.json['tablename']
        row1 = request.json['row1']
        row2 = request.json['row2']
        row3 = request.json['row3']


        mydb = connection.connect(host=hostn, user=userr, passwd=password, use_pure=True)
        cur = mydb.cursor()

        try:
            cur.execute(f"insert into {db}.{tab} values ({row1['val1']},'{row1['val2']}','{row1['val3']}'),\
                        ({row2['val1']},'{row2['val2']}','{row2['val3']}'), ({row3['val1']},'{row3['val2']}','{row3['val3']}')")
            mydb.commit()
            return jsonify(f'Values inserted in {db}.{tab}')

        except Exception as err:
            return jsonify('Error: ' + str(err))

@app.route('/mysql/db/table/insertdata_fromfile', methods=['POST'])
def insert_data_from_csv():
    import csv
    if (request.method == 'POST'):
        hostn = request.json['hostname']
        userr = request.json['userID']
        password = request.json['pwd']
        db = request.json['dbname']
        tab = request.json['tablename']
        file = request.json['filepath']

        mydb = connection.connect(host=hostn, user=userr, passwd=password, use_pure=True)
        cur = mydb.cursor()

        try:
            with open(file, 'r') as data:
                next(data)
                data_csv = csv.reader(data, delimiter=',')
                print(data_csv)
                for i in data_csv:
                    cur.execute(f"insert into {db}.{tab} values (%s,%s,%s)", [int(i[0]), i[1], i[2]])
            mydb.commit()
            return jsonify(f'Values inserted in {db}.{tab}')

        except Exception as err:
            return jsonify('Error: ' + str(err))


@app.route('/mysql/db/table/readdata', methods=['POST'])
def read_data():
    if (request.method == 'POST'):
        hostn = request.json['hostname']
        userr = request.json['userID']
        password = request.json['pwd']
        db = request.json['dbname']
        tab = request.json['tablename']

        mydb = connection.connect(host=hostn, user=userr, passwd=password, use_pure=True)
        cur = mydb.cursor()

        try:
            cur.execute(f"select * from {db}.{tab}")
            res = cur.fetchall()
            return jsonify(res)

        except Exception as err:
            return jsonify('Error: ' + str(err))


@app.route('/mysql/db/table/updatedata', methods=['POST'])
def update_data():
    if (request.method == 'POST'):
        hostn = request.json['hostname']
        userr = request.json['userID']
        password = request.json['pwd']
        db = request.json['dbname']
        tab = request.json['tablename']

        updatedcol = request.json['updatedcol']
        updatedval = request.json['updatedval']
        col2update = request.json['col2update']
        val2update = request.json['val2update']

        mydb = connection.connect(host=hostn, user=userr, passwd=password, use_pure=True)
        cur = mydb.cursor()

        try:
            cur.execute(f"update {db}.{tab} set {updatedcol} = '{updatedval}' where {col2update} = '{val2update}'")
            mydb.commit()
            return jsonify(
                f"Value of column - {updatedcol} in the row having {col2update} : '{val2update}' is updated to {updatedcol} : '{updatedval}'")

        except Exception as err:
            return jsonify('Error: ' + str(err))


@app.route('/mysql/db/table/downloaddata', methods=['POST'])
def download_data():
    import pandas as pd
    if (request.method == 'POST'):
        hostn = request.json['hostname']
        userr = request.json['userID']
        password = request.json['pwd']
        db = request.json['dbname']
        tab = request.json['tablename']
        file = request.json['filepath2download']

        mydb = connection.connect(host=hostn, user=userr, passwd=password, use_pure=True)
        cur = mydb.cursor()

        try:
            b = pd.read_sql(f'select * from {db}.{tab}', mydb)
            b.to_csv(f'{file}')
            return jsonify(f"Data downloaded to {file}.")

        except Exception as err:
            return jsonify('Error: ' + str(err))


@app.route('/mysql/db/table/deletedata', methods=['POST'])
def delete_data():
    if (request.method == 'POST'):
        hostn = request.json['hostname']
        userr = request.json['userID']
        password = request.json['pwd']
        db = request.json['dbname']
        tab = request.json['tablename']
        col = request.json['colname']
        v = request.json['value']

        mydb = connection.connect(host=hostn, user=userr, passwd=password, use_pure=True)
        cur = mydb.cursor()

        try:
            # cur.execute(f"select * from {db}.{tab} where {col} = '{v}'")
            cur.execute(f"delete from {db}.{tab} where {col} = '{v}'")
            mydb.commit()
            return jsonify(f"row having {col} : '{v}' is deleted")

        except Exception as err:
            return jsonify('Error: ' + str(err))


@app.route('/mysql/db/droptable', methods=['POST'])
def drop_table():
    if (request.method == 'POST'):
        hostn = request.json['hostname']
        userr = request.json['userID']
        password = request.json['pwd']
        db = request.json['dbname']
        tab = request.json['tablename']

        mydb = connection.connect(host=hostn, user=userr, passwd=password, use_pure=True)
        cur = mydb.cursor()

        try:
            cur.execute(f"drop table {db}.{tab}")
            # mydb.commit()
            return jsonify(f"Table: {tab} is dropped from the database: {db}")

        except Exception as err:
            return jsonify('Error: ' + str(err))


@app.route('/mysql/dropdb', methods=['POST'])
def drop_db():
    if (request.method == 'POST'):
        hostn = request.json['hostname']
        userr = request.json['userID']
        password = request.json['pwd']
        db = request.json['dbname']

        mydb = connection.connect(host=hostn, user=userr, passwd=password, use_pure=True)
        cur = mydb.cursor()

        try:
            cur.execute(f"drop database {db}")
            # mydb.commit()
            return jsonify(f"Database: {db} is dropped")

        except Exception as err:
            return jsonify('Error: ' + str(err))


if __name__ == '__main__':
    app.run(debug=True)
