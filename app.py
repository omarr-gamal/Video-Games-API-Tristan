#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import datetime
from operator import ne
from os import abort, name
import dateutil.parser
import babel
from flask import (Flask, request, jsonify,
                   Response, flash, redirect, url_for)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from flask_migrate import Migrate
from logging import Formatter, FileHandler, log
from models import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.app = app
db.init_app(app)
db.create_all()

migrate = Migrate(app, db)

#----------------------------------------------------------------------------#
# api routes.
#----------------------------------------------------------------------------#


@ app.route('/')
def index():
    return jsonify({
        'is it working?': 'yes',
    })


@ app.route('/games', methods=['GET'])
def get_games():
    try:
        games = db.session.query(
            Game.id, Game.name, Game.description, Game.release_date, Game.released, Game.rating,
            Game.critic_rating, Game.PEGI_rating, Game.genres, Game.developer, Game.publisher).all()
    except:
        abort(422)

    data = [{
        "name": game.name,
        "description": game.description,
        "release_date": game.release_date,
        "released": game.released,
        "rating": game.rating,
        "critic_rating": game.critic_rating,
        "PEGI_rating":  game.PEGI_rating,
        "genres": game.genres,
        "developer": game.developer,
        "publisher": game.publisher
    } for game in games]

    return jsonify({
        'success': True,
        'games': data,
    })


@ app.route('/games/<int:game_id>', methods=['GET'])
def get_game_by_id():
    try:
        body = request.get_json()
    except:
        abort(422)

    game_id = body.get('id', None)

    if game_id is None:
        abort(422)

    game = Game.query.filter(
        Game.id == game_id).one_or_none()
    if game is None:
        abort(404)

    data = {
        "name": game.name,
        "description": game.description,
        "release_date": game.release_date,
        "released": game.released,
        "rating": game.rating,
        "critic_rating": game.critic_rating,
        "PEGI_rating":  game.PEGI_rating,
        "genres": game.genres,
        "developer": game.developer,
        "publisher": game.publisher
    }
    return jsonify({
        'success': True,
        'game': data,
    })


@ app.route('/games', methods=['POST'])
def post_game():
    body = request.get_json()
    try:
        new_name = body.get('name', None)
        new_description = body.get('description', None)

        new_release_date = body.get('release_date', None)
        new_released = True
        # (datetime.datetime.strptime(
        #     new_release_date, '%d/%m/%y') > datetime.datetime.now())

        new_rating = body.get('rating', None)
        new_critic_rating = body.get('critic_rating', None)
        new_PEGI_rating = body.get('PEGI_rating', None)

        new_genres = body.get('genres', None)
        new_developer = body.get('developer', None)
        new_publisher = body.get('publisher', None)

        game = Game(name=new_name, description=new_description, release_date=new_release_date,
                    released=new_released, rating=new_rating, critic_rating=new_critic_rating,
                    PEGI_rating=new_PEGI_rating, genres=new_genres, developer=new_developer,
                    publisher=new_publisher)

        db.session.add(game)
        db.session.commit()
        return jsonify({
            'success': True,
        })
    except:
        db.session.rollback()
        return jsonify({
            'success': True,
        })
    finally:
        db.session.close()


@ app.route('/games/<int:game_id>', methods=['PATCH'])
def patch_game():

    return


@ app.route('/games/<int:game_id>', methods=['DELETE'])
def delete_game():

    return


#----------------------------------------------------------------------------#
# error handlers.
#----------------------------------------------------------------------------#


@ app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 404,
        'message': 'resource not found'
    }), 404


@ app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success': False,
        'error': 422,
        'message': 'unprocessable'
    }), 422


@ app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success': False,
        'error': 400,
        'message': 'bad_request'
    }), 400


@ app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        'success': False,
        'error': 405,
        'message': 'method not allowed'
    }), 405


#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')


if __name__ == '__main__':
    app.run()
