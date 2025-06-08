
# FastAPI core module for building APIs
from fastapi import FastAPI, Response, status, HTTPException, Request, Body, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List
from sqlalchemy import func
# Local application imports (models and schemas for database and request/response validation)
from .. import models, schemas, utils, oauth2
from fastapi.responses import HTMLResponse


router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)



# @router.get("/",response_model= List[schemas.MovieO] )
# def get_posts(db : Session = Depends(get_db)):
    
#     movies = db.query(models.MovieSuggest).all()
#     results = db.query(models.MovieSuggest, func.count(models.Credit.movie_id).label("credit")) \
#                 .join(models.Credit, models.Credit.movie_id == models.MovieSuggest.id, isouter=True) \
#                 .group_by(models.MovieSuggest.id) \
#                 .all()
#     print(results)

#     return results

@router.get("", response_model=List[schemas.Movie])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
#the current_user: int = Depends(oauth2.get_current_user) makes sure the user needs to be logged in to perform this action
    # Query movie suggestions and count how many credits each has
    results = db.query(models.MovieSuggest, func.count(models.Credit.movie_id).label("credit")) \
        .join(models.Credit, models.Credit.movie_id == models.MovieSuggest.id, isouter=True) \
        .group_by(models.MovieSuggest.id) \
        .all()

    movies_with_credits = []

    for movie, credit in results:
        # suggested_times = db.query(func.count(models.MovieSuggest.id)) \
        #                     .filter(models.MovieSuggest.name == movie.name) \
        #                     .scalar()
        
        user_has_credited = db.query(models.Credit).filter(
            models.Credit.movie_id == movie.id,
            models.Credit.username == current_user.username
        ).count() > 0

        movies_with_credits.append(
            schemas.Movie(
                id=movie.id,
                name=movie.name,
                ott=movie.ott,
                description=movie.description,
                suggested_by=movie.suggested_by,
                owner=schemas.User(id=movie.owner.id, username=movie.owner.username) if movie.owner else None,
                # suggested_times=suggested_times,
                credit=credit,
                user_has_credited=user_has_credited
            )
        )

    return movies_with_credits




@router.get("/{id}", response_model=schemas.MovieOut)  # Use a single MovieOut schema
def get_movie(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Query movie suggestions and join with the Credit table
    result = db.query(models.MovieSuggest, func.count(models.Credit.movie_id).label("credit")) \
        .join(models.Credit, models.Credit.movie_id == models.MovieSuggest.id, isouter=True) \
        .group_by(models.MovieSuggest.id) \
        .filter(models.MovieSuggest.id == id) \
        .first()  # Use .first() to get a single movie

    if not result:
        raise HTTPException(status_code=404, detail="Movie not found")
    

    movie, credit = result
    movie_with_credits = schemas.MovieOut(
        id=movie.id,
        name=movie.name,
        ott=movie.ott,
        description=movie.description,
        suggested_times= db.query(func.count(models.MovieSuggest.id)) \
                            .filter(models.MovieSuggest.name == movie.name) \
                            .scalar(),
        suggested_by=movie.suggested_by,
        credit=credit
    )

    return movie_with_credits


@router.get("/1/my_movies", response_model=List[schemas.MyMovies])
def get_my_suggetions(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Query movies suggested by the current user
    results = db.query(models.MovieSuggest, func.count(models.Credit.movie_id).label("credit")) \
        .join(models.Credit, models.Credit.movie_id == models.MovieSuggest.id, isouter=True) \
        .group_by(models.MovieSuggest.id) \
        .filter(models.MovieSuggest.suggested_by == current_user.username)

    # Return the movie data
    movies_with_credits = [
        schemas.MyMovies(
            id=movie.id,
            name=movie.name,
            ott=movie.ott,
            suggested_times= db.query(func.count(models.MovieSuggest.id)) \
                            .filter(models.MovieSuggest.name == movie.name) \
                            .scalar(),
            description=movie.description,
            credit=credit
        )
        for movie, credit in results
    ]

    return movies_with_credits
    

#Post new suggtion
@router.post("",status_code=status.HTTP_201_CREATED, response_model= schemas.MoviePost)
def post_new(movie : schemas.MovieCreate,db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user) ):
    
    print(current_user.username)
    new_movie = models.MovieSuggest(suggested_by=current_user.username,**movie.dict())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    
    
    return new_movie


#Go to localhost:8000/docs for interactive docs
#Run after creating a venv, insatlling reqirements - fastapi dev main.py [make sure ur in correct directory]

#get with movie id



@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model= schemas.MoviePut)
def put_movie(id : int,edit_movie : schemas.MovieEdit, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user )):
    movie_query = db.query(models.MovieSuggest).filter(models.MovieSuggest.id == id)
    movie = movie_query.first()

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Movie with id: {id} was not found")

    if movie.suggested_by != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    
    movie_query.update(edit_movie.dict(), synchronize_session= False)
    db.commit()
                
    return movie_query.first()


#Delete with ID
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_movie(id : int, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    movie_query =  db.query(models.MovieSuggest).filter(models.MovieSuggest.id == id)
    movie = movie_query.first()

    #print(movie.suggested_by)
    #print(current_user.username)

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Movie with id: {id} was not found")
    if movie.suggested_by != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db.delete(movie)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

#8:32