import pymongo
import csv
import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/mongodb/connection', methods=['POST'])
def db_connection():
    if (request.method == 'POST'):
        localhost = request.json['localhost']
        port = request.json['port']
    try:
        client = pymongo.MongoClient(f"mongodb://{localhost}:{port}/")
        return str(client)
    except Exception as err:
        return jsonify('Error: ' + str(err))


@app.route('/mongodb/dblist', methods=['POST'])
def show_dblist():
    if (request.method == 'POST'):
        localhost = request.json['localhost']
        port = request.json['port']
    try:
        client = pymongo.MongoClient(f"mongodb://{localhost}:{port}/")
        dblist = client.list_database_names()
        return jsonify(dblist)
    except Exception as err:
        return jsonify('Error: ' + str(err))


@app.route('/mongodb/createdb', methods=['POST'])
def create_db():
    if (request.method == 'POST'):
        localhost = request.json['localhost']
        port = request.json['port']
        db = request.json['dbname']

    try:
        client = pymongo.MongoClient(f"mongodb://{localhost}:{port}/")
        client[db]
        return jsonify(f"Database: {db} is created successfully")
    except Exception as err:
        return jsonify('Error: ' + str(err))


@app.route('/mongodb/db/create_collection', methods=['POST'])
def create_collection():
    if (request.method == 'POST'):
        localhost = request.json['localhost']
        port = request.json['port']
        db = request.json['dbname']
        collname = request.json['collection_name']

    try:
        client = pymongo.MongoClient(f"mongodb://{localhost}:{port}/")
        client[db][collname]
        return jsonify(f"Collection: {collname} is created successfully")
    except Exception as err:
        return jsonify('Error: ' + str(err))


@app.route('/mongodb/db/collection/insertdata', methods=['POST'])
def insert_data():
    if (request.method == 'POST'):
        localhost = request.json['localhost']
        port = request.json['port']
        db = request.json['dbname']
        collname = request.json['collection_name']
        data2insert = request.json['record']

    try:
        client = pymongo.MongoClient(f"mongodb://{localhost}:{port}/")
        coll = client[db][collname]
        coll.insert_one(data2insert)

        return jsonify(f"Data inserted into the  collection: {collname} successfully.")
    except Exception as err:
        return jsonify('Error: ' + str(err))


@app.route('/mongodb/db/collection/insert_bulkdata', methods=['POST'])
def insert_bulkdata():
    if (request.method == 'POST'):
        localhost = request.json['localhost']
        port = request.json['port']
        db = request.json['dbname']
        collname = request.json['collection_name']
        data2insert = request.json['list_of_records']

    try:
        client = pymongo.MongoClient(f"mongodb://{localhost}:{port}/")
        coll = client[db][collname]
        coll.insert_many(data2insert)

        return jsonify(f"Data inserted into the  collection: {collname} successfully.")
    except Exception as err:
        return jsonify('Error: ' + str(err))


# https://sqlserverguides.com/import-csv-into-mongodb/
@app.route('/mongodb/db/collection/insertdata_fromfile', methods=['POST'])
def insert_data_from_csv():
    import csv
    import json
    import pymongo

    if (request.method == 'POST'):
        localhost = request.json['localhost']
        port = request.json['port']
        db = request.json['dbname']
        collname = request.json['collection_name']
        file = request.json['file']

    try:
        # CSV to JSON Conversion
        csvfile = open(file, 'r')
        reader = csv.DictReader(csvfile)

        client = pymongo.MongoClient(f"mongodb://{localhost}:{port}/")  # connecting to MongoDB Compass
        db = client[db]  # creating database
        coll = db[collname]  # creating collection

        for each in reader:
            coll.insert_one(each)

        return jsonify(f"Data inserted into the  collection: {collname} from {file} successfully.")

    except Exception as err:
        return jsonify('Error: ' + str(err))


@app.route('/mongodb/db/collection/readdata', methods=['POST'])
def read_data():
    if (request.method == 'POST'):
        localhost = request.json['localhost']
        port = request.json['port']
        db = request.json['dbname']
        collname = request.json['collection_name']

    try:
        client = pymongo.MongoClient(f"mongodb://{localhost}:{port}/")
        coll = client[db][collname]
        lst = []
        for i in coll.find():
            lst.append(i)
        return f"Data available in collection: {collname} is {lst}"

    except Exception as err:
        return jsonify('Error: ' + str(err))


@app.route('/mongodb/db/collection/updatedata', methods=['POST'])
def update_data():
    if (request.method == 'POST'):
        localhost = request.json['localhost']
        port = request.json['port']
        db = request.json['dbname']
        collname = request.json['collection_name']

        updatedcol = request.json['updatedcol']
        updatedval = request.json['updatedval']
        col2update = request.json['col2update']
        val2update = request.json['val2update']

    try:
        client = pymongo.MongoClient(f"mongodb://{localhost}:{port}/")
        coll = client[db][collname]
        coll.update_one({col2update: val2update},
                        {"$set": {updatedcol: updatedval}, "$currentDate": {"lastModified": True}})

        return (
            f"Value of column - {updatedcol} in the row having {col2update} : '{val2update}' \
            is updated to {updatedcol}:'{updatedval}'")

    except Exception as err:
        return jsonify('Error: ' + str(err))


@app.route('/mongodb/db/collection/downloaddata', methods=['POST'])
def download_data():
    import pandas as pd
    import csv
    if (request.method == 'POST'):
        localhost = request.json['localhost']
        port = request.json['port']
        db = request.json['dbname']
        collname = request.json['collection_name']

        file = request.json['filepath2download']

        try:
            client = pymongo.MongoClient(f"mongodb://{localhost}:{port}/")
            coll = client[db][collname]

            lst = [i for i in coll.find()]
            df = pd.DataFrame(lst)
            df.to_csv(file, index=False)
            return jsonify(f"Data of the collection: '{collname}' is successfully downloaded to {file}")

        except Exception as err:
            return jsonify('Error: ' + str(err))


@app.route('/mongodb/db/collection/deletedata', methods=['POST'])
def delete_data():
    if (request.method == 'POST'):
        localhost = request.json['localhost']
        port = request.json['port']
        db = request.json['dbname']
        collname = request.json['collection_name']

        col = request.json['colname']
        val = request.json['value']

        try:
            client = pymongo.MongoClient(f"mongodb://{localhost}:{port}/")
            coll = client[db][collname]
            coll.delete_one({col: val})

            return jsonify(f"record having {col} : {val} is deleted from {db}.{collname}")

        except Exception as err:
            return jsonify('Error: ' + str(err))


@app.route('/mongodb/db/dropcollection', methods=['POST'])
def drop_collection():
    if (request.method == 'POST'):
        localhost = request.json['localhost']
        port = request.json['port']
        db = request.json['dbname']
        collname = request.json['collection_name']

        try:
            client = pymongo.MongoClient(f"mongodb://{localhost}:{port}/")
            coll = client[db][collname]
            coll.drop()
            return jsonify(f"Collection: '{collname}' is dropped.")

        except Exception as err:
            return jsonify('Error: ' + str(err))


if __name__ == '__main__':
    app.run(debug=True)
