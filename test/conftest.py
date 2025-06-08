from app.main import app
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app import schemas, models
from app.config import settings
from app.database import get_db
from app.oauth2 import create_access_token
from app.database import Base



SQLALCHEMY_DATABASE_URL = f"postgresql://batman:pswd@localhost:5432/test_db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)



client = TestClient(app)


@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    #before running test
    def override_get_db():#dependency
        try:
            yield session
        finally:
            session.close()
        
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
        #after running test


@pytest.fixture()
def test_user(client):
    user_data = {"username": "tester",
                "password": "password"}
    res = client.post("/users/",json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user


@pytest.fixture()
def test_user2(client):
    user_data = {"username": "tester1",
                "password": "password"}
    res = client.post("/users/",json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user

@pytest.fixture()
def test_other_user(client):
    user_data = {"username": "tester2",
                "password": "password"}
    res = client.post("/users/",json=user_data)
    new_user = res.json()
    new_user['password'] = user_data['password']
    assert res.status_code == 201
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def other_token(test_other_user):
    return create_access_token({"user_id": test_other_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers ={
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client


@pytest.fixture
def authorized_other_client(client, other_token):
    client.headers ={
        **client.headers,
        "Authorization": f"Bearer {other_token}"
    }

    return client


@pytest.fixture
def test_movie(session, test_user, test_user2):
    movies_data = [

        {
		"name": "batman",
		"ott": "jio",
		"description": "aaaaaaaaaaa",
		"suggested_by": test_user['username'],
	},
	{
		"name": "batman begins",
		"ott": "jio",
		"description": "aaaaaaaaaa",
		"suggested_by": test_user['username'],
	},
    {
		"name": "harry potter",
		"ott": "jio",
		"description": "aaaaaaaaaa",
		"suggested_by": test_user2['username'],
	}
    ]

    def create_movie_model(movie):
        return models.MovieSuggest(**movie)


    movie_map = map(create_movie_model, movies_data)
    movies = list(movie_map)


    session.add_all(movies)
    session.commit()

    movies = session.query(models.MovieSuggest).all()
    return movies