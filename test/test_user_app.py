from app import schemas
#from .database import client, session
import pytest
import jwt
from app.config import settings


def test_create_user(client):
    res = client.post("/users/",json={"username": "tester345", "password": "password"})
    new_user = schemas.User(**res.json())
    assert new_user.username == "tester345"
    assert res.status_code == 201


def test_login(client, test_user):
    #res = client.post("/users/",json={"username": "tester345", "password": "password"})
    res = client.post("/login", data={"username": test_user['username'], "password": test_user['password']})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "Bearer"
    assert res.status_code == 200

@pytest.mark.parametrize("username,password,status_code",[
    ('wronguse','password',403),
    ('tester345','passwordsre',403),
    (None,"paswd",403)
]
)
def test_wrong_login(client, test_user, username, password, status_code):
    res = client.post("/login", data={"username": username, "password": password})
    assert res.status_code == status_code


def test_get_invalid_user(client):
    res = client.get("/users/4667")
    assert res.status_code == 404
