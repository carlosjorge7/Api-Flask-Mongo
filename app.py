from flask import Flask
from flask_pymongo import PyMongo
from flask_cors import CORS

# Connection
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost/api-rest-flask'
app.config['SECRET_KEY'] = 'secret'
mongo = PyMongo(app)

# settings (CORS?)
CORS(app)

# routes
from src.routes.tasksRoutes import *
from src.routes.userRoutes import *

# Init
if __name__ == '__main__':
    app.run(debug=True, port=5500)

