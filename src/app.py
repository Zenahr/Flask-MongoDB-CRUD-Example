from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'secret'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/Users'

mongo = PyMongo(app)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/add', method=['POST'])
def add_user():
    json = request.json
    name = json['name'] 
    email = json['email'] 
    password = json['password'] 

    if name and email and password and request.method ==  'POST':
        password_hash = generate_password_hash(password)
        
        mongo.db.users.insert({
            'name':name,
            'email':email,
            'password':password_hash,
        })

        response = jsonify("User added.")
        response.status_code = 200
        return response

@app.errorhandler(404)
def not_found(error=None):
    error_message = {
        'status': 404,
        'message': 'Not Found' + request.url
    }
    error_response = jsonify(error_message)
    error_response.code = 404
    return error_message