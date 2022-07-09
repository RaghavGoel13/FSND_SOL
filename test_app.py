import json
import unittest

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db


class TestCasesCapstone(unittest.TestCase):
    def setUp(self):
        DATABASE_URL = 'postgresql://postgres:admin@localhost:5432/postgres'
        CASTING_ASSISTANT_JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktjOUt2MG1JVEUzaFZHcnJSSHhGUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1jYXBzdG9uZS1ydi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJjMWQ2ZGIzOTVhOWY1YTBiYTcxOGYzIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2NTczOTc3NzAsImV4cCI6MTY1NzQwNDk3MCwiYXpwIjoiUUVHalZLeWlJQVdSM2tOWk94emRxNUtoQUpHcnRWT1EiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.AjmZ9jWWpObFhtLUhF0OMzKs8EmOjxH7qFKDjrFeLSWJH2s66jd_7wcH6MUKu_peCiOzgpe8PYkLQQ3mMeGnKRkHrQM3io73dzTzwzNKvvDCXO932n8iFokHIAg6S5ZIb__qZDTtGDbhlM4d1dYBYU7SIlYhs0jP18OLyIqSApX6XZQcI89N8fAMA7n-tLzv5PtZVlowLF4ybE2x6VsrBmJCndRzzjcElnu352EX_oXjmlZIs5KAkPRjpw2ZRnmzVsQYlWFD2ClvalL5k7os6eLN8If7-HuxjsIwXoWC8Y6HtYo_rtASQPQWcclg-7GgJ6xA4SuwO7DoXO-1pT1Sbg'
        CASTING_DIRECTOR_JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktjOUt2MG1JVEUzaFZHcnJSSHhGUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1jYXBzdG9uZS1ydi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJjMWQ2YzBmZTA2MjkxMTYwOTJmMzlhIiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2NTczOTc3MTAsImV4cCI6MTY1NzQwNDkxMCwiYXpwIjoiUUVHalZLeWlJQVdSM2tOWk94emRxNUtoQUpHcnRWT1EiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBvc3Q6YWN0b3JzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiXX0.ceYdLcSsMvL0JQROt6dVe0fHtx7gPdm295Qb05W1zSXJTUS6_99lJMskdytRYHpOTgNQT_CijwJpR-9dnHr3q50zX0f9IKtnfHMJM7Bs7Xvgu4OnqnJRDA-pQ_Y36yE-aWqWN9J0BZR74v_nZXl0kh7NgY7XiGKjjExrRCOYo55y9F7qgYOKcqU4VVKBhADIP12SKL-lvBVgUVzX-J4wPXkbW9hdDEsyBC2m9_FYXuRat3J1oehPzvo8OmHE4cCKCZCqMHQ4I76t3qjmPCvglQuLN9LpzKXowrSJIGp_h1pXRNKy9Uu9Sy6qrMnyggepKYxw7BHGVX6w1ks9_PVd-w'
        EXECUTIVE_PRODUCER_JWT = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IktjOUt2MG1JVEUzaFZHcnJSSHhGUSJ9.eyJpc3MiOiJodHRwczovL2Rldi1jYXBzdG9uZS1ydi51cy5hdXRoMC5jb20vIiwic3ViIjoiYXV0aDB8NjJjMWQ2ZWJmZTA2MjkxMTYwOTJmM2E1IiwiYXVkIjoiY2Fwc3RvbmUiLCJpYXQiOjE2NTczOTcwNjEsImV4cCI6MTY1NzQwNDI2MSwiYXpwIjoiUUVHalZLeWlJQVdSM2tOWk94emRxNUtoQUpHcnRWT1EiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIiwidXBkYXRlOmFjdG9ycyIsInVwZGF0ZTptb3ZpZXMiXX0.mQiNa_XBLrFOZ82A1PMQ4K_t8SGWRgFLXlLSwBsapa0WQU6Eu2v2Mm3UPXGZONnTYbAYE9aQPV5hL7JHldFxaQxCRHmzZzAHmeIXNXxAuQ0shwCnWppPc7XOjl-jW0pBcGD0xuDNoDzbejvO6HXeEBp39iGvPwprVyytHSgNYxN9N9L5evBFUf4mUshM_NibEHoS7HGD8A0dFYX9DvMsjW_BtOuZ1HYUfb8r0zHtrfnao7MUWf8ij3mkuiaK62fTUznM5qH9YBr_Nq2cHSnAWwW2V3sQzvVVRnr2Lu15af59YR1mC9hmaVUjVu17-PLtBSJFvOv45E66q78UuxATiw'

        assistant_jwt = CASTING_ASSISTANT_JWT
        director_jwt = CASTING_DIRECTOR_JWT
        producer_jwt = EXECUTIVE_PRODUCER_JWT

        self.auth_headers = {
            "Casting Assistant": f'Bearer {assistant_jwt}',
            "Casting Director": f'Bearer {director_jwt}',
            "Executive Producer": f'Bearer {producer_jwt}'
        }
        self.database_path = DATABASE_URL

        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

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

    def test_add_actor_with_valid_role_director(self):
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

    def test_delete_actor_with_valid_role_producer(self):
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
