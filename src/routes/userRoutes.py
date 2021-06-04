from app import app, mongo
from src.models.user import User
from flask import request, jsonify, make_response
import jwt
from datetime import datetime, timedelta

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json['username']
        password = request.json['password']

        us = User(username, password)
        user = mongo.db.users.find_one({'username': username, 'password': password})
        
        if us.get_username() and us.get_password():
            token = jwt.encode({'username': user['username'],
                'expiration': str(datetime.utcnow() + timedelta(seconds=120))
                },app.config['SECRET_KEY'])
        print(app.config['SECRET_KEY'])
        return jsonify({'token': token})
    except:
        return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
  
@app.route('/register', methods=['POST'])
def register():
    # Recibiendo datos
    username = request.json['username']
    password = request.json['password']

    user = User(username, password)

    if username and password:
        id = mongo.db.users.insert(
            {'username': user.get_username(), 'password': user.get_password() }
        )
        response = jsonify({
            '_id': str(id),
            'username': user.get_username(),
            'password': user.get_password()
        })
        response.status_code = 200
        return response
    else:
        return make_response('Could not verify!', 401, {'WWW-Authenticate' : 'Basic realm="Login Required"'})
