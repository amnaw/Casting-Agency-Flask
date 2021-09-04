import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
import requests

from app import create_app
from models import Actor, Movie, setup_db
from auth import *


class TestCase(unittest.TestCase):
    """This class represents the test case"""

    def setUp(self):
        """Define test variables and initialize app"""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "CastingAgencydb"

        self.database_path = os.environ['DATABASE_URL']
        if self.database_path.startswith ("postgres://"):
            self.database_path = self.database_path.replace("postgres://", "postgresql://", 1)

        # "postgres://{}/{}".format(
        #     'postgres:Aa123456@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            # self.db.create_all()
        
        # Define Test variables
        self.new_actor = {
            'first_name': 'Amna',
            'last_name': 'Saad', 
            'gender': 'F'
        }
        self.new_movie = {
            'title': 'Spirited Away',
            'release_date': 'Tue, 07 Jan 2001 00:00:00 GMT', 
            'rank': 5
        }
        self.edited_actor = {
            'first_name': 'Amna',
            'last_name': 'EDITED'
        }
        self.edited_movie = {
            'title': 'The Second EDITED movie'
        }
       
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # RBAC Tests
    # Tests for Executive Producer Role

    # Tests for /actors
    def test_get_actors(self):
        response = self.client().get("/actors", headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ2NTEwMWNlZmEwMDczNDZhMTg3IiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTEyNDMsImV4cCI6MTYzMDgzNzY0MywiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NQX4D_Vad82tNr3GnLc0-a7umPGi1U-6kzBq1c7XbehjZlRa5MfK76uovjc-AVngPrKHViSSXJgcqq3R6onKjwxgxIv32h5YzXV5EV0OO5th4AoRxdMVVZrrH3a0RIKg2_MTyIPmVM_7FhGU-HtAmSfztYMD2FRV6nTwN1RLfkqCFfpTu3HVGSS_VGseDLNaH88fxYiHLdMuUQ2krw-L-fEQjnUTix5OFPT_hyt50HJ2o7uhWJWhyo4WDCUS5E7dbw8hw1FTYGZ2Li8KTTL-fsiEPCPIDQNZqO_aRVYIK-BcxyfBMUKE9dstzNKgu3tn-aHkXk__-yB_RQlI8iHOnQ"
        })
        # gets the json of the response body
        data = json.loads(response.data)  

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        print(data['actors'])
    
    def test_405_delete_actors(self):
        response = self.client().delete('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not Allowed')

    # Tests for /movies
    def test_get_movies(self):
        response = self.client().get('/movies', headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ2NTEwMWNlZmEwMDczNDZhMTg3IiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTEyNDMsImV4cCI6MTYzMDgzNzY0MywiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NQX4D_Vad82tNr3GnLc0-a7umPGi1U-6kzBq1c7XbehjZlRa5MfK76uovjc-AVngPrKHViSSXJgcqq3R6onKjwxgxIv32h5YzXV5EV0OO5th4AoRxdMVVZrrH3a0RIKg2_MTyIPmVM_7FhGU-HtAmSfztYMD2FRV6nTwN1RLfkqCFfpTu3HVGSS_VGseDLNaH88fxYiHLdMuUQ2krw-L-fEQjnUTix5OFPT_hyt50HJ2o7uhWJWhyo4WDCUS5E7dbw8hw1FTYGZ2Li8KTTL-fsiEPCPIDQNZqO_aRVYIK-BcxyfBMUKE9dstzNKgu3tn-aHkXk__-yB_RQlI8iHOnQ"
        })
        # gets the json of the response body
        data = json.loads(response.data)  

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_405_patch_movies(self):
        response = self.client().patch('/movies')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not Allowed') 

    # Tests for DELETE /actors/<id>
    def test_delete_actor(self):
        response = self.client().delete('/actors/4', headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ2NTEwMWNlZmEwMDczNDZhMTg3IiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTEyNDMsImV4cCI6MTYzMDgzNzY0MywiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NQX4D_Vad82tNr3GnLc0-a7umPGi1U-6kzBq1c7XbehjZlRa5MfK76uovjc-AVngPrKHViSSXJgcqq3R6onKjwxgxIv32h5YzXV5EV0OO5th4AoRxdMVVZrrH3a0RIKg2_MTyIPmVM_7FhGU-HtAmSfztYMD2FRV6nTwN1RLfkqCFfpTu3HVGSS_VGseDLNaH88fxYiHLdMuUQ2krw-L-fEQjnUTix5OFPT_hyt50HJ2o7uhWJWhyo4WDCUS5E7dbw8hw1FTYGZ2Li8KTTL-fsiEPCPIDQNZqO_aRVYIK-BcxyfBMUKE9dstzNKgu3tn-aHkXk__-yB_RQlI8iHOnQ"
        })
        data = json.loads(response.data)

        actor = Actor.query.get(4)  # delete from db

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], '4')
        self.assertEqual(actor, None)
    
    def test_422_actor_not_exist(self):
        response = self.client().delete('/actors/999', headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ2NTEwMWNlZmEwMDczNDZhMTg3IiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTEyNDMsImV4cCI6MTYzMDgzNzY0MywiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NQX4D_Vad82tNr3GnLc0-a7umPGi1U-6kzBq1c7XbehjZlRa5MfK76uovjc-AVngPrKHViSSXJgcqq3R6onKjwxgxIv32h5YzXV5EV0OO5th4AoRxdMVVZrrH3a0RIKg2_MTyIPmVM_7FhGU-HtAmSfztYMD2FRV6nTwN1RLfkqCFfpTu3HVGSS_VGseDLNaH88fxYiHLdMuUQ2krw-L-fEQjnUTix5OFPT_hyt50HJ2o7uhWJWhyo4WDCUS5E7dbw8hw1FTYGZ2Li8KTTL-fsiEPCPIDQNZqO_aRVYIK-BcxyfBMUKE9dstzNKgu3tn-aHkXk__-yB_RQlI8iHOnQ"
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # Tests for DELETE /movies/<id>
    def test_delete_movie(self):
        response = self.client().delete('/movies/2', headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ2NTEwMWNlZmEwMDczNDZhMTg3IiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTEyNDMsImV4cCI6MTYzMDgzNzY0MywiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NQX4D_Vad82tNr3GnLc0-a7umPGi1U-6kzBq1c7XbehjZlRa5MfK76uovjc-AVngPrKHViSSXJgcqq3R6onKjwxgxIv32h5YzXV5EV0OO5th4AoRxdMVVZrrH3a0RIKg2_MTyIPmVM_7FhGU-HtAmSfztYMD2FRV6nTwN1RLfkqCFfpTu3HVGSS_VGseDLNaH88fxYiHLdMuUQ2krw-L-fEQjnUTix5OFPT_hyt50HJ2o7uhWJWhyo4WDCUS5E7dbw8hw1FTYGZ2Li8KTTL-fsiEPCPIDQNZqO_aRVYIK-BcxyfBMUKE9dstzNKgu3tn-aHkXk__-yB_RQlI8iHOnQ"
        })
        data = json.loads(response.data)

        movie = Movie.query.get(2)  # delete from db

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], '2')
        self.assertEqual(movie, None)

    def test_422_movie_not_exist(self):
        response = self.client().delete('/movies/999', headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ2NTEwMWNlZmEwMDczNDZhMTg3IiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTEyNDMsImV4cCI6MTYzMDgzNzY0MywiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NQX4D_Vad82tNr3GnLc0-a7umPGi1U-6kzBq1c7XbehjZlRa5MfK76uovjc-AVngPrKHViSSXJgcqq3R6onKjwxgxIv32h5YzXV5EV0OO5th4AoRxdMVVZrrH3a0RIKg2_MTyIPmVM_7FhGU-HtAmSfztYMD2FRV6nTwN1RLfkqCFfpTu3HVGSS_VGseDLNaH88fxYiHLdMuUQ2krw-L-fEQjnUTix5OFPT_hyt50HJ2o7uhWJWhyo4WDCUS5E7dbw8hw1FTYGZ2Li8KTTL-fsiEPCPIDQNZqO_aRVYIK-BcxyfBMUKE9dstzNKgu3tn-aHkXk__-yB_RQlI8iHOnQ"
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # Tests for POST /actors
    def test_add_actor(self):
        response = self.client().post('/actors', json=self.new_actor, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ2NTEwMWNlZmEwMDczNDZhMTg3IiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTEyNDMsImV4cCI6MTYzMDgzNzY0MywiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NQX4D_Vad82tNr3GnLc0-a7umPGi1U-6kzBq1c7XbehjZlRa5MfK76uovjc-AVngPrKHViSSXJgcqq3R6onKjwxgxIv32h5YzXV5EV0OO5th4AoRxdMVVZrrH3a0RIKg2_MTyIPmVM_7FhGU-HtAmSfztYMD2FRV6nTwN1RLfkqCFfpTu3HVGSS_VGseDLNaH88fxYiHLdMuUQ2krw-L-fEQjnUTix5OFPT_hyt50HJ2o7uhWJWhyo4WDCUS5E7dbw8hw1FTYGZ2Li8KTTL-fsiEPCPIDQNZqO_aRVYIK-BcxyfBMUKE9dstzNKgu3tn-aHkXk__-yB_RQlI8iHOnQ"
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_id'])
        self.assertTrue(data['total_actors'])
    

    def test_422_add_actor(self):
        response = self.client().post('/actors', json={ }, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ2NTEwMWNlZmEwMDczNDZhMTg3IiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTEyNDMsImV4cCI6MTYzMDgzNzY0MywiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NQX4D_Vad82tNr3GnLc0-a7umPGi1U-6kzBq1c7XbehjZlRa5MfK76uovjc-AVngPrKHViSSXJgcqq3R6onKjwxgxIv32h5YzXV5EV0OO5th4AoRxdMVVZrrH3a0RIKg2_MTyIPmVM_7FhGU-HtAmSfztYMD2FRV6nTwN1RLfkqCFfpTu3HVGSS_VGseDLNaH88fxYiHLdMuUQ2krw-L-fEQjnUTix5OFPT_hyt50HJ2o7uhWJWhyo4WDCUS5E7dbw8hw1FTYGZ2Li8KTTL-fsiEPCPIDQNZqO_aRVYIK-BcxyfBMUKE9dstzNKgu3tn-aHkXk__-yB_RQlI8iHOnQ"
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable') 
    
    # Tests for POST /movies
    def test_add_movie(self):
        response = self.client().post('/movies', json=self.new_movie, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ2NTEwMWNlZmEwMDczNDZhMTg3IiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTEyNDMsImV4cCI6MTYzMDgzNzY0MywiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NQX4D_Vad82tNr3GnLc0-a7umPGi1U-6kzBq1c7XbehjZlRa5MfK76uovjc-AVngPrKHViSSXJgcqq3R6onKjwxgxIv32h5YzXV5EV0OO5th4AoRxdMVVZrrH3a0RIKg2_MTyIPmVM_7FhGU-HtAmSfztYMD2FRV6nTwN1RLfkqCFfpTu3HVGSS_VGseDLNaH88fxYiHLdMuUQ2krw-L-fEQjnUTix5OFPT_hyt50HJ2o7uhWJWhyo4WDCUS5E7dbw8hw1FTYGZ2Li8KTTL-fsiEPCPIDQNZqO_aRVYIK-BcxyfBMUKE9dstzNKgu3tn-aHkXk__-yB_RQlI8iHOnQ"
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_id'])
        self.assertTrue(data['total_movies'])
    

    def test_422_add_movie(self):
        response = self.client().post('/movies', json=self.new_actor, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ2NTEwMWNlZmEwMDczNDZhMTg3IiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTEyNDMsImV4cCI6MTYzMDgzNzY0MywiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NQX4D_Vad82tNr3GnLc0-a7umPGi1U-6kzBq1c7XbehjZlRa5MfK76uovjc-AVngPrKHViSSXJgcqq3R6onKjwxgxIv32h5YzXV5EV0OO5th4AoRxdMVVZrrH3a0RIKg2_MTyIPmVM_7FhGU-HtAmSfztYMD2FRV6nTwN1RLfkqCFfpTu3HVGSS_VGseDLNaH88fxYiHLdMuUQ2krw-L-fEQjnUTix5OFPT_hyt50HJ2o7uhWJWhyo4WDCUS5E7dbw8hw1FTYGZ2Li8KTTL-fsiEPCPIDQNZqO_aRVYIK-BcxyfBMUKE9dstzNKgu3tn-aHkXk__-yB_RQlI8iHOnQ"
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable') 
    
    # Tests for PATCH /actors/<id>/edit
    def test_edit_actor(self):
        response = self.client().patch('/actors/7/edit', json=self.edited_actor, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ2NTEwMWNlZmEwMDczNDZhMTg3IiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTEyNDMsImV4cCI6MTYzMDgzNzY0MywiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NQX4D_Vad82tNr3GnLc0-a7umPGi1U-6kzBq1c7XbehjZlRa5MfK76uovjc-AVngPrKHViSSXJgcqq3R6onKjwxgxIv32h5YzXV5EV0OO5th4AoRxdMVVZrrH3a0RIKg2_MTyIPmVM_7FhGU-HtAmSfztYMD2FRV6nTwN1RLfkqCFfpTu3HVGSS_VGseDLNaH88fxYiHLdMuUQ2krw-L-fEQjnUTix5OFPT_hyt50HJ2o7uhWJWhyo4WDCUS5E7dbw8hw1FTYGZ2Li8KTTL-fsiEPCPIDQNZqO_aRVYIK-BcxyfBMUKE9dstzNKgu3tn-aHkXk__-yB_RQlI8iHOnQ"
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_id'])
        self.assertTrue(data['total_actors'])
    

    def test_401_add_actor(self):
        response = self.client().patch('/actors/7/edit')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'AuthError') 
    

    def test_422_actor_not_exist2(self):
        response = self.client().patch('/actors/999/edit', json=self.edited_actor, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ2NTEwMWNlZmEwMDczNDZhMTg3IiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTEyNDMsImV4cCI6MTYzMDgzNzY0MywiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NQX4D_Vad82tNr3GnLc0-a7umPGi1U-6kzBq1c7XbehjZlRa5MfK76uovjc-AVngPrKHViSSXJgcqq3R6onKjwxgxIv32h5YzXV5EV0OO5th4AoRxdMVVZrrH3a0RIKg2_MTyIPmVM_7FhGU-HtAmSfztYMD2FRV6nTwN1RLfkqCFfpTu3HVGSS_VGseDLNaH88fxYiHLdMuUQ2krw-L-fEQjnUTix5OFPT_hyt50HJ2o7uhWJWhyo4WDCUS5E7dbw8hw1FTYGZ2Li8KTTL-fsiEPCPIDQNZqO_aRVYIK-BcxyfBMUKE9dstzNKgu3tn-aHkXk__-yB_RQlI8iHOnQ"
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # Tests for PATCH /movies/<id>/edit
    def test_edit_movie(self):
        response = self.client().patch('/movies/7/edit', json=self.edited_movie, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ2NTEwMWNlZmEwMDczNDZhMTg3IiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTEyNDMsImV4cCI6MTYzMDgzNzY0MywiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NQX4D_Vad82tNr3GnLc0-a7umPGi1U-6kzBq1c7XbehjZlRa5MfK76uovjc-AVngPrKHViSSXJgcqq3R6onKjwxgxIv32h5YzXV5EV0OO5th4AoRxdMVVZrrH3a0RIKg2_MTyIPmVM_7FhGU-HtAmSfztYMD2FRV6nTwN1RLfkqCFfpTu3HVGSS_VGseDLNaH88fxYiHLdMuUQ2krw-L-fEQjnUTix5OFPT_hyt50HJ2o7uhWJWhyo4WDCUS5E7dbw8hw1FTYGZ2Li8KTTL-fsiEPCPIDQNZqO_aRVYIK-BcxyfBMUKE9dstzNKgu3tn-aHkXk__-yB_RQlI8iHOnQ"
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_id'])
        self.assertTrue(data['total_movies'])
    

    def test_401_add_movie(self):
        response = self.client().patch('/movies/7/edit')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'AuthError') 
    

    def test_422_movie_not_exist2(self):
        response = self.client().patch('/movies/999/edit', json=self.edited_movie, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ2NTEwMWNlZmEwMDczNDZhMTg3IiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTEyNDMsImV4cCI6MTYzMDgzNzY0MywiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NQX4D_Vad82tNr3GnLc0-a7umPGi1U-6kzBq1c7XbehjZlRa5MfK76uovjc-AVngPrKHViSSXJgcqq3R6onKjwxgxIv32h5YzXV5EV0OO5th4AoRxdMVVZrrH3a0RIKg2_MTyIPmVM_7FhGU-HtAmSfztYMD2FRV6nTwN1RLfkqCFfpTu3HVGSS_VGseDLNaH88fxYiHLdMuUQ2krw-L-fEQjnUTix5OFPT_hyt50HJ2o7uhWJWhyo4WDCUS5E7dbw8hw1FTYGZ2Li8KTTL-fsiEPCPIDQNZqO_aRVYIK-BcxyfBMUKE9dstzNKgu3tn-aHkXk__-yB_RQlI8iHOnQ"
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

   
    # RBAC Tests
    # Tests for Casting Assistant Role 
    def test_assistant_get_actors(self):
        response = self.client().get("/actors", headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ3NDI3YjhlM2EwMDY5ZmU2MDUzIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTE0ODksImV4cCI6MTYzMDgzNzg4OSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.RUPR_ZJbFy223gnmygvohKlNZx1owZd8gV0vP0Kp9bHYocpTjs9WUuaWOk1mtnOCA14G-N8knVWNvTwfEQDKJy-hC7dxeuqZ6QQQxj5sFJkLdHbtrAKau2EpG24AFEAfzVEhNd_gjChZmd9TDYI4vpRKEesldP4ApWzFjFmP-FBEGtf1sSehqbJy2jFbyeKnlfZ10JNQa0RqGgUuUpJBnOa32N2czCxOonvPo8Hw_yV-Mwg6XtWRDcHwtJXzfd8X4EYuNxQ84zrbpKn5ZltMJfRNo3Dk5j5-9I_pC7_5nyhcRk8o80-KA21XiQFZz7775dqyRwZXdxsLFEPDasTjfQ"
            })
        data = json.loads(response.data)  

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_403_add_actor(self):
        response = self.client().post('/actors', json=self.new_actor, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ3NDI3YjhlM2EwMDY5ZmU2MDUzIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTA1MzAsImV4cCI6MTYzMDgzNjkzMCwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.tiqjkW1V1Z7PjuCjdBCtbTdOY0mw6PsCkg1N67oVRGeFHfWwHTpHqujdDUWiT5CCfGRIWWkxjaUyLpQGLqjm7D-dTzLmEqKMZrwnPgv2tbSrPD_nCKySwfTiSLHvOdnLUhKtHMbOXfxc4eI1AZIRaH9jEpWwvUk0vrAvkmZNLzZxBliF_q1qdo289nIcyhSWgl9UbQPH1XP_6kJ4RtzEygY56r2tcLqVuK8vAAdaP1yuzF666WHPsGAijdWN9DSAqAoMECNZMwvqcQaD0J-GxFi0nYhBFOQZs9sJJDer_YwGIRAL-Ps8HGukJhwp4MwetDgR8bANZ1ULjsPnRb83vA"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Forbidden')
    
    # RBAC Tests
    # Tests for Casting Director Role 
    def test_director_add_actor(self):
        response = self.client().post('/actors', json=self.new_actor, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ2YmE0ZjI4YWMwMDZiZDcwMGFhIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTExMDYsImV4cCI6MTYzMDgzNzUwNiwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.kJ01JoPOs3y-9GRTenLAmpQZgNP3v847Q1NuCkWSOsm3MWQ0DRRuEsYvViq91S7Y1jpDTPw09WWMeu1w3ww6RUkghheHN9C4pVDnaC66A7RltSDTnnx_N0aI6wKTk4iYdC-CK5HWB9GZAvsjzD0H8enA41NPcOnrRMiUcSblRxZyAc-t78w57evBXtwzYpgv1fiQrl7C7MZxmbdpcWmVxTxGCs7QPkwdbJChA56vU9RPpHJwUCAaIhznJ9GvJ4szStS6ReYutJjZ1RXSkV_vSAK8qITCUa3dZIRCmQzgUM4m_w3PF5qQonaopMZhfJgXTiZjUUn2X35sPPHaTL4rrQ"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_id'])
        self.assertTrue(data['total_actors'])

    def test_403_add_movie(self):
        response = self.client().post('/movies', json=self.new_movie, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMzQ2YmE0ZjI4YWMwMDZiZDcwMGFhIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA3NTAzOTQsImV4cCI6MTYzMDgzNjc5NCwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbXX0.QddNy4YgNznTcNdPjAfRZvo8mAg85vxFfVrTiQbnx_DXFaLOOce7lh8WZWGPh2isYR5eAnxQ-jI-jePi0Zc4iaznQFkkbbQm33TKInK9hXGTJkPBPLMl1cx700zj4vfvSbW7hQk5O3tqNKjGXypPFgf_ogyHOEMbAJ6cFg_HMC8JQE_f2301VqrUntW1usDoGjv_I9TL0XhvBV56RZ-br3Z6Dicx8Dzbc8ifFzpff4dDqOhl6XEqzUaPU_FOZA28ku_XLgV43vXhMKBi3GFgZI0VwJFVEpxa3RdJs5kqU_sHFJMW1vIQSSdQ9xLLaqgjjlU-c88nTfr5ZaIot31ezg"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Forbidden')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
