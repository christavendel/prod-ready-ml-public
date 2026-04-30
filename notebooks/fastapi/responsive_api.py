from datetime import datetime

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# class User(BaseModel): # First version, but with the addition of SafeUser you define some attributes multiple times
#     id: int
#     name: str = "John Doe"
#     signup_ts: datetime | None = None
#     friend_ids: List[int] | None = None
#     password: str


class SafeUser(BaseModel):
    id: int
    name: str = "John Doe"
    friend_ids: list[int] | None = None


class User(
    SafeUser
):  # Second version (same result as first, but prevents initializing the same attributes multiple times)
    signup_ts: datetime | None = None
    password: str


@app.post("/user")
async def read_user(user: User) -> User:
    return user


@app.post("/failing_user")
async def read_user(user: User) -> User:
    # the program generates invalid data, i.e. missing a password
    return {"id": user.id, "name": "John Doe"}


@app.post("/safe_user")
async def read_user(user: User) -> SafeUser:
    return user
