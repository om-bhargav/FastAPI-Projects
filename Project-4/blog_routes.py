from fastapi import APIRouter, Request
from pydantic import BaseModel
from sessions import Session
import uuid
from models import User,Blog
from typing import Optional

router=APIRouter(
    prefix="/blogs",
    tags=["blogs"]
)

class BlogTemplate(BaseModel):
    title: str
    author: str 
    post: str
    tags: str

class UpdateBlog(BaseModel):
    title: Optional[str] = None 
    post: Optional[str] = None
    tags: Optional[str] = None

session = Session()

@router.get("/")
def users(request: Request):
    blogs = session.query(Blog).all()
    return [item.__dict__ for item in blogs]

@router.post("/create")
def create_blog(request: Request, body: BlogTemplate):
    user = session.query(User).filter_by(id=body.author).first()
    if(user):
        session.add(Blog(**{**body.__dict__,"id":str(uuid.uuid4())}))
        session.commit()
    return {}

@router.delete("/delete")
def delete_user(request: Request,u_id: str):
    blog = session.query(Blog).filter_by(id=u_id).first()
    if blog:
        session.delete(blog)
        session.commit()
    return {}

@router.put("/update")
def update_user(request: Request,u_id: str,body: UpdateBlog):
    blog = session.query(Blog).filter_by(id=u_id).first()
    if blog:
        if(body.title):
            blog.title=body.title
        elif(body.post):
            blog.post=body.post
        elif(body.tags):
            blog.tags=body.tags
    session.commit()
    return {}
