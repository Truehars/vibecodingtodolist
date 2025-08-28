from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

TODOS_FILE = 'todos.json'

def load_todos():
    if os.path.exists(TODOS_FILE):
        with open(TODOS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(TODOS_FILE, 'w') as f:
        json.dump(todos, f)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/todos')
def get_todos():
    return jsonify(load_todos())

@app.route('/add', methods=['POST'])
def add_todo():
    todos = load_todos()
    new_id = max([todo['id'] for todo in todos], default=0) + 1
    new_todo = {
        'id': new_id,
        'task': request.json['task'],
        'completed': False
    }
    todos.append(new_todo)
    save_todos(todos)
    return jsonify(new_todo)

@app.route('/toggle/<int:todo_id>', methods=['PUT'])
def toggle_todo(todo_id):
    todos = load_todos()
    for todo in todos:
        if todo['id'] == todo_id:
            todo['completed'] = not todo.get('completed', False)
            break
    save_todos(todos)
    return jsonify({'success': True})

@app.route('/delete/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    todos = load_todos()
    todos = [todo for todo in todos if todo['id'] != todo_id]
    save_todos(todos)
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True)