from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
from crud import BasicInfo, TestReview, get_course_teacher, create_class_in_db, enroll_class_in_db

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
def get_history_classes(stundentID: int, classID: int, db: Session = Depends(get_db)):
    return TestReview(db, classID, studentID)

@app.get("/getcoursebyteacher")
def get_course_by_teacher(email: str, db: Session = Depends(get_db)):
    return get_course_teacher(db, email)

@app.get("/createclass")
def create_class(email: str, course: str, db: Session = Depends(get_db)):
    return create_class_in_db(db, email, course)

@app.get("/enrollclass")
def enroll_class(studntID: int, classID: str, db: Session = Depends(get_db)):
    return enroll_class_in_db(db, studntID, classID)

@app.post("/inserttext")
def insert_text(classid: int, text: str):
    # procressing main
    return "OK"
