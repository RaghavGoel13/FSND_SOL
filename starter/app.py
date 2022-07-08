# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#

from flask import Flask, request, abort, jsonify
from flask_cors import CORS

from authenticar import requires_auth, AuthError
from models import Actors, Movies, setup_db


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

        #  ----------------------------------------------------------------
        #  Actors Controller
        #  ----------------------------------------------------------------

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actors.query.all()
        if not actors:
            abort(404, "No Actors were found in the database")
        else:
            actors_list = list(map(lambda actors: actors.get_actor, actors))
        return jsonify({
            "success": True,
            "actors": actors_list,
            "message": "actors retrieved successfully",
        }), 200

    @app.route('/actors/<int:id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor_by_id(payload, id):
        actor_by_id = Actors.query.get(id)
        if not actor_by_id:
            abort(404, 'Actor with id: ' + str(id) + ' could not be found.')
        else:
            actor_by_id_list = list(map(lambda actors: actors.get_actor, actor_by_id))
        return jsonify({
            "success": True,
            "actors": actor_by_id_list,
            "message": "actors retrieved successfully",
        }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        request_body = request.get_json()
        try:
            if request_body is None:
                abort(400, "Bad Request : Empty JSON Request")

            name = request_body.get('name', None)
            age = request_body.get('age', None)
            gender = request_body.get('gender', None)
            movie_id = request_body.get('movie_id', None)
            phone = request_body.get('phone', None)

            if name is None or age is None or gender is None or phone is None or movie_id is None:
                abort(400, "Bad Request : Missing field while adding new actor")

            actor = Actors(name=name, gender=gender, age=age, phone=phone, movie_id=movie_id);
            actor.add_actor()

        except BaseException:
            abort(400, "Bad Request : while inserting data to the database")

        return jsonify({
            "success": True,
            "message": "new actor inserted successfully"
        }), 201

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('update:actors')
    def update_actor(payload, id):
        actor_to_update = Actors.query.get(id)
        if not actor_to_update:
            abort(404, 'Actor with id: ' + str(id) + ' could not be found.')

        request_body = request.get_json()
        name = request_body.get('name', None)
        age = request_body.get('age', None)
        gender = request_body.get('gender', None)
        movie_id = request_body.get('movie_id', None)
        phone = request_body.get('phone', None)
        if name:
            actor_to_update.name = name
        if age:
            actor_to_update.age = age
        if gender:
            actor_to_update.gender = gender
        if movie_id:
            actor_to_update.movie_id = movie_id
        if phone:
            actor_to_update.phone = phone

        try:
            actor_to_update.update_actor()
        except BaseException:
            abort(400, "Bad formatted request due to unavailable movie id " + str(movie_id))

        return jsonify({
            "success": True,
            "updated": actor_to_update.get_actor,
            "message": "actor updated successfully"
        }), 201

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        actor_to_delete = Actors.query.filter(Actors.id == id).one_or_none()
        if not actor_to_delete:
            abort(404, 'Actor with id: ' + str(id) + 'not found in database')
        try:
            actor_to_delete.delete_actor()
        except BaseException:
            abort(400)

        return jsonify({
            "success": True,
            "message": 'Actor with id: ' + str(id) + ' deleted successfully'}), 200

    #  ----------------------------------------------------------------
    #  Movies Controller
    #  ----------------------------------------------------------------

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(payload):
        movies = Movies.query.all()
        if not movies:
            abort(404, "No movies were found in the database")
        else:
            movies_list = list(map(lambda movies: movies.get_movie, movies))
        return jsonify({
            "success": True,
            "movies": movies_list,
            "message": "movies retrieved successfully",
        }), 200

    @app.route('/movies/<int:id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie_by_id(payload, id):
        movie_by_id = Movies.query.get(id)
        if not movie_by_id:
            abort(404, 'Movie with id: ' + str(id) + ' could not be found.')
        else:
            movie_by_id_list = list(map(lambda movies: movies.get_movie, movie_by_id))
        return jsonify({
            "success": True,
            "movies": movie_by_id_list,
            "message": "movies retrieved successfully",
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        request_body = request.get_json()
        try:
            if request_body is None:
                abort(400)

            title = request_body.get('title', None)
            release_date = request_body.get('release_date', None)
            rating = request_body.get('rating', None)

            if title is None or release_date is None or rating is None:
                abort(400, "Bad Request-Missing field while adding new movie")

            movie = Movies(title=title, release_date=release_date, rating=rating)
            movie.add_movie()

        except BaseException:
            abort(400)

        return jsonify({
            "success": True,
            "message": "new movie inserted successfully"
        }), 201

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('update:movies')
    def update_movie(payload, id):
        movie_to_update = Movies.query.get(id)
        if not movie_to_update:
            abort(404, 'Movie with id: ' + str(id) + ' could not be found.')

        request_body = request.get_json()
        title = request_body.get('title', None)
        release_date = request_body.get('release_date', None)
        rating = request_body.get('rating', None)

        if title:
            movie_to_update.title = title
        if release_date:
            movie_to_update.release_date = release_date
        if rating:
            movie_to_update.rating = rating

        try:
            movie_to_update.update_movie()
        except BaseException:
            abort(400, "Bad formatted request due to unavailable movie id" + str(id))
        return jsonify({
            "success": True,
            "message": "movies updated successfully for movie id " + str(id)
        }), 201

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        movie_to_delete = Movies.query.filter(Movies.id == id).one_or_none()
        if not movie_to_delete:
            abort(404, 'Unable to found movie in database with id: ' + str(id))
        try:
            movie_to_delete.delete_movie()
        except BaseException:
            abort(400)

        return jsonify({
            "success": True,
            "message": 'Movie with id: ' + str(id) + ' deleted successfully'}), 200

    #  ----------------------------------------------------------------
    # Error Handling
    #  ----------------------------------------------------------------
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request'
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'Unathorized'
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False,
            "error": 405,
            "message": 'Method Not Allowed'
        }), 405

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error'
        }), 500

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable entity found"
        }), 422

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
