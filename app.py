from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    user_name = 'kaizhou'
    current_tasks = [
        'Learn Flask routing',
        'Understand templates',
        'Build a task tracker',
    ]
    return render_template('index.html', name=user_name, tasks=current_tasks)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/task/<int:task_id>')
def show_task(task_id):

    MIN_TASK_ID = 1
    MAX_TASK_ID = 10

    if task_id < MIN_TASK_ID:
        return redirect(url_for('show_task', task_id=MIN_TASK_ID))
    
    if task_id > MAX_TASK_ID:
        return redirect(url_for('show_task', task_id=MAX_TASK_ID))

    task = {
        'id': task_id,
        'title': f'Task number {task_id}',
        'description': 'This is a placeholder task description.'
    }
    return render_template('task.html', task=task)

if __name__ == '__main__':
    app.run(debug=True, port=5001)