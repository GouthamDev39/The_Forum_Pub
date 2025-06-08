#Pydantic model
#Pydantic is the most widely used data validation library for Python.
#https://docs.pydantic.dev/latest/
#data validation is nothing but making sure the input from user is correct [i.e gives string for name, number for age, etc]
from pydantic import BaseModel, Field#For schema
from datetime import datetime
from typing import Optional, List
from pydantic.types import conint


class UserCreate(BaseModel):
    username : str
    password : str 

class User(BaseModel):
    id : int
    username: str
    class Config:
        from_attributes = True


class UserDetails(User):
    suggested_movies : List[str]
    movie_id : List[int]

class MovieBase(BaseModel):
    name : str
    ott : str
    description : str = Field(min_length=10)
    suggested_by: str
    

class MovieCreate(BaseModel):
    name : str
    ott : str
    description : str = Field(min_length=10)
    

class MovieEdit(BaseModel):
    ott : str
    description : str = Field(min_length=10)


class Movie(BaseModel):
    id: int
    name: str
    ott: str
    description: str
    suggested_by: str
    #suggested_times : int
    owner: User
    credit : int
    user_has_credited: bool

    class Config:
        from_attributes = True


class MoviePost(BaseModel):
    id: int
    name: str
    ott: str
    description: str
    suggested_by: str

class MoviePut(BaseModel):
    name: str
    ott: str
    description : str

    class Config:
        from_attributes = True



class MyMovies(BaseModel):
    id: int
    name: str
    ott: str
    description: str
    suggested_times : int
    #suggested_by: str
    #owner: User
    credit : int
    #user_has_credited: bool

    class Config:
        from_attributes = True


class MovieID(MyMovies):
    pass
    

class MovieOut(MyMovies):
    suggested_by : str



""" class Login(BaseModel):
    username : str
    password : str
     """

class Token(BaseModel):
    access_token: str
    token_type : str
    user : str

class TokenData(BaseModel):
    id: Optional[int]


class Credit(BaseModel):
    movie_id : int
    dir: conint(le=1)

