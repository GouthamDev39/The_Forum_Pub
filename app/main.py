
#from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Request, Depends
#from fastapi import Body, Depends
from fastapi.responses import JSONResponse
#from pydantic import BaseModel
from contextlib import asynccontextmanager
from .routers import movies, users, auth, credit, ui
from sqlalchemy.orm import Session
from . import schemas, models, utils
from .oauth2 import get_current_user
from .database import get_db
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates#front end
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi_tailwind import tailwind
from pathlib import Path
#from .config import settings
     


#models.Base.metadata.create_all(bind=engine)

static_files = StaticFiles(directory="static")

@asynccontextmanager
async def lifespan(app: FastAPI):
    process = tailwind.compile(static_files.directory + "/css/styles.css")
    try:
        yield
    finally:
        process.terminate()

app = FastAPI(lifespan = lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from the 'static' directory
app.mount("/static", static_files, name="static")

# Setup Jinja2 templates for rendering HTML files
templates = Jinja2Templates(directory="templates")



# This line tells SQLAlchemy to create all database tables based on the models defined with Base
# It uses the engine (database connection) to issue CREATE TABLE statements if tables don't exist



#root site
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/update", response_class=HTMLResponse)
async def update_content(request: Request):
    return templates.TemplateResponse("partial.html", {"request": request, "content": "Hello Batman"})


app.include_router(movies.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(credit.router)
app.include_router(ui.router)


# #Front End-UI
# @app.get("/movies-ui", response_class=HTMLResponse)
# def movies_ui():
#     return Path("templates/movies.html").read_text()

@app.get("/movies-ui", response_class=HTMLResponse)
def movies_ui(request: Request):
    return templates.TemplateResponse("movies.html", {"request": request})


@app.get("/my-page", response_class=HTMLResponse)
def movies_ui(request: Request):
    return templates.TemplateResponse("my-page.html", {"request": request})
    # return Path("templates/my-page.html").read_text()


@app.get("/homepage", response_class=HTMLResponse)
def movies_ui():
    return Path("templates/homepage.html").read_text()
    

@app.get("/movie-create-ui", response_class=HTMLResponse)
def movies_ui(request: Request):
    return templates.TemplateResponse("movie-create.html", {"request": request})

# @app.get("/movies-id-ui", response_class=HTMLResponse)
# def movies_ui():
#     return Path("templates/movie-detail.html").read_text()

@app.get("/movies-id-ui", response_class=HTMLResponse)
def movie_ui(request: Request):
    return templates.TemplateResponse("movie-detail.html", {"request": request})

# @app.get("/user-id-ui", response_class=HTMLResponse)
# def movies_ui():
#     return Path("templates/user-detail.html").read_text()


@app.get("/user-id-ui", response_class=HTMLResponse)
def user_detail_ui(request: Request):
    return templates.TemplateResponse("user-detail.html", {"request": request})

@app.get("/register-ui",response_class=HTMLResponse)
def register_ui():
    return Path("templates/register.html").read_text()

@app.get("/login-ui", response_class=HTMLResponse)
def login_ui():
    return Path("templates/login.html").read_text()



