# MySQL Database with Flask

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy  # importing sqlalchemy
from datetime import datetime
import pymysql


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:MySQL123@127.0.0.1:3306/flaskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)  # initializing the database


class Todo(db.Model):  # creating the table
    # defining the columns
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    desc = db.Column(db.String(200))
    data_of_creation = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Todo('{self.sno}', '{self.title}')"

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

