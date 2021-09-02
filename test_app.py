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

        self.database_path = "postgres://{}/{}".format(
            'postgres:Aa123456@localhost:5432', self.database_name)
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
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMDdlNzg3YjhlM2EwMDY5ZmRhZDIzIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1NjgyODksImV4cCI6MTYzMDY1NDY4OSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NF4gX6e-lQcno4wN9cwqd4GZ4bm1sX9rlWnNnxuivV9zuKTKfa4Gu3Vo_NqxCiIRHA52QXx1UpEAurBQYjkCeqwObyd3_l0b_DO2KqK0PbAGOAYVNTxnIpxiwdYOh3ZSNiT-F0bOyLrHEwe3QKcb-SJY5w4CvhQim9kbPcmCECCcxFpJk2WmsZEzOD8C5JzlclgUFyFu01LbUrBMyyWgS_56hZu6B5myji3dGlTjwwKV7fplCgZ9eyLa1FqXJzR7-o-DxmK-OVf-bQuRFiKfccdC1ssEa-InBNIVjAvXd5VK9WpwkOPmaqFG_7fF0BlXaM9sXNTKlNQyJvjdSS8hJw"
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
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMDdlNzg3YjhlM2EwMDY5ZmRhZDIzIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1NjgyODksImV4cCI6MTYzMDY1NDY4OSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NF4gX6e-lQcno4wN9cwqd4GZ4bm1sX9rlWnNnxuivV9zuKTKfa4Gu3Vo_NqxCiIRHA52QXx1UpEAurBQYjkCeqwObyd3_l0b_DO2KqK0PbAGOAYVNTxnIpxiwdYOh3ZSNiT-F0bOyLrHEwe3QKcb-SJY5w4CvhQim9kbPcmCECCcxFpJk2WmsZEzOD8C5JzlclgUFyFu01LbUrBMyyWgS_56hZu6B5myji3dGlTjwwKV7fplCgZ9eyLa1FqXJzR7-o-DxmK-OVf-bQuRFiKfccdC1ssEa-InBNIVjAvXd5VK9WpwkOPmaqFG_7fF0BlXaM9sXNTKlNQyJvjdSS8hJw"
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
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMDdlNzg3YjhlM2EwMDY5ZmRhZDIzIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1NjgyODksImV4cCI6MTYzMDY1NDY4OSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NF4gX6e-lQcno4wN9cwqd4GZ4bm1sX9rlWnNnxuivV9zuKTKfa4Gu3Vo_NqxCiIRHA52QXx1UpEAurBQYjkCeqwObyd3_l0b_DO2KqK0PbAGOAYVNTxnIpxiwdYOh3ZSNiT-F0bOyLrHEwe3QKcb-SJY5w4CvhQim9kbPcmCECCcxFpJk2WmsZEzOD8C5JzlclgUFyFu01LbUrBMyyWgS_56hZu6B5myji3dGlTjwwKV7fplCgZ9eyLa1FqXJzR7-o-DxmK-OVf-bQuRFiKfccdC1ssEa-InBNIVjAvXd5VK9WpwkOPmaqFG_7fF0BlXaM9sXNTKlNQyJvjdSS8hJw"
            })
        data = json.loads(response.data)

        actor = Actor.query.get(4)  # delete from db

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], '4')
        self.assertEqual(actor, None)
    
    def test_422_actor_not_exist(self):
        response = self.client().delete('/actors/999', headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMDdlNzg3YjhlM2EwMDY5ZmRhZDIzIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1NjgyODksImV4cCI6MTYzMDY1NDY4OSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NF4gX6e-lQcno4wN9cwqd4GZ4bm1sX9rlWnNnxuivV9zuKTKfa4Gu3Vo_NqxCiIRHA52QXx1UpEAurBQYjkCeqwObyd3_l0b_DO2KqK0PbAGOAYVNTxnIpxiwdYOh3ZSNiT-F0bOyLrHEwe3QKcb-SJY5w4CvhQim9kbPcmCECCcxFpJk2WmsZEzOD8C5JzlclgUFyFu01LbUrBMyyWgS_56hZu6B5myji3dGlTjwwKV7fplCgZ9eyLa1FqXJzR7-o-DxmK-OVf-bQuRFiKfccdC1ssEa-InBNIVjAvXd5VK9WpwkOPmaqFG_7fF0BlXaM9sXNTKlNQyJvjdSS8hJw"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # Tests for DELETE /movies/<id>
    def test_delete_movie(self):
        response = self.client().delete('/movies/2', headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMDdlNzg3YjhlM2EwMDY5ZmRhZDIzIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1NjgyODksImV4cCI6MTYzMDY1NDY4OSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NF4gX6e-lQcno4wN9cwqd4GZ4bm1sX9rlWnNnxuivV9zuKTKfa4Gu3Vo_NqxCiIRHA52QXx1UpEAurBQYjkCeqwObyd3_l0b_DO2KqK0PbAGOAYVNTxnIpxiwdYOh3ZSNiT-F0bOyLrHEwe3QKcb-SJY5w4CvhQim9kbPcmCECCcxFpJk2WmsZEzOD8C5JzlclgUFyFu01LbUrBMyyWgS_56hZu6B5myji3dGlTjwwKV7fplCgZ9eyLa1FqXJzR7-o-DxmK-OVf-bQuRFiKfccdC1ssEa-InBNIVjAvXd5VK9WpwkOPmaqFG_7fF0BlXaM9sXNTKlNQyJvjdSS8hJw"
            })
        data = json.loads(response.data)

        movie = Movie.query.get(2)  # delete from db

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], '2')
        self.assertEqual(movie, None)

    def test_422_movie_not_exist(self):
        response = self.client().delete('/movies/999', headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMDdlNzg3YjhlM2EwMDY5ZmRhZDIzIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1NjgyODksImV4cCI6MTYzMDY1NDY4OSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NF4gX6e-lQcno4wN9cwqd4GZ4bm1sX9rlWnNnxuivV9zuKTKfa4Gu3Vo_NqxCiIRHA52QXx1UpEAurBQYjkCeqwObyd3_l0b_DO2KqK0PbAGOAYVNTxnIpxiwdYOh3ZSNiT-F0bOyLrHEwe3QKcb-SJY5w4CvhQim9kbPcmCECCcxFpJk2WmsZEzOD8C5JzlclgUFyFu01LbUrBMyyWgS_56hZu6B5myji3dGlTjwwKV7fplCgZ9eyLa1FqXJzR7-o-DxmK-OVf-bQuRFiKfccdC1ssEa-InBNIVjAvXd5VK9WpwkOPmaqFG_7fF0BlXaM9sXNTKlNQyJvjdSS8hJw"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # Tests for POST /actors
    def test_add_actor(self):
        response = self.client().post('/actors', json=self.new_actor, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMDdlNzg3YjhlM2EwMDY5ZmRhZDIzIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1NjgyODksImV4cCI6MTYzMDY1NDY4OSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NF4gX6e-lQcno4wN9cwqd4GZ4bm1sX9rlWnNnxuivV9zuKTKfa4Gu3Vo_NqxCiIRHA52QXx1UpEAurBQYjkCeqwObyd3_l0b_DO2KqK0PbAGOAYVNTxnIpxiwdYOh3ZSNiT-F0bOyLrHEwe3QKcb-SJY5w4CvhQim9kbPcmCECCcxFpJk2WmsZEzOD8C5JzlclgUFyFu01LbUrBMyyWgS_56hZu6B5myji3dGlTjwwKV7fplCgZ9eyLa1FqXJzR7-o-DxmK-OVf-bQuRFiKfccdC1ssEa-InBNIVjAvXd5VK9WpwkOPmaqFG_7fF0BlXaM9sXNTKlNQyJvjdSS8hJw"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_id'])
        self.assertTrue(data['total_actors'])
    

    def test_422_add_actor(self):
        response = self.client().post('/actors', json={ }, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMDdlNzg3YjhlM2EwMDY5ZmRhZDIzIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1NjgyODksImV4cCI6MTYzMDY1NDY4OSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NF4gX6e-lQcno4wN9cwqd4GZ4bm1sX9rlWnNnxuivV9zuKTKfa4Gu3Vo_NqxCiIRHA52QXx1UpEAurBQYjkCeqwObyd3_l0b_DO2KqK0PbAGOAYVNTxnIpxiwdYOh3ZSNiT-F0bOyLrHEwe3QKcb-SJY5w4CvhQim9kbPcmCECCcxFpJk2WmsZEzOD8C5JzlclgUFyFu01LbUrBMyyWgS_56hZu6B5myji3dGlTjwwKV7fplCgZ9eyLa1FqXJzR7-o-DxmK-OVf-bQuRFiKfccdC1ssEa-InBNIVjAvXd5VK9WpwkOPmaqFG_7fF0BlXaM9sXNTKlNQyJvjdSS8hJw"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable') 
    
    # Tests for POST /movies
    def test_add_movie(self):
        response = self.client().post('/movies', json=self.new_movie, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMDdlNzg3YjhlM2EwMDY5ZmRhZDIzIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1NjgyODksImV4cCI6MTYzMDY1NDY4OSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NF4gX6e-lQcno4wN9cwqd4GZ4bm1sX9rlWnNnxuivV9zuKTKfa4Gu3Vo_NqxCiIRHA52QXx1UpEAurBQYjkCeqwObyd3_l0b_DO2KqK0PbAGOAYVNTxnIpxiwdYOh3ZSNiT-F0bOyLrHEwe3QKcb-SJY5w4CvhQim9kbPcmCECCcxFpJk2WmsZEzOD8C5JzlclgUFyFu01LbUrBMyyWgS_56hZu6B5myji3dGlTjwwKV7fplCgZ9eyLa1FqXJzR7-o-DxmK-OVf-bQuRFiKfccdC1ssEa-InBNIVjAvXd5VK9WpwkOPmaqFG_7fF0BlXaM9sXNTKlNQyJvjdSS8hJw"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie_id'])
        self.assertTrue(data['total_movies'])
    

    def test_422_add_movie(self):
        response = self.client().post('/movies', json=self.new_actor, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMDdlNzg3YjhlM2EwMDY5ZmRhZDIzIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1NjgyODksImV4cCI6MTYzMDY1NDY4OSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NF4gX6e-lQcno4wN9cwqd4GZ4bm1sX9rlWnNnxuivV9zuKTKfa4Gu3Vo_NqxCiIRHA52QXx1UpEAurBQYjkCeqwObyd3_l0b_DO2KqK0PbAGOAYVNTxnIpxiwdYOh3ZSNiT-F0bOyLrHEwe3QKcb-SJY5w4CvhQim9kbPcmCECCcxFpJk2WmsZEzOD8C5JzlclgUFyFu01LbUrBMyyWgS_56hZu6B5myji3dGlTjwwKV7fplCgZ9eyLa1FqXJzR7-o-DxmK-OVf-bQuRFiKfccdC1ssEa-InBNIVjAvXd5VK9WpwkOPmaqFG_7fF0BlXaM9sXNTKlNQyJvjdSS8hJw"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable') 
    
    # Tests for PATCH /actors/<id>/edit
    def test_edit_actor(self):
        response = self.client().patch('/actors/7/edit', json=self.edited_actor, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMDdlNzg3YjhlM2EwMDY5ZmRhZDIzIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1NjgyODksImV4cCI6MTYzMDY1NDY4OSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NF4gX6e-lQcno4wN9cwqd4GZ4bm1sX9rlWnNnxuivV9zuKTKfa4Gu3Vo_NqxCiIRHA52QXx1UpEAurBQYjkCeqwObyd3_l0b_DO2KqK0PbAGOAYVNTxnIpxiwdYOh3ZSNiT-F0bOyLrHEwe3QKcb-SJY5w4CvhQim9kbPcmCECCcxFpJk2WmsZEzOD8C5JzlclgUFyFu01LbUrBMyyWgS_56hZu6B5myji3dGlTjwwKV7fplCgZ9eyLa1FqXJzR7-o-DxmK-OVf-bQuRFiKfccdC1ssEa-InBNIVjAvXd5VK9WpwkOPmaqFG_7fF0BlXaM9sXNTKlNQyJvjdSS8hJw"
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
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMDdlNzg3YjhlM2EwMDY5ZmRhZDIzIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1NjgyODksImV4cCI6MTYzMDY1NDY4OSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NF4gX6e-lQcno4wN9cwqd4GZ4bm1sX9rlWnNnxuivV9zuKTKfa4Gu3Vo_NqxCiIRHA52QXx1UpEAurBQYjkCeqwObyd3_l0b_DO2KqK0PbAGOAYVNTxnIpxiwdYOh3ZSNiT-F0bOyLrHEwe3QKcb-SJY5w4CvhQim9kbPcmCECCcxFpJk2WmsZEzOD8C5JzlclgUFyFu01LbUrBMyyWgS_56hZu6B5myji3dGlTjwwKV7fplCgZ9eyLa1FqXJzR7-o-DxmK-OVf-bQuRFiKfccdC1ssEa-InBNIVjAvXd5VK9WpwkOPmaqFG_7fF0BlXaM9sXNTKlNQyJvjdSS8hJw"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

    # Tests for PATCH /movies/<id>/edit
    def test_edit_movie(self):
        response = self.client().patch('/movies/7/edit', json=self.edited_movie, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMDdlNzg3YjhlM2EwMDY5ZmRhZDIzIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1NjgyODksImV4cCI6MTYzMDY1NDY4OSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NF4gX6e-lQcno4wN9cwqd4GZ4bm1sX9rlWnNnxuivV9zuKTKfa4Gu3Vo_NqxCiIRHA52QXx1UpEAurBQYjkCeqwObyd3_l0b_DO2KqK0PbAGOAYVNTxnIpxiwdYOh3ZSNiT-F0bOyLrHEwe3QKcb-SJY5w4CvhQim9kbPcmCECCcxFpJk2WmsZEzOD8C5JzlclgUFyFu01LbUrBMyyWgS_56hZu6B5myji3dGlTjwwKV7fplCgZ9eyLa1FqXJzR7-o-DxmK-OVf-bQuRFiKfccdC1ssEa-InBNIVjAvXd5VK9WpwkOPmaqFG_7fF0BlXaM9sXNTKlNQyJvjdSS8hJw"
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
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMDdlNzg3YjhlM2EwMDY5ZmRhZDIzIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1NjgyODksImV4cCI6MTYzMDY1NDY4OSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImRlbGV0ZTptb3ZpZSIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiLCJwb3N0Om1vdmllIl19.NF4gX6e-lQcno4wN9cwqd4GZ4bm1sX9rlWnNnxuivV9zuKTKfa4Gu3Vo_NqxCiIRHA52QXx1UpEAurBQYjkCeqwObyd3_l0b_DO2KqK0PbAGOAYVNTxnIpxiwdYOh3ZSNiT-F0bOyLrHEwe3QKcb-SJY5w4CvhQim9kbPcmCECCcxFpJk2WmsZEzOD8C5JzlclgUFyFu01LbUrBMyyWgS_56hZu6B5myji3dGlTjwwKV7fplCgZ9eyLa1FqXJzR7-o-DxmK-OVf-bQuRFiKfccdC1ssEa-InBNIVjAvXd5VK9WpwkOPmaqFG_7fF0BlXaM9sXNTKlNQyJvjdSS8hJw"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable')

   
    # RBAC Tests
    # Tests for Casting Assistant Role 
    def test_assistant_get_actors(self):
        response = self.client().get("/actors", headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMGU4NmFmNDNhNjIwMDZhOGNkN2Y3IiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1OTUzNjMsImV4cCI6MTYzMDY4MTc2MywiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.VV_JQm1SPMoB_p2ZJ5z-_itV8bie7kgIDYaS_4Gk0Rp_0Z-wX5v0yu4Kt_U1qu_tAUVfhrLAmfKGNmiOPlZ_6hVvxxrT9x_BnNESCGA0B2f_arz0hLb9KCfIcqvwaqtqhLZZd8Qey_5h9i2lx4V6auGYm1tHIKzYmQFauPce7KpvxMwLURHxC7oCWYgkhvZZL4meDIzyBUj37CrfrTEeRSrKyFie8kIJmjtoIFkMCnw0AemkFJqcr48gfFkH4sI7ricAgh3mz3RLeYXN5SiZX7f1G2cBGznC19bWyLOGcjpkCS808T380158_xxMeCLb-XH_5n81_hoMskCmWbDO3g"
            })
        data = json.loads(response.data)  

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_403_add_actor(self):
        response = self.client().post('/actors', json=self.new_actor, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMGU4NmFmNDNhNjIwMDZhOGNkN2Y3IiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1OTUzNjMsImV4cCI6MTYzMDY4MTc2MywiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.VV_JQm1SPMoB_p2ZJ5z-_itV8bie7kgIDYaS_4Gk0Rp_0Z-wX5v0yu4Kt_U1qu_tAUVfhrLAmfKGNmiOPlZ_6hVvxxrT9x_BnNESCGA0B2f_arz0hLb9KCfIcqvwaqtqhLZZd8Qey_5h9i2lx4V6auGYm1tHIKzYmQFauPce7KpvxMwLURHxC7oCWYgkhvZZL4meDIzyBUj37CrfrTEeRSrKyFie8kIJmjtoIFkMCnw0AemkFJqcr48gfFkH4sI7ricAgh3mz3RLeYXN5SiZX7f1G2cBGznC19bWyLOGcjpkCS808T380158_xxMeCLb-XH_5n81_hoMskCmWbDO3g"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Forbidden')
    
    # RBAC Tests
    # Tests for Casting Director Role 
    def test_director_add_actor(self):
        response = self.client().post('/actors', json=self.new_actor, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMGViZDM3YjhlM2EwMDY5ZmRjOGYxIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1OTYwODUsImV4cCI6MTYzMDY4MjQ4NSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.n6VPhACRp5QjFNNOtcVG1isGhUdaR1bSnQFQ--e4Vk394DKgWzD-w_Zo_mMACclATyhrMx-hazyhzKNjwQ9dTl0KouOqWytRIc7Yv9ibRfznZ_0KLTar7NluDs4rwBIJIao4NeRsjZr33ksRjoip3aV655lfnpXZKmv_f_SKYKV37CIFts5vGhNko_RKIE_fhj2qPhKRp6-KO5_4UoHIooclI2QlGbtsGGHxYlzUoemRDbdPPQr192ydxyxTgxeWZnItOKCQX8Mn7zYXsPcYuStd439ETcBZmUl69kEmHxrSFTvlaATBpXt09StT_2dmou4Zes7YqQ-DedFVDAjemA"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor_id'])
        self.assertTrue(data['total_actors'])

    def test_403_add_movie(self):
        response = self.client().post('/movies', json=self.new_movie, headers={ 
            "Authorization": "bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjI5UnQzalNyNFVKMkhqZFpVV25VViJ9.eyJpc3MiOiJodHRwczovL2Rldi0wNHp2cnQ4bC51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjEzMGViZDM3YjhlM2EwMDY5ZmRjOGYxIiwiYXVkIjoiQ2FzdGluZy1BZ2VuY3kiLCJpYXQiOjE2MzA1OTYwODUsImV4cCI6MTYzMDY4MjQ4NSwiYXpwIjoiaW02UWhJZVFIek1ZdllYRlJyZWFha3VoVXV0UGRtbEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvciIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3IiLCJwYXRjaDptb3ZpZSIsInBvc3Q6YWN0b3IiXX0.n6VPhACRp5QjFNNOtcVG1isGhUdaR1bSnQFQ--e4Vk394DKgWzD-w_Zo_mMACclATyhrMx-hazyhzKNjwQ9dTl0KouOqWytRIc7Yv9ibRfznZ_0KLTar7NluDs4rwBIJIao4NeRsjZr33ksRjoip3aV655lfnpXZKmv_f_SKYKV37CIFts5vGhNko_RKIE_fhj2qPhKRp6-KO5_4UoHIooclI2QlGbtsGGHxYlzUoemRDbdPPQr192ydxyxTgxeWZnItOKCQX8Mn7zYXsPcYuStd439ETcBZmUl69kEmHxrSFTvlaATBpXt09StT_2dmou4Zes7YqQ-DedFVDAjemA"
            })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Forbidden')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
