import sys
sys.path.append(".")
from pytest import mark
from app.backbone import schemas


def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200
    posts = [schemas.PostOut(**p) for p in res.json()]
    assert len(posts) == len(test_posts)
    assert posts[0].Post.id == test_posts[0].id  # maybe not ideal? does it get shuffled?


def test_unauthorized_user_get_all_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 200
    post = schemas.PostOut(**res.json())
    assert post.Post.id == test_posts[0].id  # maybe not ideal? does it get shuffled?
    assert post.Post.content == test_posts[0].content  # maybe not ideal? does it get shuffled?
    assert post.Post.title == test_posts[0].title  # maybe not ideal? does it get shuffled?


def test_unauthorized_user_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/88888")
    assert res.status_code == 404


@mark.parametrize("title, content, published", [
    ("awesome new title", "i am a content", True),
    ("favorite pizza", "i am a content", False),
    ("awesome new title", "i love pepperoni", True),
    ("tallest skyscrapers", "wahoo", False),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post("/posts/", json={"title": title, "content": content, "published": published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.owner_id == test_user["id"]
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published


def test_create_post_default_published_true(
    authorized_client,
    test_user,
    test_posts
):
    res = authorized_client.post(
        "/posts/",
        json={"title": "awesome new title", "content": "i am a content"}
    )
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.owner_id == test_user["id"]
    assert created_post.published is True


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post(
        "/posts/",
        json={"title": "awesome new title", "content": "i am a content"}
    )
    assert res.status_code == 401


def test_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_non_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/99999")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_user_2, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(
        f"/posts/{test_posts[0].id}",
        json=data
    )
    assert res.status_code == 200
    updated_post = schemas.Post(**res.json())
    assert updated_post.title == data["title"]
    assert updated_post.content == data["content"]
    assert updated_post.id == data["id"]


def test_unauthorized_user_update_post(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[0].id
    }
    res = client.put(
        f"/posts/{test_posts[3].id}",
        json=data
    )
    assert res.status_code == 401


def test_update_post_non_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": 98989
    }
    res = authorized_client.put("/posts/98989", json=data)    
    assert res.status_code == 404


def test_update_other_user_post(authorized_client, test_user, test_user_2, test_posts):
    data = {
        "title": "updated title",
        "content": "updated content",
        "id": test_posts[3].id
    }
    res = authorized_client.put(
        f"/posts/{test_posts[3].id}",
        json=data
    )
    assert res.status_code == 403
