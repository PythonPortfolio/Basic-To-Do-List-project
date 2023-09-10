from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):     # function that returns a string when we create a new element
        return '<Task %r>' % self.id  # will return 'Task' + it the id of the task

with app.app_context():
    db.create_all()

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']  # new variable assigned to input (content list)
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'  # error  message

    else:
        tasks = Todo.query.order_by(Todo.date_created).all()  # looks  at all database contents, and return them ordered by date created
        return render_template('index.html', tasks=tasks)


if __name__ == "__main__":
    app.run(debug=True)
