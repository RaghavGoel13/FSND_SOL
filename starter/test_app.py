import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db
from settings import DB_NAME, DB_USER, DB_PASSWORD, CASTING_ASSISTANT_JWT, CASTING_DIRECTOR_JWT, EXECUTIVE_PRODUCER_JWT


class TestCasesCapstone(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_USER, DB_PASSWORD, 'localhost:5432', DB_NAME)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        assistant_jwt = CASTING_ASSISTANT_JWT
        director_jwt = CASTING_DIRECTOR_JWT
        producer_jwt = EXECUTIVE_PRODUCER_JWT

        self.auth_headers = {
            "Casting Assistant": f'Bearer {assistant_jwt}',
            "Casting Director": f'Bearer {director_jwt}',
            "Executive Producer": f'Bearer {producer_jwt}'
        }

        self.movie = {
            "title": "My Name is Khan",
            "release_date": "2020-11-02",
            "rating": 10
        }

        self.actor = {
            "name": "Shahrukh Khan",
            "age": "50",
            "gender": "M",
            "phone": "123456666",
            "movie_id": 5
        }

    def tearDown(self):
        pass

    #  ----------------------------------------------------------------
    #  GET Movies Test Cases
    #  ----------------------------------------------------------------

    def test_get_movie_with_valid_role_assistant(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = self.client().get('/movies', headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["movies"]), type([]))

    def test_get_movie_with_valid_role_director(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        res = self.client().get('/movies', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["movies"]), type([]))

    def test_get_movie_with_valid_role_producer(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        res = self.client().get('/movies', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["movies"]), type([]))

    def test_get_movie_with_401(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    #  ----------------------------------------------------------------
    #  GET Movie by id Test Cases
    #  ----------------------------------------------------------------

    def test_get_movie_by_id_with_valid_role_assistant(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        movie_id = 5
        res = self.client().get(f'/movies/{movie_id}', headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["movies"]), type([]))

    def test_get_movie_by_id_with_valid_role_director(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        movie_id = 5
        res = self.client().get(f'/movies/{movie_id}', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["movies"]), type([]))

    def test_get_movie_by_id_with_valid_role_producer(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        movie_id = 5
        res = self.client().get(f'/movies/{movie_id}', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["movies"]), type([]))

    def test_get_movie_by_id_with_401(self):
        movie_id = 5
        res = self.client().get(f'/movies/{movie_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    #  ----------------------------------------------------------------
    #  POST Movies Test Cases
    #  ----------------------------------------------------------------

    def test_add_movie_with_valid_invalid_role_assistant_unauthorised(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = self.client().post(f'/movies',
                                 json=self.movie, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_add_movie_with_invalid_role_director_unauthorised(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        res = self.client().post(f'/movies',
                                 json=self.movie, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_add_movie_with_valid_role_producer(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        res = self.client().post(f'/movies',
                                 json=self.movie, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])

    def test_add_movie_with_valid_role_producer_bad_request(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        incorrect_movie_payload = {"title": "Movie"}
        res = self.client().post(f'/movies',
                                 json=incorrect_movie_payload, headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Bad Request")

    #  ----------------------------------------------------------------
    #  PATCH Movies Test Cases
    #  ----------------------------------------------------------------

    def test_update_movie_with_valid_invalid_role_assistant_unauthorised(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        movie_id = 2
        update_movie_payload = {"title": "My Name is Khan 2"}
        res = self.client().patch(f'/movies/{movie_id}',
                                  json=update_movie_payload, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_update_movie_with_valid_role_director(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        movie_id = 5
        update_movie_payload = {"title": "My Name is Khan 2"}
        res = self.client().patch(f'/movies/{movie_id}',
                                  json=update_movie_payload, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])

    def test_update_movie_with_valid_role_producer(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        movie_id = 5
        update_movie_payload = {"title": "My Name is Khan 2"}
        res = self.client().patch(f'/movies/{movie_id}',
                                  json=update_movie_payload, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])

    def test_update_movie_with_movie_not_found(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        movie_id = -1
        update_movie_payload = {"title": "My Name is Khan 2"}
        res = self.client().patch(f'/movies/{movie_id}',
                                  json=update_movie_payload, headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_update_movie_with_movie_401(self):
        movie_id = 5
        update_movie_payload = {"title": "My Name is Khan 2"}
        res = self.client().patch(f'/movies/{movie_id}', json=update_movie_payload)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    #  ----------------------------------------------------------------
    #  DELETE Movies Test Cases
    #  ----------------------------------------------------------------

    def test_delete_movie_with_valid_invalid_role_assistant_unauthorised(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        movie_id = 2
        res = self.client().delete(f'/movies/{movie_id}', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_delete_movie_with_valid_role_director_unauthorised(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        movie_id = 4
        res = self.client().delete(f'/movies/{movie_id}', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_delete_movie_with_valid_role_producer(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        res = self.client().get('/movies', headers=header_obj)
        data = json.loads(res.data)
        total_movies = len(data["movies"])
        movie_id = data["movies"][total_movies - 1]["id"]
        res = self.client().delete(f'/movies/{movie_id}', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_movie_with_movie_not_found(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        movie_id = -1
        res = self.client().delete(f'/movies/{movie_id}', headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    #  ----------------------------------------------------------------
    #  GET Actors Test Cases
    #  ----------------------------------------------------------------

    def test_get_actor_with_valid_role_assistant(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = self.client().get('/actors', headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["actors"]), type([]))

    def test_get_actor_with_valid_role_director(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        res = self.client().get('/actors', headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["actors"]), type([]))

    def test_get_actor_with_valid_role_producer(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        res = self.client().get('/actors', headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["actors"]), type([]))

    def test_get_actor_with_401(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    #  ----------------------------------------------------------------
    #  GET Actor By Id Test Cases
    #  ----------------------------------------------------------------

    def test_get_actor_by_id_with_valid_role_assistant(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        actor_id = 4
        res = self.client().get(f'/actors/{actor_id}', headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["actors"]), type([]))

    def test_get_actor_by_id_with_valid_role_director(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        actor_id = 4
        res = self.client().get(f'/actors/{actor_id}', headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["actors"]), type([]))

    def test_get_actor_by_id_with_valid_role_producer(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        actor_id = 4
        res = self.client().get(f'/actors/{actor_id}', headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(type(data["actors"]), type([]))

    def test_get_actor_by_id_with_401(self):
        actor_id = 4
        res = self.client().get(f'/actors/{actor_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    #  ----------------------------------------------------------------
    #  POST Actors Test Cases
    #  ----------------------------------------------------------------

    def test_add_actor_with_valid_invalid_role_assistant_unauthorised(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        res = self.client().post(f'/actors',
                                 json=self.actor, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_add_movie_with_valid_role_director(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        res = self.client().post(f'/actors',
                                 json=self.actor, headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])

    def test_add_actor_with_valid_role_producer(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        res = self.client().post(f'/actors', json=self.actor, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])

    def test_add_actor_with_valid_role_producer_bad_request(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        incorrect_actor_payload = {"name": "Kamal Khan"}
        res = self.client().post(f'/actors',
                                 json=incorrect_actor_payload, headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], "Bad Request")

    #  ----------------------------------------------------------------
    #  DELETE Actors Test Cases
    #  ----------------------------------------------------------------

    def test_delete_actor_with_valid_invalid_role_assistant_unauthorised(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        actor_id = 4
        res = self.client().delete(f'/actors/{actor_id}', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_delete_actor_with_valid_role_director(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        res = self.client().get('/actors', headers=header_obj)
        data = json.loads(res.data)
        total_actors = len(data["actors"])
        actor_id = data["actors"][total_actors - 1]["id"]
        res = self.client().delete(f'/actors/{actor_id}', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_movie_with_valid_role_producer(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        res = self.client().get('/actors', headers=header_obj)
        data = json.loads(res.data)
        total_actors = len(data["actors"])
        actor_id = data["actors"][total_actors - 1]["id"]
        res = self.client().delete(f'/actors/{actor_id}', headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_delete_actor_with_actor_not_found(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        actor_id = -1
        res = self.client().delete(f'/actors/{actor_id}', headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_delete_actor_with_401(self):
        actor_id = 5
        res = self.client().delete(f'/actors/{actor_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    #  ----------------------------------------------------------------
    #  PATCH Actors Test Cases
    #  ----------------------------------------------------------------

    def test_update_actor_with_valid_invalid_role_assistant_unauthorised(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Assistant"]
        }
        actor_id = 4
        res = self.client().patch(f'/actors/{actor_id}',
                                  json=self.actor, headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    def test_update_actor_with_valid_role_director(self):
        header_obj = {
            "Authorization": self.auth_headers["Casting Director"]
        }
        actor_id = 4
        res = self.client().patch(f'/actors/{actor_id}',
                                  json=self.actor, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])

    def test_update_actor_with_valid_role_producer(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        actor_id = 4
        res = self.client().patch(f'/actors/{actor_id}',
                                  json=self.actor, headers=header_obj)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])

    def test_update_actor_with_actor_not_found(self):
        header_obj = {
            "Authorization": self.auth_headers["Executive Producer"]
        }
        actor_id = -1
        update_actor_payload = {"name": "Sunil Shetty"}
        res = self.client().patch(f'/actors/{actor_id}',
                                  json=update_actor_payload, headers=header_obj)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])

    def test_update_actor_with_401(self):
        actor_id = 4
        res = self.client().patch(f'/actors/{actor_id}',
                                  json=self.actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
