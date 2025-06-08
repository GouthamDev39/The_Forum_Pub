from typing import List
from app import schemas
import pytest

def test_get_all_movie(authorized_client,test_movie):
    res = authorized_client.get("/movies/")
    assert len(res.json()) == len(test_movie)
    assert res.status_code == 200


def test_unauthorized_access_get_all(client,test_movie):
    res = client.get("/movies/")
    assert res.status_code == 401


def test_unauthorized_access_get_one(client,test_movie):
    res = client.get("/movies/1")
    assert res.status_code == 401


def test_get_one_movie(authorized_client, test_movie):
    res = authorized_client.get(f"movies/{test_movie[0].id}")
    # print(res.json())
    movie = schemas.MovieOut(**res.json())
    assert movie.id == test_movie[0].id
    assert movie.name == test_movie[0].name
    assert movie.ott == test_movie[0].ott
    assert res.status_code == 200



@pytest.mark.parametrize("name,description,ott, status_code",[
   ("The Dark Knight", "One of the best ever","Jio",201),
   ("The Dark Knight Rises", "One","Jio",422),
   ("The Batman", "One of the best ever","",201),
   (None, "One of the best ever","Jio",422),

])
def test_create_movie(authorized_client, test_movie, test_user,name,description, ott, status_code):
    res = authorized_client.post("/movies/",json={
        "name": name, "description": description, "ott": ott
    } )
    if status_code == 201:
        new_movie = schemas.MoviePost(**res.json())
        #print(new_movie)
        assert new_movie.name == name
        assert new_movie.description == description
        assert new_movie.ott == ott
        assert new_movie.suggested_by == test_user['username']
    assert res.status_code == status_code


def test_unauthorized_access_create_post(client,test_movie, test_user):

    res = client.post("/movies/",json={"name":"name", "description":"descriptiomn","ott":"ott"})
    assert res.status_code == 401


def test_unauthorized_access_delete_post(client,test_movie, test_user):

    res = client.delete(f"/movies/{test_movie[0].id}")
    assert res.status_code == 401




def test_delete_movie(authorized_client,test_movie, test_user):
    res = authorized_client.delete(f"/movies/{test_movie[0].id}")
    assert test_movie[0].suggested_by == test_user['username']
    assert res.status_code == 204


def test_delete_non_existing_movie(authorized_client,test_movie, test_user):
    res = authorized_client.delete(f"/movies/2345343454")
    assert res.status_code == 404


def test_delete_non_owner_suggetion(authorized_other_client,test_movie, test_user):
    res = authorized_other_client.delete(f"/movies/{test_movie[0].id}")
    assert res.status_code == 403


def test_edit_movie(authorized_client, test_movie, test_user):
    res = authorized_client.put(f"/movies/{test_movie[0].id}", json={"name":"test","description":"One of the best Batman projects",
                    "ott":"Netflix"})
    edited= schemas.MoviePut(**res.json())
    assert edited.name == test_movie[0].name
    assert edited.description == "One of the best Batman projects"
    assert edited.ott == "Netflix"
    assert res.status_code == 201

def test_edit_movie_by_non_owner(authorized_client, test_movie):
    res = authorized_client.put(f"/movies/{test_movie[-1].id}", json={"name":"test","description":"One of the best Batman projects",
                    "ott":"Netflix"})
    assert res.status_code == 403


def test_get_owner_movies(authorized_client, test_movie, test_user):
    res = authorized_client.get(f"/movies/1/my_movies")
    assert res.status_code == 200
