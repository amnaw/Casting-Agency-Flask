import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from flask_migrate import Migrate
from models import *
from flask_cors import CORS
from auth import AuthError, requires_auth

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__)
    setup_db(app)
  # Set up CORS. Allow '*' for origins. # CORS(app) basic
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  # The after_request dec set Access-Control-Allow  # CORS response headers
    @app.after_request
    def after_request(response):
        response.headers.add(
          'Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add(
          'Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')

        return response
    
  ############### Endpoints ##################  
    @app.route('/')
    def get():
      return jsonify({"greeting": "Hello World!"})
      
  # GET actors
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
      try:
        actorsTuple = Actor.query.order_by(Actor.id).all()
        actors = [actor.format() for actor in actorsTuple]
      except:
        abort(422)

      return jsonify({
            'success': True,
            'actors': actors
            }), 200
  
  # GET movies
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
      moviesTuple = Movie.query.order_by(Movie.id).all()
      movies = [movie.format() for movie in moviesTuple]

      return jsonify({
            'success': True,
            'movies': movies
            }), 200
  
  # DELETE actor
    @app.route('/actors/<id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(payload, id):
      try:
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
          abort(404)

        actor.delete()
                
        return jsonify({
            'success': True,
            'delete': id
            }), 200
      except:
        abort(422)
    
  # DELETE movie
    @app.route('/movies/<id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(payload, id):
      try:
        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
          abort(404)

        movie.delete()
                
        return jsonify({
            'success': True,
            'delete': id
            }), 200
      except:
        abort(422)
    
  # POST actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actor')
    def create_actor(payload):
        try:
          body = request.get_json()
          first_name = body.get('first_name', None)
          last_name = body.get('last_name', None)
          gender = body.get('gender', None)

          new_actor = Actor(
          first_name=first_name, 
          last_name=last_name, 
          gender=gender)

          new_actor.insert()

          return jsonify({
            'success': True,
            'actor_id': new_actor.id,
            'total_actors': len(Actor.query.all())
          }), 200
        
        except:
            abort(422)
      
  # POST movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movie')
    def create_movie(payload):
        try:
          body = request.get_json()

          title = body.get('title', None)
          release_date = body.get('release_date', None)
          rank = body.get('rank', None)

          new_movie = Movie(
          title=title, 
          release_date=release_date, 
          rank=rank)

          new_movie.insert()

          return jsonify({
            'success': True,
            'movie_id': new_movie.id,
            'total_movies': len(Movie.query.all())
          }), 200
        
        except:
            abort(422)
    
  # PATCH actor
    @app.route('/actors/<int:id>/edit', methods=['PATCH'])
    @requires_auth('patch:actor')
    def edit_actor(payload, id):
        try:
          body = request.get_json()
          first_name = body.get('first_name', None)
          last_name = body.get('last_name', None)
          gender = body.get('gender', None)

          # get actor id
          actor = Actor.query.filter(Actor.id == id).one_or_none()
          if actor is None:
            abort(404)

          # set its 3 value
          if first_name:
             actor.first_name = first_name
          if last_name:
             actor.last_name = last_name
          if gender:
             actor.gender = gender
          
          # save the update
          if first_name or last_name or gender:
            actor.update()
            return jsonify({
              'success': True,
              'actor_id': actor.id,
              'total_actors': len(Actor.query.all())
            }), 200
        
        except:
            abort(422)
    
  # PATCH movie
    @app.route('/movies/<int:id>/edit', methods=['PATCH'])
    @requires_auth('patch:movie')
    def edit_movie(payload, id):
        try:
          body = request.get_json()

          title = body.get('title', None)
          release_date = body.get('release_date', None)
          rank = body.get('rank', None)

          movie = Movie.query.filter(Movie.id == id).one_or_none()
          if movie is None:
            abort(404)

          if title:
            movie.title = title
          if release_date:
            movie.release_date = release_date
          if rank:
            movie.rank = rank
          
          # save the update
          if title or release_date or rank:
            movie.update()
            return jsonify({
              'success': True,
              'movie_id': movie.id,
              'total_movies': len(Movie.query.all())
            }), 200
        
        except:
            abort(422)
     
  # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }), 422


    @app.errorhandler(404)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource not Found"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False, 
            "error": 400,
            "message": "Bad Request"  
            }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False, 
            "error": 405,
            "message": "Method not Allowed"   
            }), 405

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "success": False, 
            "error": 500,
            "message": "Server Error"   
            }), 500

    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({
            "success": False, 
            "error": 401,
            "message": "Unauthorized"   
            }), 401
    
    @app.errorhandler(403)
    def unauthorized_error(error):
        return jsonify({
            "success": False, 
            "error": 403,
            "message": "Forbidden"   
            }), 403

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False, 
            "error": error.status_code,
            "message": "AuthError"   
            }), error.status_code

    return app

app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)