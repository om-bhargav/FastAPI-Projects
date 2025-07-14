from fastapi import APIRouter,Request
from pydantic import BaseModel
from sessions import Session
from typing import Optional
import uuid
from models import User
router = APIRouter(
    prefix="/users",
    tags=["users"]
)

class UserTemplate(BaseModel):
    name: str
    email: str
    age: int

class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None



session = Session()

@router.get("/")
def users(request: Request):
    return [item.__dict__ for item in session.query(User).all()]

@router.post("/create")
def create_user(request: Request, body: UserTemplate):
    session.add(User(**{**body.__dict__,"id":str(uuid.uuid4())}))
    session.commit()
    return {}

@router.delete("/delete")
def delete_user(request: Request, u_id: str):
    user = session.query(User).filter_by(id=u_id).first()
    if(user):
        session.delete(user)
        session.commit()
    return {}

@router.put("/update")
def update_user(request: Request,u_id: str,body: UpdateUser):
    user = session.query(User).filter_by(id=u_id).first()
    if(user):
        if(body.age):
            user.age=body.age
        elif(body.name):
            user.name=body.name
        elif(body.email):
            user.email=body.email
    session.commit()
    return {}


