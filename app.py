#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
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
db.init_app(app)

migrate = Migrate(app, db)

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#


def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(value)
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format)


app.jinja_env.filters['datetime'] = format_datetime

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

    return


@ app.route('/games/<int:game_id>', methods=['GET'])
def get_game_by_id():

    return


@ app.route('/games', methods=['POST'])
def post_game():

    return


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
