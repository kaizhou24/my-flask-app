from flask import Flask, render_template, redirect, url_for, request
from math import ceil

app = Flask(__name__)

PER_PAGE = 5
USER_NAME = 'kaizhou'
SAMPLE_TASKS = [
    {'id': i, 'title': f'Task {i}', 'description': f'Description for task {i}'}
    for i in range(1, 27)
]
MIN_TASK_ID, MAX_TASK_ID = 1, len(SAMPLE_TASKS)
MIN_PAGE, MAX_PAGE = 1, ceil(len(SAMPLE_TASKS) / PER_PAGE)

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)

    if page < MIN_PAGE:
        return redirect(url_for('index', page=MIN_PAGE))
    
    if page > MAX_PAGE:
        return redirect(url_for('index', page=MAX_PAGE))

    start, end = get_pagination_index(page, PER_PAGE)
    paginated_tasks = SAMPLE_TASKS[start:end]

    context = {
        'name': USER_NAME,
        'tasks': paginated_tasks,
        'page': page,
        'total_tasks': len(SAMPLE_TASKS),
        'total_pages': MAX_PAGE,
        'has_prev': page > 1,
        'has_next': page < MAX_PAGE,
        'start': start,
        'end': min(end, len(SAMPLE_TASKS))
    }

    return render_template('index.html', **context)

def get_pagination_index(page, per_page):
    start_index = (page - 1) * per_page
    end_index = start_index + per_page
    return (start_index, end_index)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/task/<int:task_id>')
def show_task(task_id):

    if task_id < MIN_TASK_ID:
        return redirect(url_for('show_task', task_id=MIN_TASK_ID))
    
    if task_id > MAX_TASK_ID:
        return redirect(url_for('show_task', task_id=MAX_TASK_ID))

    task = {
        'id': task_id,
        'title': f'Task {task_id}',
        'description': 'This is a placeholder task description.',
        'has_previous': task_id > MIN_TASK_ID,
        'has_next': task_id < MAX_TASK_ID,
        'previous_id': task_id - 1 if task_id > MIN_TASK_ID else None,
        'next_id': task_id + 1 if task_id < MAX_TASK_ID else None
    }
    return render_template('task.html', task=task)

if __name__ == '__main__':
    app.run(debug=True, port=5001)