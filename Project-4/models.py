from base import Base
from sqlalchemy import Column,String,Integer
class User(Base):
    __tablename__="busers"
    name = Column(String)
    id = Column(String,primary_key=True)
    email = Column(String)
    age = Column(Integer)

    
class Blog(Base):
    __tablename__="blogs"
    title = Column(String)
    author = Column(String)
    post = Column(String)
    tags = Column(String)
    id = Column(String,primary_key=True)