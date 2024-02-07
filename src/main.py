from fastapi import FastAPI


app = FastAPI()


@app.get("/")
async def root() -> str:
    return "You're on the index page!"
