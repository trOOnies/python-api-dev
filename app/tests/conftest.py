from cgi import test
from email.iterators import typed_subpart_iterator
import sys
sys.path.append(".")
from pytest import fixture
from app.main import app
from app.backbone import models
from app.backbone.config import settings
from app.backbone.database import get_db, Base
from app.backbone.oauth2 import create_access_token
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from fastapi.testclient import TestClient
# from alembic import command


# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password123@localhost:5432/fastapi_test"
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.db_username}:{settings.db_password}@{settings.db_hostname}:{settings.db_port}/{settings.db_name}_test"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False}  # for SQLite
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)


# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
# app.dependency_overrides[get_db] = override_get_db


@fixture()
def session():
    """yield makes it so that we can run code before and after our test"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)  # keep tables
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# CLEAN SLATE METHOD
# @fixture
# def client():
#     Base.metadata.create_all(bind=engine)
#     yield TestClient(app)
#     Base.metadata.drop_all(bind=engine)  # clean slate


# KEEP TABLES METHOD
# @fixture
# def client():
#     """yield makes it so that we can run code before and after our test"""
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)  # keep tables
#     yield TestClient(app)


# ALEMBIC
# @fixture
# def client():
#     command.upgrade("head")
#     yield TestClient(app)
#     command.downgrade("base")


# Use session as well
@fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@fixture
def test_user(client):
    # models.User(...)
    user_data = {"email": "sanjeev@gmail.com", "password": "password123"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@fixture
def test_user_2(client):
    # He could have made a test_users, but he forgot to do it so
    user_data = {"email": "sanjeev1@gmail.com", "password": "password456"}
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user


@fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client


@fixture
def test_posts(session, test_user, test_user_2):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user["id"]
        },
        {
            "title": "2nd title",
            "content": "2nd content",
            "owner_id": test_user["id"]
        },
        {
            "title": "3rd title",
            "content": "3rd content",
            "owner_id": test_user["id"]
        },
        {
            "title": "another title by tu2",
            "content": "such content",
            "owner_id": test_user_2["id"]
        }
    ]
    session.add_all([models.Post(**pdata) for pdata in posts_data])
    session.commit()
    posts = session.query(models.Post).all()
    return posts
