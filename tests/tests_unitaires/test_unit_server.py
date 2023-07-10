import server
import pytest


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


@pytest.mark.parametrize("date, expected_value", [
    ("2020-03-27 10:00:00", False),
    ("2024-05-11 10:00:00", True),
])
def test_check_date(date, expected_value):
    assert server.check_competition_date(date) == expected_value
