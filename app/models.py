#SQL alchemy models 
#Models are lik defining a new table, create them with class

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
from .database import Base

class MovieSuggest(Base):
    __tablename__ = "movie_suggest"

    id = Column(Integer, nullable= False,primary_key = True)
    name = Column(String, nullable= False)
    ott = Column(String, nullable= False)
    description = Column(String, nullable= False)
    suggested_by = Column(String, ForeignKey("users.username", ondelete="CASCADE"), nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))
    #credits = relationship()
    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable= False,primary_key = True)
    username = Column(String, nullable = False, unique = True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))


class Credit(Base):
    __tablename__ = "credit"

    username = Column(String, ForeignKey("users.username",ondelete="CASCADE"), primary_key=True)
    movie_id = Column(Integer, ForeignKey("movie_suggest.id", ondelete="CASCADE"), primary_key=True)