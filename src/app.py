from flask import Flask, jsonify, request, Response
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Users'

mongo = PyMongo(app)

@app.route('/api/v1/add', methods=['POST'])
def add_user():
    json = request.json
    name = json['name'] 
    email = json['email'] 
    password = json['password'] 

    if name and email and password and request.method ==  'POST':
        password_hash = generate_password_hash(password)
        
        payload = {
            'name':name,
            'email':email,
            'password':password_hash,
        }
        mongo.db.users.insert_one(payload)
        del payload['_id']
        del payload['password']
        payload.update({'status_code':200})
        response = dumps(payload)
        return Response(response, mimetype='application/json')

@app.route('/api/v1/users', methods=['GET'])
def users():
    return Response(dumps(mongo.db.users.find()), mimetype='application/json')

@app.errorhandler(404)
def not_found(error=None):
    error_message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }
    error_response = jsonify(error_message)
    error_response.code = 404
    return error_message

if __name__ == '__main__':
    app.run(debug=True)

