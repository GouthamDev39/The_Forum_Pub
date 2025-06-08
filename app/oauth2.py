
#Create token
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from datetime import datetime, timedelta
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings
from fastapi import Request


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')



SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES


def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id : str = payload.get("user_id", "username")

        if user_id is None:
            raise credentials_exception

        return schemas.TokenData(id=user_id)

    except ExpiredSignatureError:
        raise credentials_exception
    except InvalidTokenError:
        raise credentials_exception



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
 
    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user

# def get_current_user(
#     request: Request,
#     db: Session = Depends(database.get_db),
#     token: str = Depends(oauth2_scheme)  # default fallback
# ):
#     # Try cookie first
#     token = request.cookies.get("access_token") or token

#     credentials_exception = HTTPException(
#         status_code=401,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )

#     token_data = verify_access_token(token, credentials_exception)
#     user = db.query(models.User).filter(models.User.id == token_data.id).first()

#     return user
