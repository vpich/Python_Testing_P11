from flask_testing import TestCase
from server import app
import server


FAKE_CLUBS = [
    {
        "name": "Few_points_Club",
        "email": "test@club1.com",
        "points": "3"
    },
    {
        "name": "Many_points_Club",
        "email": "test@club2.com",
        "points": "12"
    },
]

FAKE_COMPETITIONS = [
    {
        "name": "Current_competition",
        "date": "2024-03-27 10:00:00",
        "numberOfPlaces": "5"
    },
    {
        "name": "Past_competition",
        "date": "2020-10-22 13:30:00",
        "numberOfPlaces": "15"
    }
]


class UrlsTest(TestCase):

    def create_app(self):
        app.config["TESTING"] = True
        return app

    def setUp(self):
        server.clubs = FAKE_CLUBS
        server.competitions = FAKE_COMPETITIONS

    def test_access_index_success(self):
        response = self.client.get("/")
        self.assertTemplateUsed('index.html')
        assert response.status_code == 200
