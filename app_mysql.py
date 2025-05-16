from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

DB_user_name = 'python_user'
DB_pass = 'password123'
DB_address = 'localhost'


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_user_name}:{DB_pass}@{DB_address}/TestDB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    due_date = db.Column(db.DateTime, nullable=True)
    done = db.Column(db.Boolean, default=False, nullable=False)

with app.app_context():
    db.create_all()

def load_tasks():
    dic = {}
    tasks = Task.query.all()
    for task in tasks:
        dic[task.name] = {"deadline": task.due_date, "done": task.done}
    return dic


def save_tasks(tasks):
    pass


@app.route('/', methods=['GET','POST'])
def calc(input=False):
    if request.method == 'POST':
        if "task" in request.form and "deadline" in request.form:
            task = request.form["task"]
            deadline = request.form["deadline"]
            new_task = Task(name = task, due_date=deadline)
            db.session.add(new_task)
            db.session.commit()
        elif "delete" in request.form:
            task = request.form["delete"]
            task_to_del = Task.query.filter(Task.name == task).first()
            if task_to_del:
                db.session.delete(task_to_del)
                db.session.commit()
        elif "done" in request.form:
            task = request.form["done"]
            done_task = Task.query.filter(Task.name == task).first()
            if done_task:
                done_task.done = True
                db.session.commit()
    dic = load_tasks()
    return render_template('main.html', dic=dic)
