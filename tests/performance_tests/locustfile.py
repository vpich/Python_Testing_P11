from locust import HttpUser, task, between


class ProjectPerfTest(HttpUser):
    wait_time = between(1, 5)

    def on_start(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task
    def index_page(self):
        self.client.get("/")

    @task
    def login_page(self):
        self.client.post("/showSummary", {"email": "john@simplylift.co"})

    @task
    def booking_page(self):
        club = "Simply Lift"
        competition = "Spring Festival"
        self.client.get(f'/book/{competition}/{club}')

    @task
    def purchase_page(self):
        club = "Simply Lift"
        competition = "Spring Festival"
        places = "1"
        self.client.post("/purchasePlaces", {"club": club, "competition": competition, "places": places})

    @task
    def points_board_page(self):
        self.client.get("/pointsBoard")

    @task
    def logout(self):
        self.client.get('/logout')


