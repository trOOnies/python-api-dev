import os
import time
import psycopg2
import models
import schemas
from typing import List
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from fastapi import FastAPI, HTTPException, Response, status, Depends
from database import engine, get_db
from utils import hash

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


print("Connecting to database...")
while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastapi",
            user="postgres",
            password=os.environ.get("PSQL_PASS"),
            cursor_factory=RealDictCursor,
        )
        cursor = conn.cursor()
        print("Database connection established")
        break
    except Exception as err:
        print("Database connection failed")
        print("Error:", err)
    time.sleep(2)


my_posts = [
    {
        "title": "Hello World",
        "content": "My first post",
        "published": True,
        "id": 1,
    },
]


def find_index_post(id):
    return next(i for i, p in enumerate(my_posts) if p["id"] == id)


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (id,))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} was not found"
        )
    return post


@app.post(
    "/posts",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Post,
)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # DO USE execute() and not f-strings! The library shields us from SQL injections
    # cursor.execute(
    #     f"""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #     (post.title, post.content, post.published)
    # )
    # new_post = cursor.fetchone()
    # conn.commit()
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    # This retrieves the created post and store it again (replaces the RETURNING)
    db.refresh(new_post)  # need orm_mode to be able to be returned
    return new_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist"
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    # conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    # cursor.execute(
    #     """UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #     (post.title, post.content, post.published, id)
    # )
    # updated_post = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    present_post = post_query.first()
    if present_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} does not exist"
        )
    # conn.commit()
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


@app.post(
    "/users",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.UserOut
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user.password = hash(user.password)

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist"
        )
    return user
