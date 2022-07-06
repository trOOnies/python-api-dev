from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backbone.routers import post, user, auth, vote

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

origins = ["*"]  # TODO: PLEASE DO NOT LEAVE THIS LIKE THIS IN A PRODUCTION ENV!
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/")
def root():
    return {"message": "Hello World"}
