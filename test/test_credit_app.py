from app import models
import pytest


@pytest.fixture()
def credit_on_suggest(test_movie, session, test_user):
    new_credit = models.Credit(movie_id=test_movie[-1].id,username=test_user['username'])
    session.add(new_credit)
    session.commit()

def test_credit_on_suggest(authorized_client, test_movie):
    res = authorized_client.post("/credit/", json={"movie_id": test_movie[-1].id, "dir": 1})
    assert res.status_code == 201


def test_credit_on_credited_suggest(authorized_client, test_movie, credit_on_suggest):
    res = authorized_client.post("/credit/", json={"movie_id": test_movie[-1].id, "dir": 1})
    assert res.status_code == 409


def test_uncredit_on_suggest(authorized_client, test_movie, credit_on_suggest):
    res = authorized_client.post("/credit/", json={"movie_id": test_movie[-1].id, "dir": 0})
    assert res.status_code == 201


def test_credit_on_non_existing_suggest(authorized_client, test_movie):
    res = authorized_client.post("/credit/", json={"movie_id": 63324, "dir": 1})
    assert res.status_code == 404


def test_uncredit_on_non_existing_suggest(authorized_client, test_movie, credit_on_suggest):
    res = authorized_client.post("/credit/", json={"movie_id": 3425387, "dir": 0})
    assert res.status_code == 404
