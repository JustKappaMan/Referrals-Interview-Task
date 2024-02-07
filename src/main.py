from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import OAuth2PasswordRequestForm

from database import fake_db
from models import Token, User
from auth import create_access_token, authenticate_user, get_current_active_user


app = FastAPI()


@app.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = authenticate_user(fake_db, form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_my_profile(current_user: Annotated[User, Depends(get_current_active_user)]) -> User:
    return current_user


@app.get("/users/me/items/")
async def read_my_items(current_user: Annotated[User, Depends(get_current_active_user)]) -> list[dict]:
    return [
        {"item_id": "foo", "owner": current_user.username},
        {"item_id": "bar", "owner": current_user.username},
        {"item_id": "...", "owner": current_user.username},
        {"item_id": "baz", "owner": current_user.username},
    ]
