from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Actor, Movie


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route('/')
    def index():
        return 'not implemented'

    return app


app = create_app()

RESULTS_PER_PAGE = 10


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization,true")
    response.headers.add("Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,PATCH,OPTIONS")
    return response


def get_paginated(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE
    results = [s.format() for s in selection]

    return results[start:end]


@app.route('/actors')
def get_actors():
    actors = Actor.query.order_by(Actor.name).all()
    selected_actors = get_paginated(request, actors)
    if len(selected_actors) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'actors': selected_actors,
        'total_actors': len(actors),
        'actors_displayed': len(selected_actors)
    })


@app.route('/actors', methods=['POST'])
def add_actor():
    body = request.get_json()
    name = body['name']
    birthdate = body['birthdate']
    gender = body['gender']
    seeking_work = bool(body['seekingWork'])

    try:
        new_actor = Actor(
            name=name,
            birthdate=birthdate,
            gender=gender,
            seeking_work=seeking_work
        )
        new_actor.insert()
    except Exception:
        abort(422)
    return jsonify({
        'success': True,
        'id': new_actor.id,
        'total_actors': len(Actor.query.all())
    })

# @app.route('/actors/<int:actor_id>', methods=['PATCH'])
# def modify_actor(actor_id):
#     actor = Actor.query.filter(Actor.id=actor_id).one_or_none()
#     if actor is None:
#         abort(404)
    
#     body = request.get_json()
#     name = body['name']
#     birthdate = body['birthdate']
#     gender = body['gender']
#     seeking_work = bool(body['seekingWork'])

#     try:



@app.route('/movies')
def get_movies():
    movies = Movie.query.order_by(Movie.title).all()
    seleted_movies = get_paginated(request, movies)

    if len(seleted_movies) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'movies': seleted_movies,
        'total_movies': len(movies),
        'movies_displayed': len(seleted_movies)
    })


@app.route('/movies', methods=['POST'])
def add_movie():
    body = request.get_json()
    title = body['title']
    release_date = body['releaseDate']
    genre = body['genre']

    try:
        new_movie = Movie(
            title=title,
            release_date=release_date,
            genre=genre
            )
        new_movie.insert()
    except Exception:
        abort(422)

    return jsonify({
        'success': True,
        'id': new_movie.id,
        'total_movies': len(Movie.query.all())
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
