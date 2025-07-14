from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
from sqlalchemy.orm import sessionmaker
from pydantic import BaseModel
import uuid
### This project is uses database.db file to store data and performs CRUD operations.

class ItemType(BaseModel):
      task_name: str

app=FastAPI()
engine=create_engine("sqlite:///database.db")
Base=declarative_base()

class Item(Base):
      __tablename__='items'
      id=Column(String,primary_key=True)
      task_name=Column(String)

Base.metadata.create_all(engine)

Session=sessionmaker(bind=engine)
session=Session()

@app.get("/")
async def read_items():
      items=session.query(Item).all()
      items_dict={}
      for item in items:
          items_dict[item.id]=item.task_name
      return items_dict

@app.post("/create/")
async def create_item(body: ItemType):
      id=str(uuid.uuid4())
      exists=session.query(Item).filter_by(id=id).first()
      if exists:
            return {"message":"Item Already Exists!"}
      item=Item(id=id,task_name=body.task_name)
      session.add(item)
      session.commit()
      return {"message":"Item Created!"}

@app.patch("/update/{item_id}")
async def update_item(item_id: str,body: ItemType):
      session.merge(Item(id=item_id,task_name=body.task_name))
      session.commit()
      return {"message":"Item Updated!"}

@app.delete("/items/{item_id}")
async def delete_item(item_id):
      item=session.query(Item).filter_by(id=item_id).first()
      if item:
            session.delete(item)
            session.commit()
      return {"message":"Item Deleted!"}
