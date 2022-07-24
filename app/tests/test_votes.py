import sys
sys.path.append(".")
from pytest import fixture
from app.backbone import schemas, models


@fixture
def test_vote(session, test_user, test_posts):
    new_vote = models.Vote(post_id=test_posts[3].id, user_id=test_user["id"])
    session.add(new_vote)
    session.commit()
    return new_vote


def test_vote_on_post(authorized_client, test_user, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 201
    # assert schemas.Vote(**res.json()).id == 1  # doesnt return the vote, should query it


def test_vote_twice_post(authorized_client, test_user, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409


def test_unauthorized_vote_on_post(client, test_user, test_posts):
    res = client.post("/vote/", json={"post_id": test_posts[0].id, "dir": 1})
    assert res.status_code == 401


def test_vote_post_non_exist(authorized_client, test_user, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": 99331, "dir": 1})
    assert res.status_code == 404


def test_delete_vote(authorized_client, test_user, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201
    # assert schemas.Vote(**res.json()).id == 0  # doesnt return the vote, should query it


def test_unauthorized_delete_vote(client, test_user, test_posts, test_vote):
    res = client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 401


def test_delete_non_voted(authorized_client, test_user, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404
