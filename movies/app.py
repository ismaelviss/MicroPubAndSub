from bson import ObjectId
from flask import Flask, request, jsonify
from flask_jwt import jwt_required, current_identity

from shared.auth import jwt
from .db import db_client

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Bruce Wayne is Batman'
jwt.init_app(app)


@app.route('/movies/')
def movies_list():
    results = db_client.movies.find()
    movies = []
    for result in results:
        movies.append({
            'id': str(result['_id']),
            'title': result['title']
        })
    return jsonify(movies)


@app.route('/movies/<string:movie_id>')
def movie_detail(movie_id):
    result = db_client.movies.find_one({'_id': ObjectId(movie_id)})
    if result is None:
        return jsonify({'error': 'Movie not found'}), 404
    movie = {
        'id': str(result['_id']),
        'title': result['title'],
        'description': result['title'],
        'rating': result['rating'],
        'reviews': result['reviews'],
    }
    return jsonify(movie)

