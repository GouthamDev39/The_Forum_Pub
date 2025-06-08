from fastapi import FastAPI, Response, status, HTTPException, Request, Body, Depends, APIRouter
from sqlalchemy.orm import Session
# Local application imports (models and schemas for database and request/response validation)
from .. import models, schemas, utils, oauth2
from ..database import get_db




router = APIRouter(
    prefix="/credit",
    tags=["Credit"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def credit(credit: schemas.Credit, db : Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    movie = db.query(models.MovieSuggest).filter(models.MovieSuggest.id == credit.movie_id).first()

    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Movie with id: {credit.movie_id} was not found")


    credit_query = db.query(models.Credit).filter(models.Credit.movie_id == credit.movie_id, models.Credit.username == current_user.username)
    found_credit = credit_query.first()
    if (credit.dir == 1):
        if found_credit:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.username} has already voted")
        
        new_credit = models.Credit(movie_id=credit.movie_id,username=current_user.username )
        db.add(new_credit)
        db.commit()
        return {f"Credit made"}
    else:
        if not found_credit:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No credits made")
        credit_query.delete(synchronize_session=False)
        db.commit()

        return(f"Credit revoked")