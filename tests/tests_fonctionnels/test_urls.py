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
        "points": "13"
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
    },
    {
        "name": "Limit_competition",
        "date": "2024-10-22 13:30:00",
        "numberOfPlaces": "20"
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

    # ERROR n1
    def test_login_fail(self):
        response = self.client.post("/showSummary", data={"email": "wrong@club.com"})
        assert response.status_code == 400
        assert b"Sorry, that email was not found." in response.data

    def test_login_success(self):
        response = self.client.post("/showSummary", data={"email": FAKE_CLUBS[0]["email"]})
        assert response.status_code == 200
        self.assertTemplateUsed("welcome.html")
        self.assertContext("club", FAKE_CLUBS[0])

    # BUG n2
    def test_purchase_places_unavalaible_points_fail(self):
        response = self.client.post("/purchasePlaces", data={
            "competition": FAKE_COMPETITIONS[0]["name"],
            "club": FAKE_CLUBS[0]["name"],
            "places": 4})
        assert response.status_code == 400
        assert b"not allowed to use unavalaible points." in response.data

    def test_purchase_places_success(self):
        response = self.client.post("/purchasePlaces", data={
            "competition": FAKE_COMPETITIONS[0]["name"],
            "club": FAKE_CLUBS[0]["name"],
            "places": 1})
        assert response.status_code == 200

    # BUG n4
    def test_book_more_than_limit_places_fail(self):
        response = self.client.post("/purchasePlaces", data={
            "competition": FAKE_COMPETITIONS[2]["name"],
            "club": FAKE_CLUBS[1]["name"],
            "places": 13})
        assert response.status_code == 400
        assert b"more than 12 places per competitions." in response.data

    # BUG supplémentaire
    def test_book_more_than_max_places_fail(self):
        response = self.client.post("/purchasePlaces", data={
            "competition": FAKE_COMPETITIONS[0]["name"],
            "club": FAKE_CLUBS[1]["name"],
            "places": 7})
        assert response.status_code == 400
        assert b"more than places avalaible in this competition." in response.data

    # BUG n5
    def test_access_book_past_competition_fail(self):
        competition = FAKE_COMPETITIONS[1]["name"]
        club = FAKE_CLUBS[0]["name"]
        response = self.client.get(f"/book/{competition}/{club}")
        assert response.status_code == 200
        self.assertTemplateUsed("welcome.html")
        assert b"You can&#39;t book a previous competition" in response.data

    def test_access_book_current_competition_success(self):
        competition = FAKE_COMPETITIONS[0]["name"]
        club = FAKE_CLUBS[0]["name"]
        response = self.client.get(f"/book/{competition}/{club}")
        assert response.status_code == 200
        self.assertTemplateUsed("booking.html")