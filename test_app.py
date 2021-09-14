import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

db_user = os.environ['DB_USER']
db_pass = os.environ['DB_PASS']


class TriviaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgresql://{}:{}@://{}/{}".format(db_user, db_pass,
                                                                  'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
        #     # create all tables
            self.db.create_all()

    def tearDown(self):
        pass

    def test_post_game(self):
        res = self.client().post(
            '/games', json={'name': 'new game', 'description': 'new game description',
                            'release_date': '19/5/21', 'rating': 90, 'critic_rating': 93,
                            'PEGI_rating': 16, 'genres': 'action', 'developer': '11bit', 'publisher': '11bit'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_400_sent_invalid_release_date(self):
        res = self.client().post(
            '/games', json={'name': 'new game', 'description': 'new game description',
                            'release_date': '19/19/2021', 'rating': 90, 'critic_rating': 93,
                            'PEGI_rating': 16, 'genres': 'action', 'developer': '11bit', 'publisher': '11bit'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_get_games(self):
        res = self.client().get('/games')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['games'])

    def test_get_game_by_id(self):
        res = self.client().get('/games/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['game'])

    def test_404_sent_nonexistent_game_id(self):
        res = self.client().get('/games/12345679')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_patch_game(self):
        res = self.client().patch(
            '/games/1', json={'name': 'new game', 'description': 'new game description'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_patch_game(self):
        res = self.client().delete('/games/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
