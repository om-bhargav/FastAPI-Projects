from fastapi import FastAPI
from user_routes import router as uroutes
from blog_routes import router as broutes
from base import Base

app = FastAPI()

app.include_router(uroutes)
app.include_router(broutes)