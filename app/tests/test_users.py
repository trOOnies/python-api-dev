import sys
sys.path.append(".")
from pytest import mark
from jose import jwt
from app.backbone import schemas
from app.backbone.config import settings

# We have to import session as well, bc client needs it
   

def test_root(client):
    # session.query(models.Post....)
    res = client.get("/")
    assert res.json().get("message") == "Hello World"
    assert res.status_code == 200


def test_create_user(client):
    # VERY IMPORTANT! WE NEED A FINAL SLASH HERE, OR ELSE A REDIRECT IS RETURNED
    # This is because of using prefixes in FastAPI
    res = client.post(
        "/users/", json={"email": "hello123@gmail.com", "password": "password123"}
    )
    print(res.content)
    assert res.status_code == 201

    new_user = schemas.UserOut(**res.json())
    print(new_user)
    assert new_user.email == "hello123@gmail.com"


def test_login_user(client, test_user):    
    res = client.post(
        "/login", data={"username": test_user["email"], "password": test_user["password"]}
    )
    assert res.status_code == 200

    login_res = schemas.Token(**res.json())
    assert login_res.token_type == "bearer"

    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user["id"]


@mark.parametrize("email, password, status_code", [
    ("wrongemail@gmail.com", "password123", 403),
    ("@gmail.com", "wrongPassword", 403),
    ("wrongemail@gmail.com", "wrongPassword", 403),
    (None, "password123", 422),
    ("sanjeev@gmail.com", None, 422),
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
    # assert res.json().get("detail") == "Invalid credentials"
