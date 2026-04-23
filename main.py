from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from app.database.database import get_db, engine
from app.models import models
from app.routers import notes

# create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow React frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include routes
app.include_router(notes.router)


# root
@app.get("/")
def read_root():
    return {"message": "Knowledge Graph API is running"}


# DB test
@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"message": "DB Connected Successfully"}
