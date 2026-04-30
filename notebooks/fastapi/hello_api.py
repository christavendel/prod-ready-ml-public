from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def hello():
    return "Hello, world!"


@app.get("/greet/{name}")
def greet(name: str):
    return f"Hello, {name}!"


@app.get("/greet_int")
def greet_int(num: int | str | None = 0):
    return f"Hello, number {num}!"
