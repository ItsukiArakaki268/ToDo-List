from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# A dictionary to store tasks, categorized by list names
todo_lists = {
    '課題': [],
    'やること': [],
    '買うもの': []
}

@app.route('/')
def index():
    return render_template('index.html', todo_lists=todo_lists)

@app.route('/list/<list_name>')
def view_list(list_name):
    tasks = todo_lists.get(list_name, [])
    return render_template('list.html', list_name=list_name, tasks=tasks)

@app.route('/add_list', methods=['GET', 'POST'])
def add_list():
    if request.method == 'POST':
        list_name = request.form.get('list_name')
        if list_name and list_name not in todo_lists:
            todo_lists[list_name] = []
        return redirect(url_for('index'))
    return render_template('add_list.html')

@app.route('/add_task/<list_name>', methods=['GET', 'POST'])
def add_task(list_name):
    if request.method == 'POST':
        task = request.form.get('task')
        if task:
            todo_lists[list_name].append({'task': task, 'completed': False})
        return redirect(url_for('view_list', list_name=list_name))
    return render_template('add_task.html', list_name=list_name)

@app.route('/delete_task/<list_name>/<int:task_id>', methods=['POST'])
def delete_task(list_name, task_id):
    if list_name in todo_lists and 0 <= task_id < len(todo_lists[list_name]):
        todo_lists[list_name].pop(task_id)
    return redirect(url_for('view_list', list_name=list_name))

@app.route('/complete_task/<list_name>/<int:task_id>', methods=['POST'])
def complete_task(list_name, task_id):
    if list_name in todo_lists and 0 <= task_id < len(todo_lists[list_name]):
        todo_lists[list_name][task_id]['completed'] = not todo_lists[list_name][task_id]['completed']
    return redirect(url_for('view_list', list_name=list_name))

if __name__ == '__main__':
    app.run(debug=True)
