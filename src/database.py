from models import UserInDB


def get_user(db: dict, username: str) -> UserInDB | None:
    return UserInDB(**db[username]) if username in db else None


fake_db = {
    "johndoe": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}
