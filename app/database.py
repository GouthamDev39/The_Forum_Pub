#Databse stuffs
"""What is SQL alchemy -> It is an Object Relational Mapper (ORM) that 
allows developers to interact with databases in a more Pythonic and abstract way, without writing raw SQL for every query.

cursor.execute( INSERT INTO products (name,price,is_sale,inventory) VALUES (%s,%s,%s,%s) RETURNING * ,(products.name,
             products.price,products.is_sale,products.inventory))
The above line is same as below command frommain.py

new_movie = models.MovieSuggest(**movie.dict())
    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)
    
    return new_movie

With sqlaclhcemy we use python keys than using directquerying, this is best practice no negate SQL injection

"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg as db
from psycopg.rows import dict_row
from .config import settings

import time


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@ipaddress:port/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit = False, autoflush= False, bind= engine)

Base = declarative_base()#we usethis class to inherit to create each db models 

def get_db():#dependency
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



# while True:#Connect to DB
#     try:
#         conn = db.connect(host='localhost', dbname ='forum_app', user='batman',
#                                 password='pswd', row_factory = dict_row)
#         cursor = conn.cursor()
#         print("Databse connection succesful")
#         break

#     except Exception as error:
#         print("Connection Failed")
#         print("Error was", error)
#         time.sleep(3)