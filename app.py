import os
from flask import Flask, request, abort, jsonify, render_template
from flask_cors import CORS

from models import setup_db, Actor, Movie
from auth import AuthError, requires_auth


def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    @app.route('/')
    def index():
        return render_template("index.html", login_url=os.environ['LOGIN_URL'])

    @app.route('/home')
    def home():
        return render_template('home.html')

    @app.route('/favicon.ico')
    def favicon():
        return ""

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

    @app.route('/actors')
    @requires_auth('read:actors')
    def get_actors():
        selected_actors = Actor.query.order_by(Actor.name).all()
        selected_actors = [s.format() for s in selected_actors]
        if len(selected_actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': selected_actors,
            'total_actors': len(selected_actors),
        })

    @app.route('/actors/<int:actor_id>')
    @requires_auth('read:actors')
    def get_actor(actor_id):
        actor = Actor.query.filter(Actor.id == actor_id).one_or_none()

        if actor is None:
            abort(404)

        return jsonify({
            'success': True,
            'actor': actor.format()
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
                name=name.title(),
                birthdate=birthdate,
                gender=gender,
                seeking_work=seeking_work
            )
            new_actor.insert()
        except Exception as e:
            print(f"Exception {e} in add new actor")
            abort(422)
        return jsonify({
            'success': True,
            'id': new_actor.id,
            'total_actors': len(Actor.query.all()),
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
            actor.birthdate = birthdate if birthdate else actor.birthdate
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
        movies = [m.format() for m in movies]
        if len(movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': movies,
            'total_movies': len(movies),
        })

    @app.route('/movies/<int:movie_id>')
    @requires_auth('read:movies')
    def get_movie(movie_id):
        movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
        if movie is None:
            abort(404)
        return jsonify({
            'success': True,
            'movie': movie.format()
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
                title=title.title(),
                release_date=release_date,
                genre=genre.title()
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
            movie.title = title.title() if title else movie.title
            movie.release_date = release_date if release_date \
                else movie.release_date
            movie.genre = genre.title() if genre else movie.genre
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
    def auth_error(error):
        return jsonify({
            "success": False,
            'error': error.status_code,
            'message': error.error
        }), error.status_code

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Not Found"
        }),

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
