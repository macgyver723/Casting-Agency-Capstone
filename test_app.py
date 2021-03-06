import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor


class CastingAgencyTestCase(unittest.TestCase):
    '''This class represents the Casting Agencey test case'''

    def setUp(self):
        '''Define variables and initalize the app.'''
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'casting_agency_test'
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'postgres', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # jwts
        self.assistant_headers = {
            "Content-Type": "application/json",
            "Authorization": os.getenv('CASTING_ASSISTANT')
        }
        self.director_headers = {
            "Content-Type": "application/json",
            "Authorization": os.getenv('CASTING_DIRECTOR')
        }
        self.producer_headers = {
            "Content-Type": "application/json",
            "Authorization": os.getenv('EXECUTIVE_PRODUCER')
        }

        # data objects to use for tests
        self.new_actor = {
            "name": "Tom Shanks",
            "birthdate": "1955-01-01 00:00:00",
            "gender": "M",
            "seekingWork": True
        }

        self.new_movie = {
            "title": "Star Wars X: We messed up",
            "releaseDate": "2023-07-23 00:00:00",
            "genre": "Fantasy"
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        '''Executed after each test'''
        pass

    def test_get_actors_casting_asst(self):
        res = self.client().get('/actors', headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])

    def test_get_actors_no_permissions(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_get_actor_by_id(self):
        res = self.client().get('/actors/38', headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_get_actor_by_id_without_permissions(self):
        res = self.client().get('/actors/38')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_add_actor_casting_director(self):
        res = self.client().post('/actors',
                                 headers=self.director_headers,
                                 json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertTrue(data['total_actors'])

    def test_add_actor_unauthorized_assistant(self):
        res = self.client().post('/actors', headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')

    def test_modify_actor_executive_producer(self):
        res = self.client().patch('/actors/33',
                                  headers=self.producer_headers,
                                  json={"name": "Tom Hinks"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_actor']['name'], "Tom Hinks")

    def test_modify_actor_unauthorized_assistant(self):
        res = self.client().patch('/actors/34',
                                  headers=self.assistant_headers,
                                  json={"name": "Christian Ball"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')

    def test_delete_actor_casting_director(self):
        res = self.client().delete('/actors/35',
                                   headers=self.director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_name'], "Hue Jillman")
        actor = Actor.query.filter(Actor.id == 35).one_or_none()
        self.assertFalse(actor)

    def test_delete_actor_unauthorized_casing_assistant(self):
        res = self.client().delete('/actors/33',
                                   headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')

    def test_get_movies_executive_producer(self):
        res = self.client().get('/movies',
                                headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['total_movies'])

    def test_get_movies_no_permissions(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_get_movie_by_id(self):
        res = self.client().get('/movies/7', headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_get_movie_by_id_no_permissions(self):
        res = self.client().get('/movies/7')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'])

    def test_add_movie_executive_producer(self):
        res = self.client().post('/movies',
                                 headers=self.producer_headers,
                                 json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['id'])
        self.assertTrue(data['total_movies'])

    def test_add_movie_unauthorized_casting_director(self):
        res = self.client().post('/movies',
                                 headers=self.director_headers,
                                 json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')

    def test_modify_movie_casting_director(self):
        res = self.client().patch('/movies/8',
                                  headers=self.director_headers,
                                  json={"genre": "Action"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['updated_movie']['genre'], "Action")

    def test_modify_movie_unauthorized_casting_assistant(self):
        res = self.client().patch('/movies/7',
                                  headers=self.assistant_headers,
                                  json={"genre": "Horror"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')

    def test_delete_movie_executive_producer(self):
        res = self.client().delete('/movies/9',
                                   headers=self.producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted_title'], "Saw 31")

    def test_delete_movie_unauthorized_casting_director(self):
        res = self.client().delete('/movies/8',
                                   headers=self.director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message']['code'], 'unauthorized')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
