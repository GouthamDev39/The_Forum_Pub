
# FastAPI core module for building APIs
from fastapi import FastAPI, Response, status, HTTPException, Request, Body, Depends, APIRouter
from sqlalchemy.orm import Session
# Local application imports (models and schemas for database and request/response validation)
from .. import models, schemas, utils, oauth2
from ..database import get_db
from fastapi.responses import HTMLResponse
from fastapi import Form

router = APIRouter(tags=["UI"])





@router.post("/register-ui", response_class=HTMLResponse)
def create_user_from_form(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    if db.query(models.User).filter(models.User.username == username).first():
        return HTMLResponse(
            content=f"<p class='text-red-500'>❌ Username <strong>{username}</strong> is already taken.</p>",
            status_code=200
        )

    hashed_password = utils.hash(password)
    new_user = models.User(username=username, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return HTMLResponse(
    content="""
    <p class='text-green-400'>✅ User created successfully!</p>
    <script>
      document.querySelector("form").reset();
    </script>

    <a href="/login-ui" class="inline-block bg-cyan-500 hover:bg-cyan-600 text-white font-semibold px-6 py-3 rounded transition">
        Login
    </a>
       """,
    status_code=201
)



