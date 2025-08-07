from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from math import ceil

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    created_on = db.Column(db.DateTime, default=db.func.now())
    due_date = db.Column(db.Date, nullable=True)

def populate_sample_data():
    if Task.query.count() == 0:
        tasks = [Task(subject=f"Task {i}", description=f"Description for task {i}") 
                 for i in range(1, 30)]
        db.session.add_all(tasks)
        db.session.commit()
        print(f"Created {len(tasks)} tasks")  # Keep this for now

PER_PAGE = 5
USER_NAME = 'kaizhou'

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)

    pagination = Task.query.paginate(page=page, per_page=PER_PAGE, error_out=False)

    context = {
        'name': USER_NAME,
        'tasks': pagination.items,
        'page': pagination.page,
        'total_tasks': pagination.total,
        'total_pages': pagination.pages,
        'has_prev': pagination.has_prev,
        'has_next': pagination.has_next,
        'start': (pagination.page - 1) * PER_PAGE + 1,
        'end': min(pagination.page * PER_PAGE, pagination.total)
    }

    return render_template('index.html', **context)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/task/<int:task_id>')
def show_task(task_id):
    task = Task.query.get_or_404(task_id)
    previous_task = Task.query.filter(Task.id < task_id).order_by(Task.id.desc()).first()
    next_task = Task.query.filter(Task.id > task_id).order_by(Task.id.asc()).first()

    context = {
        'task': task,
        'has_previous': bool(previous_task),
        'previous_id': previous_task.id if previous_task else None,
        'has_next': bool(next_task),
        'next_id': next_task.id if next_task else None,
    }

    return render_template('task.html', **context)

with app.app_context():
    db.create_all()
    populate_sample_data()

if __name__ == '__main__':
    app.run(debug=True, port=5001)