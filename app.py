from flask import Flask, render_template, request
import json
import os


app = Flask(__name__)
FILE_PATH = "tasks.json"

def load_tasks():
    if os.path.exists(FILE_PATH):
        with open(FILE_PATH, "r") as file:
            return json.load(file)
    return {}

def save_tasks(tasks):
    with open(FILE_PATH, "w") as file:
        json.dump(tasks, file)

dic = load_tasks()

@app.route('/', methods=['GET','POST'])
def calc(input=False):
    if request.method == 'POST':
        if "task" in request.form and "deadline" in request.form:
            task = request.form["task"]
            deadline = request.form["deadline"]
            dic[task] = {"deadline": deadline, "done": False}
        elif "delete" in request.form:
            task = request.form["delete"]
            del dic[task]
        elif "done" in request.form:
            task = request.form["done"]
            dic[task]["done"] = True
        save_tasks(dic)
    return render_template('main.html', dic=dic)
