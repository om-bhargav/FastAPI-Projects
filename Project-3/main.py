from fastapi import FastAPI
from sqlalchemy import create_engine,Column,Integer,String,Boolean,update
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
from typing import Optional
Base=declarative_base()

class UserTemplate(BaseModel):
    name: str
    email: str
    password: str
    age: int
    martial_status: bool

class UpdateUser(BaseModel):
    name: Optional[str]=None
    password: Optional[str]=None
    age: Optional[int]=None
    martial_status: Optional[bool]=None

class User(Base):
    __tablename__="users"
    name=Column(String)
    email=Column(String,primary_key=True)
    password=Column(String)
    age=Column(Integer)
    martial_status=Column(Boolean)

engine=create_engine("sqlite:///database.db")

Base.metadata.create_all(engine)

app=FastAPI()

Session=sessionmaker(bind=engine)
session=Session()


@app.get("/")
def getUsers():
    items=session.query(User).all()
    items_list=[]
    for item in items:
        items_list.append(item.__dict__)
    return items_list

@app.post("/create")
def createUser(body: UserTemplate):
    user=session.query(User).filter_by(email=body.email).first()
    if(not user):
        session.add(User(**body.__dict__))
        session.commit()
    return {}

@app.put("/update/{email_id}")
def updateUser(email_id: str,body: UpdateUser):
    user=session.query(User).filter_by(email=email_id).first()
    # update(User).where(User.email==email_id).values(**{key:body.__dict__[key] for key in body.__dict__ if body.__dict__[key]!=None})
    if(body.age!=None):
        user.age=body.age
    
    if(body.name!=None):
        user.name=body.name
    
    if(body.password!=None):
        user.password=body.password
    
    if(body.martial_status!=None):
        user.martial_status=body.martial_status
    
    session.commit()
    return {}

@app.delete("/delete/{email_id}")
def deleteUser(email_id: str):
    user=session.query(User).filter_by(email=email_id).first()
    if(user):
        session.delete(user)
        session.commit()    
    return {}

@app.post("/change")
def changePassword(email_id: str,password: str):
    user=session.query(User).filter_by(email=email_id).first()
    if user:
        user.password=password
    return {}

@app.post("/search")
def searchUsers(name: Optional[str]=None,age: Optional[int]=None,martial_status: Optional[bool]=None):
    items_res=[]
    items=session.query(User).all()
    print(name,age,martial_status)
    for item in items:
        if(name and name.lower() in item.name.lower()):
            items_res.append(item.__dict__)
        elif(age and age==item.age):
            items_res.append(item.__dict__)
        elif(martial_status and martial_status == item.martial_status):
            items_res.append(item.__dict__)
    return items_res

