from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from crud import BasicInfo, TestReview

app = FastAPI()

def get_db():
    engine = create_engine('mysql+pymysql://vedangj:password@localhost/paradigm')
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()

@app.get("/basicinfo")
def get_basic_info(studntID: int, db: Session = Depends(get_db)):
    return BasicInfo(db, studntID).get_response_basic()

@app.get("/testreview")
def get_history_classes(stundentID: int, classID: int, db: Session = Depends(get_db))
    return TestReview(db, classID, studentID)
