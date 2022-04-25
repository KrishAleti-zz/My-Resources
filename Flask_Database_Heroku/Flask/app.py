""" We can get the code snippets for flask-database usage from te below urls:
https://flask.palletsprojects.com/en/2.1.x/quickstart/
https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application """

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy  # importing sqlalchemy
from datetime import datetime
import pymysql
# import mysql.connector as connection

app = Flask(__name__)

"""Database configuration - code snippet:- https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/"""

# configuring the database
# app.config['SQLALCHEMY_DATABASE_URI'] = mysql://username:password@server/db -> defining the mysql database
"""The database which we are giving here needs to be created in the sql workbench 1st"""
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:MySQL123@localhost/flaskdb"

"""getting module not found error for mysql db, hence we are using pymysql
 https://stackoverflow.com/questions/454854/no-module-named-mysqldb
we need to edit the SQLAlchemy URL schema like this: mysql+pymysql://username:passwd@host/database 
as we are installed PyMySQL"""

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MySQL123@127.0.0.1:3306/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # initializing the database

"""defining the class to create the table and defining the columns of the taable:-
https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/#a-minimal-application
https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/"""

class Todo(db.Model):  # creating the table - class name: Todo is the table name
    # defining the columns
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    desc = db.Column(db.String(200))
    data_of_creation = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Todo('{self.sno}', '{self.title}')"
"""Usage of __repr__: When the object of Todo class is printed, the __repr__ function will be automatically executed and 
it will return the values of the sno,title """
"""As we had given the sno. filed as int type and primary key, the database (mysql) will automatically 
give the integer number to that field and it will be incremented automatically starting from 1.
https://retool.com/blog/how-to-work-with-auto-incrementing-ids-in-sql/  """

"""Inserting values in the database:-
https://flask-sqlalchemy.palletsprojects.com/en/2.x/queries/?highlight=insert"""
@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo = Todo(title=title, desc=desc)  # instantiating the class - Todo and passing the values
        db.session.add(todo)  # adding the object to the database
        db.session.commit()  # committing the changes to the database
    todolist = Todo.query.all()  # fetching all the data from the table
    return render_template("index.html", todolist=todolist)


@app.route("/show")
def about():
    todolist = Todo.query.all()  # fetching all the data from the table
    print(todolist)
    return str(todolist)


@app.route('/delete/<string:sno>')
def delete(sno):
    todel = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todel)
    db.session.commit()
    return redirect('/')


@app.route("/update")
def update():
    todolist = Todo.query.all()  # fetching all the data from the table
    print(todolist)
    return str(todolist)


if __name__ == "__main__":
    app.run(debug=True)  # debug=True --- this shows the error message in the browser itself (if any)

# can also run the app from the cmd using python app.run
# https://stackoverflow.com/questions/62847282/heroku-error-could-not-install-packages-due-to-an-environmenterror-errno-2-n

