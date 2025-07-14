from fastapi import FastAPI
from sqlalchemy import create_engine,Column,String,Integer
from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Optional
import uuid
def response_message(message):
    return {"Message":message}
app=FastAPI()
class BookItem(BaseModel):
    author_name: str
    book_text: str
    pages: str
class UpdateBookItem(BaseModel):
    author_name: Optional[str] = None
    book_text: Optional[str] = None
    pages: Optional[str] = None

engine=create_engine("sqlite:///database.db")

Base = declarative_base()

class Book(Base):
    __tablename__='books'
    id=Column(String,primary_key=True)
    author_name=Column(String)
    book_text=Column(String)
    pages=Column(Integer)

Base.metadata.create_all(engine)

Session=sessionmaker(bind=engine)
session=Session()


@app.get("/")
def list_books():
    items_dict={}
    items=session.query(Book).all()
    for item in items:
        items_dict[item.id]={"author_name":item.author_name,"book_text":item.book_text,"pages":item.pages}
    return items_dict

@app.post("/create")
def create_book(body: BookItem):
    book=Book(id=str(uuid.uuid4()),author_name=body.author_name,book_text=body.book_text,pages=body.pages)
    session.add(book)
    session.commit()
    return response_message("Book Created!")

@app.get("/get/{item_id}")
def getbookbyId(item_id):
    item=session.query(Book).filter_by(id=item_id).first()
    if(item):
        res=item.__dict__.copy()
        del res["_sa_instance_state"]
        return res
    return response_message("Item not Exists!")

@app.put("/update/{item_id}")
def update_book(item_id,body: UpdateBookItem):
    item=session.query(Book).filter_by(id=item_id).first()
    if(item):

        if(body.author_name):
            session.merge(Book(id=item_id,author_name=body.author_name))

        if(body.book_text):
            session.merge(Book(id=item_id,book_text=body.book_text))
        
        if(body.pages):
            session.merge(Book(id=item_id,pages=body.pages))

    session.commit()

    return response_message("Book Updated!")

@app.delete("/delete/{item_id}")
def delete_book(item_id: str):
    book=session.query(Book).filter_by(id=item_id).first()
    if(book):
        session.delete(book)
        session.commit()
    return response_message("Book Deleted!")

@app.post("/search")
def search_book(body: UpdateBookItem):
    items_list=[]
    items=session.query(Book).all()
    for item in items:
        if((body.author_name!=None and body.author_name in item.author_name) or (body.book_text!=None and body.book_text in item.book_text) or (body.pages!=None and body.pages in item.pages)):
            items_list.append({"id":item.id,"author_name":item.author_name,"book text":item.book_text,"pages":item.pages})

    return items_list


