import random

from fastapi import FastAPI, Query
from pydantic import BaseModel

from app.bootstrap import cors, exceptions
from app.routes.search import search_router

app = FastAPI()
app.include_router(search_router, prefix="/search", tags=["search"])

cors.setup_cors(app)
exceptions.setup_exception_handlers(app)


@app.get("/")
def get_root():
    """And example showing how FastAPI converts python dicts to JSON"""
    return {"message": "Hello World"}


@app.get("/example/")
def get_with_query(arg: str = Query(default=None)):
    """An example showing how to use query parameters"""
    return {"arg": arg}


class UserIn(BaseModel):
    """A pydantic model for the information expected from the ui"""
    name: str
    age: int


class UserOut(UserIn):
    """A pydantic model for the information returned to the ui"""
    id: int


@app.post("/validate/", response_model=UserOut)
def validate_data(user: UserIn):
    """An example showing how to validate data from the ui and return a response"""
    return {
        "id": random.randint(100, 1000),
        **user.dict(),
    }
