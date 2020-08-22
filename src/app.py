from flask import Flask, jsonify, request, Response
from pymongo import MongoClient
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
client = MongoClient()
db = client.anime
collection = db.anime

@app.route('/api/v1/anime/add', methods=['POST'])
def add_item():
    json = request.json
    anime = json['anime'] 
    season = json['season'] 
    episode = json['episode']
    rating = json['rating']

    if request.method ==  'POST' and anime and season and episode and rating:

        payload = {
            'anime': json['anime'], 
            'season': json['season'], 
            'episode': json['episode'],
            'rating': json['rating'],
        }

        collection.insert_one(payload)
        response = dumps(payload)
        return Response(response, status=200, mimetype='application/json')

@app.route('/api/v1/anime', methods=['GET'])
def items():
    return Response(dumps(collection.find()), mimetype='application/json')

@app.route('/api/v1/anime/<anime_id>', methods=['GET', 'DELETE'])
def item(item_id):
    if request.method ==  'GET':
        response = dumps(collection.find_one({'_id': ObjectId(item_id)}))
        print(response)
        return Response(response, status=200, mimetype='application/json')
    if request.method ==  'DELETE': # TODO: check if user exists and tell in response, otherwise delete.
        collection.delete_one({'_id': ObjectId(item_id)})
        return Response("Entry deleted.", status=200, mimetype='text/plain')


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

