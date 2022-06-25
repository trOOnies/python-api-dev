import psycopg2
import time
import os
import backbone.models as models
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from backbone.routers import post, user
from backbone.database import engine

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


app.include_router(post.router)
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
