from flask import Flask, jsonify, request, make_response, session
from flask_restful import Api, Resource
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from config import app, db
from models import User, Task, Todo
from datetime import datetime

migrate = Migrate(app, db)
api = Api(app)
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return '<h1>Welcome to Taskier!</h1>'


class Users(Resource):
    def get(self):
        users = User.query.all()
        user_list = [user.to_dict() for user in users]
        return jsonify(user_list)

    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Invalid request data'}), 400)

        password = data.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(username=data.get('username'), password=hashed_password, email=data.get('email'))
        user.created_at = datetime.now()

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        response = make_response(user.to_dict(), 201)
        return response


class UserById(Resource):
    def get(self, id):
        user = User.query.get(id)
        if user:
            return jsonify(user.to_dict())
        return {'error': 'User not found'}, 404

    def patch(self, id):
        user = User.query.get(id)
        if not user:
            return {'error': 'User not found'}, 404

        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Invalid request data'}), 400)

        for key, value in data.items():
            setattr(user, key, value)

        db.session.commit()

        return jsonify(user.to_dict())

    def delete(self, id):
        user = User.query.get(id)
        if not user:
            return {'error': 'User not found'}, 404

        db.session.delete(user)
        db.session.commit()

        return make_response(jsonify({'message': 'User deleted successfully'}), 200)


class Tasks(Resource):
    def get(self):
        tasks = Task.query.all()
        task_list = [task.to_dict() for task in tasks]
        return jsonify(task_list)

    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Invalid request data'}), 400)

        task = Task(**data)
        db.session.add(task)
        db.session.commit()

        return make_response(jsonify({'message': 'Task created successfully'}), 201)


class TaskById(Resource):
    def get(self, id):
        task = Task.query.get(id)
        if task:
            return jsonify(task.to_dict())
        return {'error': 'Task not found'}, 404

    def patch(self, id):
        task = Task.query.get(id)
        if not task:
            return {'error': 'Task not found'}, 404

        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Invalid request data'}), 400)

        for key, value in data.items():
            setattr(task, key, value)

        db.session.commit()

        return jsonify(task.to_dict())

    def delete(self, id):
        task = Task.query.get(id)
        if not task:
            return {'error': 'Task not found'}, 404

        db.session.delete(task)
        db.session.commit()

        return make_response(jsonify({'message': 'Task deleted successfully'}), 200)


class Todos(Resource):
    def get(self):
        todos = Todo.query.all()
        todo_list = [todo.to_dict() for todo in todos]
        return jsonify(todo_list)

    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Invalid request data'}), 400)

        todo = Todo(**data)
        db.session.add(todo)
        db.session.commit()

        return make_response(jsonify({'message': 'Todo created successfully'}), 201)


class TodoById(Resource):
    def get(self, id):
        todo = Todo.query.get(id)
        if todo:
            return jsonify(todo.to_dict())
        return {'error': 'Todo not found'}, 404

    def patch(self, id):
        todo = Todo.query.get(id)
        if not todo:
            return {'error': 'Todo not found'}, 404

        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Invalid request data'}), 400)

        for key, value in data.items():
            setattr(todo, key, value)

        db.session.commit()

        return jsonify(todo.to_dict())

    def delete(self, id):
        todo = Todo.query.get(id)
        if not todo:
            return {'error': 'Todo not found'}, 404

        db.session.delete(todo)
        db.session.commit()

        return make_response(jsonify({'message': 'Todo deleted successfully'}), 200)


class Signup(Resource):
    def post(self):
        data = request.get_json()
        if not data:
            return make_response(jsonify({'error': 'Invalid request data'}), 400)

        password = data.get('password')
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        user = User(username=data.get('username'), password=hashed_password, email=data.get('email'))
        user.created_at = datetime.now()

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id

        return make_response(jsonify({'message': 'User created successfully'}), 201)


# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return make_response(jsonify({'error': 'Invalid request data'}), 400)

    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user or not bcrypt.check_password_hash(user.password, password):
        return make_response(jsonify({'error': 'Invalid username or password'}), 401)

    session['user_id'] = user.id

    return make_response(jsonify({'message': 'Logged in successfully'}), 200)


# Logout endpoint
@app.route('/logout', methods=['POST'])
def logout():
    session.pop('user_id', None)  # Remove user ID from the session
    return make_response(jsonify({'message': 'Logged out successfully'}), 200)


api.add_resource(Users, '/users')
api.add_resource(UserById, '/users/<int:id>')
api.add_resource(Tasks, '/tasks')
api.add_resource(TaskById, '/tasks/<int:id>')
api.add_resource(Todos, '/todos')
api.add_resource(TodoById, '/todos/<int:id>')
api.add_resource(Signup, '/signup')


if __name__ == '__main__':
    app.run(port=5555, debug=True)
