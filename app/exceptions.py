from fastapi import HTTPException
from fastapi import status

INVALID_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Incorrect username or password",
    headers={"WWW-Authenticate": "Bearer"},
)

INACTIVE_USER_EXCEPTION = HTTPException(status_code=400, detail="Inactive user")
