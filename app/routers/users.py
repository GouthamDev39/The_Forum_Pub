# FastAPI core module for building APIs
from fastapi import FastAPI, Response, status, HTTPException, Request, Body, Depends, APIRouter
from sqlalchemy.orm import Session
# Local application imports (models and schemas for database and request/response validation)
from .. import models, schemas, utils, oauth2
from ..database import get_db




router = APIRouter(
    prefix="/users",
    tags=["Users"]
)



@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user : schemas.UserCreate, db : Session = Depends(get_db)):
    
    #Hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    
    #movie_query =  db.query(models.MovieSuggest).filter(models.MovieSuggest.id == id)
    user_query = db.query(models.User).filter(models.User.username == new_user.username).first()


    if user_query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Username {new_user.username} already taken. Try something else")

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/{id}",response_model=schemas.UserDetails)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id} was not found"
        )

    # Fetch suggested movies (e.g. movie names)
    suggested_movies = db.query(models.MovieSuggest).filter(
        models.MovieSuggest.suggested_by == user.username
    ).all()

    movie_names = [movie.name for movie in suggested_movies]
    movie_id = [movie.id for movie in suggested_movies]

    #print(movie_names,movie_id)

    return {
        "id": user.id,
        "username": user.username,
        "suggested_movies": movie_names,
        "movie_id":movie_id
    }


@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def edit_user(id: int, edit_user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id)
    user = user_query.first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id: {id} was not found")

    # Hash the new password before updating
    hashed_password = utils.hash(edit_user.password)
    edit_user.password = hashed_password

    user_query.update(edit_user.dict(), synchronize_session=False)
    db.commit()

    return user_query.first()


#7:24