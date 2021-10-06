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

    def make_invalid_date_format_error_message():
        return jsonify({
            'success': False,
            'message': 'please enter date in the correct format d/m/y as in: 30/5/21'
        })

    def make_unexpected_error_message():
        return jsonify({
            'success': False,
            'message': 'an unexpected error occured while processing your request. Please try again shortly.'
        })

    def make_developer_not_found_error_message(new_developer):
        return jsonify({
            'success': False,
            'message': 'could not find developer with id {}'.format(new_developer)
        })

    def make_publisher_not_found_error_message(new_publisher):
        return jsonify({
            'success': False,
            'message': 'could not find publisher with id {}'.format(new_publisher)
        })

    # //////////////////////////////////////////////////////////////////
    # endpoints
    # //////////////////////////////////////////////////////////////////

    # home endpoint
    @ app.route('/')
    def index():
        return jsonify({
            'message': 'hi, this is game api tristan. In order to understand how to interact with the api, \
please read the documentation here https://github.com/fiend361/Video-Games-API-Tristan or just \
try hitting https://tristan-game-api.herokuapp.com/games',
        })

    # games endpoints
    @ app.route('/games', methods=['GET'])
    def get_games():
        try:
            games = Game.query.all()
        except:
            abort(422)

        data = [game.format() for game in games]

        return jsonify({
            'success': True,
            'games': data,
        })

    @ app.route('/games/<int:game_id>', methods=['GET'])
    def get_game_by_id(game_id):
        game = Game.query.filter(
            Game.id == game_id).one_or_none()
        if game is None:
            abort(404)

        return jsonify({
            'success': True,
            'game': game.format(),
        })

    @ app.route('/games', methods=['POST'])
    def post_game():
        body = request.get_json()
        new_release_date = body.get('release_date', None)
        new_released = False
        try:
            new_released = (datetime.datetime.strptime(
                new_release_date, '%d/%m/%y') < datetime.datetime.now())
        except:
            return make_invalid_date_format_error_message()

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
                return make_developer_not_found_error_message(new_developer)

            publisher = Publisher.query.filter(
                Publisher.id == new_publisher).one_or_none()
            if publisher is None:
                return make_publisher_not_found_error_message(new_publisher)

            game = Game(name=new_name, description=new_description, release_date=new_release_date,
                        released=new_released, rating=new_rating, critic_rating=new_critic_rating,
                        PEGI_rating=new_PEGI_rating, genres=new_genres, developer_id=new_developer,
                        publisher_id=new_publisher)

            game.insert()
            return jsonify({
                'success': True,
                'game': game.format()
            })
        except:
            return make_unexpected_error_message()

    @ app.route('/games/<int:game_id>', methods=['PATCH'])
    def patch_game(game_id):
        game = Game.query.filter(
            Game.id == game_id).one_or_none()
        if game is None:
            abort(404)

        body = request.get_json()

        new_release_date = body.get('release_date', None)
        new_released = False
        if new_release_date is not None:
            try:
                new_released = (datetime.datetime.strptime(
                    new_release_date, '%d/%m/%y') < datetime.datetime.now())
            except:
                return make_invalid_date_format_error_message()

        new_developer = body.get('developer', None)
        if new_developer is not None:
            developer = Developer.query.filter(
                Developer.id == new_developer).one_or_none()
            if developer is None:
                return make_developer_not_found_error_message(new_developer)

        new_publisher = body.get('publisher', None)
        if new_publisher is not None:
            publisher = Publisher.query.filter(
                Publisher.id == new_publisher).one_or_none()
            if publisher is None:
                return make_publisher_not_found_error_message(new_publisher)

        try:
            new_name = body.get('name', None)
            new_description = body.get('description', None)

            new_rating = body.get('rating', None)
            new_critic_rating = body.get('critic_rating', None)
            new_PEGI_rating = body.get('PEGI_rating', None)

            new_genres = body.get('genres', None)

            if new_name is not None:
                game.name = new_name
            if new_description is not None:
                game.description = new_description
            if new_release_date is not None:
                game.release_date = new_release_date
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
                game.developer_id = new_developer
            if new_publisher is not None:
                game.publisher_id = new_publisher

            game.update()

            return jsonify({
                'success': True,
                'game': game.format()
            })
        except:
            return make_unexpected_error_message()

    @ app.route('/games/<int:game_id>', methods=['DELETE'])
    def delete_game(game_id):
        try:
            game = Game.query.filter(
                Game.id == game_id).one_or_none()
            if game is None:
                abort(404)

            game.delete()

            return jsonify({
                'success': True,
                'message': 'successfully deleted game with id {}'.format(game_id)
            })
        except:
            return make_unexpected_error_message()

    # developers endpoints
    @ app.route('/developers', methods=['GET'])
    def get_developers():
        try:
            developers = Developer.query.all()
        except:
            abort(422)

        data = [developer.format() for developer in developers]

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

        return jsonify({
            'success': True,
            'developer': developer.format(),
        })

    @ app.route('/developers', methods=['POST'])
    def post_developer():
        body = request.get_json()
        try:
            new_name = body.get('name', None)
            new_description = body.get('description', None)

            new_rating = body.get('rating', None)
            new_establish_year = body.get('establish_year', None)

            new_active = body.get('active', None)

            developer = Developer(name=new_name, description=new_description, rating=new_rating,
                                  establish_year=new_establish_year, active=new_active)

            developer.insert()
            return jsonify({
                'success': True,
                'developer': developer.format(),
            })
        except:
            return make_unexpected_error_message()

    # publishers endpoints
    @ app.route('/publishers', methods=['GET'])
    def get_publishers():
        try:
            publishers = Publisher.query.all()
        except:
            abort(422)

        data = [publisher.format() for publisher in publishers]

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

        return jsonify({
            'success': True,
            'publisher': publisher.format(),
        })

    @ app.route('/publishers', methods=['POST'])
    def post_publisher():
        body = request.get_json()
        try:
            new_name = body.get('name', None)
            new_description = body.get('description', None)

            new_rating = body.get('rating', None)
            new_establish_year = body.get('establish_year', None)

            new_active = body.get('active', None)

            publisher = Publisher(name=new_name, description=new_description, rating=new_rating,
                                  establish_year=new_establish_year, active=new_active)

            publisher.insert()

            return jsonify({
                'success': True,
                'developer': publisher.format(),
            })
        except:
            return make_unexpected_error_message()

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
