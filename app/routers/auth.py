from fastapi import APIRouter,Depends, status, HTTPException, Response
from fastapi.security import  OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .. import schemas, models, utils, database, oauth2

router = APIRouter(tags=["Authentication"])



@router.post("/login", response_model=schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(),db : Session = Depends(database.get_db)):
   
    user = db.query(models.User).filter(models.User.username == user_credentials.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    #Since the passwords are hased and stored need to compare the hased password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data = {"user_id":user.id})


    return {"token_type": "Bearer", "access_token": access_token, "user": user.username}


#from fastapi import Response

# @router.post("/login")
# def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
#     # Validate user (check username & password)
#     user = db.query(models.User).filter(models.User.username == user_credentials.username).first()
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
    
#     access_token = oauth2.create_access_token(data={"user_id": user.id})

#     response = Response(content={"message": "Login successful"})
    
#     # Set cookie
#     response.set_cookie(
#         key="access_token",
#         value=access_token,
#         httponly=True,
#         secure=False,  # set to True in production with HTTPS
#         samesite="lax",  # or "strict"
#         max_age=3600,  # expires in 1 hour
#         path="/"
#     )

#     return response




""" 

  "username": "batman",
  "password": "batman123"

"""

