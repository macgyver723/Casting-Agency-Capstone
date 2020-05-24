from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth

# https://fsnd-stefan.auth0.com/authorize?audience=casting-agency&response_type=token&client_id=MKNzsmrLb5LVoFNvHBaR53rkIE0f5TGm&redirect_uri=http://0.0.0.0:8080/callback
'''
jwts
Casting Assistant:
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhiZXQ0WlRvaTE2bzUyRXd4ZENoRSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc3RlZmFuLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWM5NWRmN2VlNTZjNDBjNmQ4MTY2NjAiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU5MDMzOTM3NSwiZXhwIjoxNTkwMzQ2NTc1LCJhenAiOiJNS056c21yTGI1TFZvRk52SEJhUjUzcmtJRTBmNVRHbSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.GHowFCUeRtlft0UATpP91KNtsWSLPABt0B_qsV3GItmGsqTkSOCsV0X7sTZx2ZjAMbusKM04g3UO6oNafTLZncveXD0vCcvVFM3vVIVSJ8iApfW4QvSBxqNrSLZYZEHxYTDpPrcHCv1y6oV_Ay-jsA9C050_8qsN_NVr1gJJoa92X1ySG-g761e6qPm6GihJfuI6D68tIb_FWboT7Y5notr-HQ2FWrZnDnAIUzuR0FGQhp8QLgzDRgRw1EDxUjfWgIL9vumb_s3I_UTK1VI9KVbt7oyMX9HB3sYvkKDiSGVaWNSH7nV9qLsE90Z7_TDmPXWp9v_tIj9zLNMXcj4V3w
Casting Director:
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhiZXQ0WlRvaTE2bzUyRXd4ZENoRSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc3RlZmFuLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWM5NWUxZGVlNTZjNDBjNmQ4MTY2ZDUiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU5MDM0MDE5MCwiZXhwIjoxNTkwMzQ3MzkwLCJhenAiOiJNS056c21yTGI1TFZvRk52SEJhUjUzcmtJRTBmNVRHbSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImRlbGV0ZTphY3RvciIsImVkaXQ6YWN0b3JzIiwiZWRpdDptb3ZpZXMiLCJyZWFkOmFjdG9ycyIsInJlYWQ6bW92aWVzIl19.FvEnFQoCLPMBH7yTs-KlxFQuJpaaFiaM162Q2TdKrCgbb_nplpC0u3vvh8JKL8uGbsc1IE0V-EqwTO1I6nE07Hza9CxUbJErdUAeGkyUJK7uc2sF4nKjCxr4u66RluRIuS4HyRJ1E49HnpTkBXes_ylC4b_WAjAKkpUBesoFIX9-VkywnTEtpR90HAaktp3KxibyWzMTBJFQH6O_9Lg0WnAGhWjqLVhGXuA-39rbcajiMpACiqz8YHIAh4MSvPtnS_zmX4ShIOZWQ6pY96vnoZMnSY0tu-CjjFB-5nJYiAo2DMTDGPEAYq5OAWWruhG9jilN_hz2QIcWwRMI0zy-YQ
Executive Producer:
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkhiZXQ0WlRvaTE2bzUyRXd4ZENoRSJ9.eyJpc3MiOiJodHRwczovL2ZzbmQtc3RlZmFuLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZWM5NWUzOWVlNTZjNDBjNmQ4MTY3MTkiLCJhdWQiOiJjYXN0aW5nLWFnZW5jeSIsImlhdCI6MTU5MDM0MDI4MiwiZXhwIjoxNTkwMzQ3NDgyLCJhenAiOiJNS056c21yTGI1TFZvRk52SEJhUjUzcmtJRTBmNVRHbSIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiYWRkOmFjdG9ycyIsImFkZDptb3ZpZXMiLCJkZWxldGU6YWN0b3IiLCJkZWxldGU6bW92aWUiLCJlZGl0OmFjdG9ycyIsImVkaXQ6bW92aWVzIiwicmVhZDphY3RvcnMiLCJyZWFkOm1vdmllcyJdfQ.KmFC65lb_yS6uNp4UuIGqNRZxteTXrsPWF3NIHkghKyAn-SKDCu--cY-mNbFvrVde0eipCzywe6NZ_iyQSXd4Fk6MgkJKeH_BNpoH_U5crBe98LMRShN-r1OFgOS3BHdZ3U0mwUoDCdVyLz6Za0x53oKGAqzsk-ZWb2mTE0CZiwGuIJvc2Tjs_cbxT1Xnh2XK4lLUr0RtaFisJsefiG444QVOgZ1sqAqvNmSFDzDZuzL860YGKIx9RRmxEcfDbq04VFBTq9Ey8z76ui_t91TGOkoSeRIvonIsrm5SK4CVi0qrlyqfuYTdy_2yw-FgYzFPGPD8v3wtubYtJoG0cw8YA
'''


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
    response.headers.add(
        "Access-Control-Allow-Headers",
        "Content-Type,Authorization,true"
        )
    response.headers.add(
        "Access-Control-Allow-Methods",
        "GET,PUT,POST,DELETE,PATCH,OPTIONS"
        )
    return response


def get_paginated(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * RESULTS_PER_PAGE
    end = start + RESULTS_PER_PAGE
    results = [s.format() for s in selection]

    return results[start:end]


@app.route('/actors')
@requires_auth('read:actors')
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
@requires_auth('add:actors')
def add_actor():
    data = request.get_json()
    name = data.get('name', None)
    birthdate = data.get('birthdate', None)
    gender = data.get('gender', None)
    seeking_work = bool(data.get('seekingWork', None))

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


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('edit:actors')
def edit_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)

    data = request.get_json()
    name = data.get('name', None)
    birthdate = data.get('birthdate', None)
    gender = data.get('gender', None)
    seeking_work = data.get('seekingWork', None)

    try:
        actor.name = name if name else actor.name
        actor.dirthdate = birthdate if birthdate else actor.birthdate
        actor.gender = gender if gender else actor.gender
        actor.seeking_work = bool(seeking_work) if seeking_work \
            else actor.seeking_work
        actor.update()
    except Exception:
        abort(422)

    return jsonify({
        'success': True,
        'updated_actor': actor.format()
    })


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(actor_id):
    actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
    if actor is None:
        abort(404)

    deleted_name = actor.name
    actor.delete()

    return jsonify({
        'success': True,
        'deleted_name': deleted_name
    })


@app.route('/movies')
@requires_auth('read:movies')
def get_movies():
    movies = Movie.query.order_by(Movie.genre).all()
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
@requires_auth('add:movies')
def add_movie():
    data = request.get_json()
    title = data.get('title', None)
    release_date = data.get('releaseDate', None)
    genre = data.get('genre', None)

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


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('edit:movies')
def edit_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)

    data = request.get_json()
    title = data.get('title', None)
    release_date = data.get('releaseDate', None)
    genre = data.get('genre', None)

    try:
        movie.title = title if title else movie.title
        movie.release_date = release_date if release_date \
            else movie.release_date
        movie.genre = genre if genre else movie.genre
        movie.update()
    except Exception:
        abort(422)

    return jsonify({
        'success': True,
        'updated_movie': movie.format()
    })


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(movie_id):
    movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
    if movie is None:
        abort(404)

    deleted_title = movie.title
    movie.delete()

    return jsonify({
        'success': True,
        'deleted_title': deleted_title
    })


@app.errorhandler(AuthError)
def not_found(error):
    return jsonify({
        "success": False,
        'error': error.status_code,
        'message': error.error
    }), error.status_code


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
