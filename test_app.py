import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


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
        self.producer_hearders = {
            "Content-Type": "application/json",
            "Authorization": os.getenv('EXECUTIVE_DIRECTOR')
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

    def test_get_paginated_actors_casting_asst(self):
        res = self.client().get('/actors', headers=self.assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['total_actors'])
        self.assertTrue(data['actors_displayed'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
