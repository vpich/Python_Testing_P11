import server


def test_should_load_clubs_list():
    sut = server.loadClubs()
    assert type(sut) == list


def test_should_load_clubs_keys():
    sut = server.loadClubs()
    whitelist_keys = ["name", "email", "points"]
    sut_keys = []
    sut_keys = [key for key in sut[0].keys() if key not in sut_keys]
    assert sut_keys == whitelist_keys


def test_should_load_competitions_list():
    sut = server.loadCompetitions()
    assert type(sut) == list


def test_should_load_competitions_keys():
    sut = server.loadCompetitions()
    whitelist_keys = ["name", "date", "numberOfPlaces"]
    sut_keys = []
    sut_keys = [key for key in sut[0].keys() if key not in sut_keys]
    assert sut_keys == whitelist_keys


def test_check_future_date():
    sut = server.check_competition_date
    date = "2024-05-11 15:00:00"
    expected_value = True
    assert sut(date) == expected_value


def test_check_past_date():
    sut = server.check_competition_date
    date = "2020-03-27 10:00:00"
    expected_value = False
    assert sut(date) == expected_value
