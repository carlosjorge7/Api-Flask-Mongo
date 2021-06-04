from app import app, mongo
from src.models.task import Task
from flask import request, jsonify, Response

from bson import json_util
from bson.objectid import ObjectId

from .verify import token_required

@app.route('/', methods=['GET'])
#@token_required
def welcome():
    return {'message': 'Welcome, API REST FLASK AND MONGODB'}

@app.route('/task', methods=['POST'])
#@token_required
def create_task():
    # Peticion
    name = request.json['name']
    description = request.json['description']
    status = request.json['status']

    task = Task(name, description, status)
    
    if name and description and status:
        id = mongo.db.tasks.insert(
            {'name': task.get_name(), 'description': task.get_description(), 'status': task.get_status()}
        )
        response = jsonify({
            '_id': str(id),
            'name': task.get_name(), 
            'description': task.get_description(), 
            'status': task.get_status()
        })
        response.status_code = 200
        return response
    else:
        return not_found()

# Middleware de verificacion de token
@app.route('/tasks', methods=['GET'])
#@token_required
def get_tasks():
    tasks = mongo.db.tasks.find()
    response = json_util.dumps(tasks)
    return Response(response, mimetype='application/json')

@app.route('/task/<id>', methods=['GET'])
#@token_required
def get_task(id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(id)})
    response = json_util.dumps(task)
    return Response(response, mimetype='application/json')

@app.route('/task/<id>', methods=['DELETE'])
#@token_required
def delete_task(id):
    mongo.db.tasks.delete_one({'_id': ObjectId(id)})
    response = jsonify({
        'message': 'Task whith ID : ' + id + ' eliminada'
    })
    return response

@app.route('/task/<id>', methods=['PUT'])
#@token_required
def update_task(id):
    name = request.json['name']
    description = request.json['description']
    status = request.json['status']

    task = Task(name, description, status)

    if name and description and status:
        mongo.db.tasks.update_one({'_id': ObjectId(id)}, {'$set': {
           'name': task.get_name(),
            'description': task.get_description(),
            'status': task.get_status()
        }})
        response = jsonify({'message': 'Task updated', status: 200})
        return response
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    response_err = jsonify({
        'message': 'Recurso no encontrado' + request.url,
        'status':404
    })
    response_err.status_code = 404
    return response_err


