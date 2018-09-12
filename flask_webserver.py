from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth


# 确保 web service 安全服务 要求客户端提供一个用户名和密码
auth = HTTPBasicAuth()


# 回调函数 Flask-HTTPAuth 使用它来获取给定用户的密码 校验 dyx-0405
@auth.get_password
def get_password(username):
    if username == 'dyx':
        return '0405'
    return None


# 回调函数是用于给客户端发送未授权错误代码
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 403)


tasks = [
    {
        'id': 1,
        'title': 'Buy something',
        'description': 'milk, apple, pizza, fruit',
        'done': False
    },
    {
        'id': 2,
        'title': 'learn python',
        'description': 'learn how to use flask',
        'done': False
    }
]


app = Flask(__name__)


# 404 错误处理程序
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': "Not found"}), 404)


# 查询所有todo list
@app.route('/todo/api/v1.0/tasks', methods=['GET'])
@auth.login_required
def get_tasks():
    return jsonify({'task': tasks})


# 查询某一项todo
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def get_task(task_id):
    task_iterator = filter(lambda t: t['id'] == task_id, tasks)
    task = list(task_iterator)
    if len(task) == 0:
        abort(404)
    return jsonify({'task': task[0]})


# 增加一项todo
@app.route('/todo/api/v1.0/tasks', methods=['POST'])
@auth.login_required
def create_task():
    if not request.json or 'title' not in request.json:
        abort(400)
    task = {
        'id': tasks[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'done': False
    }
    tasks.append(task)
    return jsonify({'task': task}), 201


# 修改一项todo
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def update_task(task_id):
    task_iterator = filter(lambda t: t['id'] == task_id, tasks)
    task = list(task_iterator)
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != str:
        abort(400)
    if 'description' in request.json and type(request.json['description']) is not str:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    return jsonify({'task': task[0]})


# 删除一项todo
@app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
@auth.login_required
def delete_task(task_id):
    task_iterator = filter(lambda t: t['id'] == task_id, tasks)
    task = list(task_iterator)
    if len(task) == 0:
        abort(400)
    tasks.remove(task[0])
    return jsonify({'result': True})


if __name__ == '__main__':
    app.run(debug=True)
