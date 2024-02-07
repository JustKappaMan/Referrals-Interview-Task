import os
import sys

from dotenv import load_dotenv


# Load environment variables from 'src/.env' file
load_dotenv()

# The key to use for signing the JWK claim set
if (SECRET_KEY := os.getenv("SECRET_KEY")) is None:
    sys.exit(
        "Error! 'SECRET_KEY' environment variable not set.\n"
        "Create .env file in 'src' folder and add 'SECRET_KEY' variable into it."
    )

# For how long user's access token lasts (in minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 30
