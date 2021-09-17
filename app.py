#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import datetime
from operator import ne
import os
import dateutil.parser
import babel
from flask import (Flask, request, jsonify,
                   Response, flash, redirect, url_for)
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from typing import final
import logging
import random
from flask_migrate import Migrate
from logging import Formatter, FileHandler, log
from models import *
from auth import requires_auth, AuthError


#----------------------------------------------------------------------------#
# App.
#----------------------------------------------------------------------------#


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @ app.route('/')
    def index():
        return jsonify({
            'message': 'hi, this is game api tristan. In order to understand how to interact with the api, please read the documentation here https://github.com/fiend361/Video-Games-API-Tristan',
        })

    @ app.route('/games', methods=['GET'])
    # @requires_auth('get:games')
    def get_games():
        try:
            games = Game.query.all()
        except:
            abort(422)

        data = [{
            "id": game.id,
            "name": game.name,
            "description": game.description,
            "release_date": game.release_date,
            "released": game.released,
            "rating": game.rating,
            "critic_rating": game.critic_rating,
            "PEGI_rating":  game.PEGI_rating,
            "genres": game.genres,
            "developer": game.developer_id,
            "publisher": game.publisher_id
        } for game in games]

        return jsonify({
            'success': True,
            'games': data,
        })

    @ app.route('/games/<int:game_id>', methods=['GET'])
    # @requires_auth('get:games')
    def get_game_by_id(game_id):
        game = Game.query.filter(
            Game.id == game_id).one_or_none()
        if game is None:
            abort(404)

        data = {
            "id": game.id,
            "name": game.name,
            "description": game.description,
            "release_date": game.release_date,
            "released": game.released,
            "rating": game.rating,
            "critic_rating": game.critic_rating,
            "PEGI_rating":  game.PEGI_rating,
            "genres": game.genres,
            "developer": game.developer_id,
            "publisher": game.publisher_id
        }
        return jsonify({
            'success': True,
            'game': data,
        })

    @ app.route('/games', methods=['POST'])
    # @requires_auth('post:games')
    def post_game():
        body = request.get_json()
        try:
            new_release_date = body.get('release_date', None)
            new_released = (datetime.datetime.strptime(
                new_release_date, '%d/%m/%y') > datetime.datetime.now())
        except:
            return jsonify({
                'success': False,
                'message': 'please enter date in the correct format d/m/y as in: 30/5/21'
            })

        try:
            new_name = body.get('name', None)
            new_description = body.get('description', None)

            new_rating = body.get('rating', None)
            new_critic_rating = body.get('critic_rating', None)
            new_PEGI_rating = body.get('PEGI_rating', None)

            new_genres = body.get('genres', None)
            new_developer = body.get('developer', None)
            new_publisher = body.get('publisher', None)

            developer = Developer.query.filter(
                Developer.id == new_developer).one_or_none()
            if developer is None:
                return jsonify({
                    'success': False,
                    'message': 'could not find developer with id {}'.format(new_developer)
                })

            publisher = Publisher.query.filter(
                Publisher.id == new_publisher).one_or_none()
            if publisher is None:
                return jsonify({
                    'success': False,
                    'message': 'could not find publisher with id {}'.format(new_publisher)
                })

            game = Game(name=new_name, description=new_description, release_date=new_release_date,
                        released=new_released, rating=new_rating, critic_rating=new_critic_rating,
                        PEGI_rating=new_PEGI_rating, genres=new_genres, developer_id=new_developer,
                        publisher_id=new_publisher)

            game.insert()
            return jsonify({
                'success': True,
            })
        except:
            return jsonify({
                'success': False,
            })

    @ app.route('/games/<int:game_id>', methods=['PATCH'])
    # @requires_auth('patch:games')
    def patch_game(game_id):
        game = Game.query.filter(
            Game.id == game_id).one_or_none()
        if game is None:
            abort(404)

        body = request.get_json()
        try:
            new_name = body.get('name', None)
            new_description = body.get('description', None)

            new_release_date = body.get('release_date', None)
            new_released = (datetime.datetime.strptime(
                new_release_date, '%d/%m/%y') > datetime.datetime.now())

            new_rating = body.get('rating', None)
            new_critic_rating = body.get('critic_rating', None)
            new_PEGI_rating = body.get('PEGI_rating', None)

            new_genres = body.get('genres', None)
            new_developer = body.get('developer', None)
            new_publisher = body.get('publisher', None)

            if new_name is not None:
                game.name = new_name
            if new_description is not None:
                game.description = new_description
            if new_release_date is not None:
                game.release_date = new_release_date
            if new_released is not None:
                game.released = new_released
            if new_rating is not None:
                game.rating = new_rating
            if new_critic_rating is not None:
                game.critic_rating = new_critic_rating
            if new_PEGI_rating is not None:
                game.PEGI_rating = new_PEGI_rating
            if new_genres is not None:
                game.genres = new_genres
            if new_developer is not None:
                developer = Developer.query.filter(
                    Developer.id == new_developer).one_or_none()
                if developer is None:
                    return jsonify({
                        'success': False,
                        'message': 'could not find developer with id {}'.format(new_developer)
                    })
                game.developer_id = new_developer
            if new_publisher is not None:
                publisher = Publisher.query.filter(
                    Publisher.id == new_publisher).one_or_none()
                if publisher is None:
                    return jsonify({
                        'success': False,
                        'message': 'could not find publisher with id {}'.format(new_publisher)
                    })
                game.publisher_id = new_publisher

            game.update()

            return jsonify({
                'success': True,
            })
        except:
            return jsonify({
                'success': False,
            })

    @ app.route('/games/<int:game_id>', methods=['DELETE'])
    # @requires_auth('delete:games')
    def delete_game(game_id):
        try:
            game = Game.query.filter(
                Game.id == game_id).one_or_none()
            if game is None:
                abort(404)

            game.delete()

            return jsonify({
                'success': True,
            })
        except:
            return jsonify({
                'success': False,
            })

    @ app.route('/developers', methods=['GET'])
    def get_developers():
        try:
            developers = Developer.query.all()
        except:
            abort(422)

        data = [{
            "id": developer.id,
            "name": developer.name,
            "description": developer.description
        } for developer in developers]

        return jsonify({
            'success': True,
            'developers': data,
        })

    @ app.route('/developers/<int:developer_id>', methods=['GET'])
    def get_developer_by_id(developer_id):
        developer = Developer.query.filter(
            Developer.id == developer_id).one_or_none()
        if developer is None:
            abort(404)

        data = {
            "id": developer.id,
            "name": developer.name,
            "description": developer.description
        }
        return jsonify({
            'success': True,
            'developer': data,
        })

    @ app.route('/developers', methods=['POST'])
    def post_developer():
        body = request.get_json()
        try:
            new_name = body.get('name', None)
            new_description = body.get('description', None)

            developer = Developer(name=new_name, description=new_description)

            developer.insert()
            return jsonify({
                'success': True,
            })
        except:
            return jsonify({
                'success': False,
            })

    @ app.route('/publishers', methods=['GET'])
    def get_publishers():
        try:
            publishers = Publisher.query.all()
        except:
            abort(422)

        data = [{
            "id": publisher.id,
            "name": publisher.name,
            "description": publisher.description
        } for publisher in publishers]

        return jsonify({
            'success': True,
            'publishers': data,
        })

    @ app.route('/publishers/<int:publisher_id>', methods=['GET'])
    def get_publisher_by_id(publisher_id):
        publisher = Publisher.query.filter(
            Publisher.id == publisher_id).one_or_none()
        if publisher is None:
            abort(404)

        data = {
            "id": publisher.id,
            "name": publisher.name,
            "description": publisher.description
        }
        return jsonify({
            'success': True,
            'publisher': data,
        })

    @ app.route('/publishers', methods=['POST'])
    def post_publisher():
        body = request.get_json()
        try:
            new_name = body.get('name', None)
            new_description = body.get('description', None)

            publisher = Publisher(name=new_name, description=new_description)

            publisher.insert()
            return jsonify({
                'success': True,
            })
        except:
            return jsonify({
                'success': False,
            })

    # //////////////////////////////////////////////////////////////////
    # error handlers
    # //////////////////////////////////////////////////////////////////

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

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
