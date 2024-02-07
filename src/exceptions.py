from fastapi import HTTPException, status


__all__ = [
    "CredentialsException",
    "UnregisteredUserException",
    "InvalidPasswordException",
    "InactiveUserException"
]

# Raised when something is wrong with JWT token
CredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Couldn't validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

# Raised when unregistered user is trying to sign in
UnregisteredUserException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Unregistered user",
    headers={"WWW-Authenticate": "Bearer"},
)

# Raised when registered user is trying to sign in with invalid password
InvalidPasswordException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid password",
    headers={"WWW-Authenticate": "Bearer"},
)

# Raised when user session is inactive
InactiveUserException = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Inactive user",
    headers={"WWW-Authenticate": "Bearer"},
)
