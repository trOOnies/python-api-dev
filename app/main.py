import backbone.models as models
from fastapi import FastAPI
from backbone.routers import post, user, auth
from backbone.database import engine
from backbone.config import settings

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

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
app.include_router(auth.router)


@app.get("/")
def root():
    return {"message": "Hello World"}
