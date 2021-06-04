from app import app, mongo
from flask import jsonify, request
import jwt
from functools import wraps

from bson.objectid import ObjectId

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 403
        try: 
            data = jwt.decode(token, app.config['SECRET_KEY'])
            #current_user = User.query.filter_by(public_id=data['public_id']).first()
            current_user = mongo.db.users.find_one({'_id': ObjectId('60b8b3d0b47f2b50813ec250')})
        except:
            return jsonify({'message' : 'Token is invalid!'}), 403
            
        return f(current_user, *args, **kwargs)
    return decorated