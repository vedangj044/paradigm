from typing import List
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine
import crud
from ml import mls

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
    return crud.BasicInfo(db, studntID).get_response_basic()

@app.get("/testreview")
def get_history_classes(stundentID: int, classID: int, db: Session = Depends(get_db)):
    return crud.TestReview(db, classID, stundentID).get_test_review()

@app.get("/getcoursebyteacher")
def get_course_by_teacher(email: str, db: Session = Depends(get_db)):
    return crud.get_course_teacher(db, email)

@app.get("/createclass")
def create_class(email: str, course: str, db: Session = Depends(get_db)):
    return crud.create_class_in_db(db, email, course)

@app.get("/enrollclass")
def enroll_class(studntID: int, classID: str, db: Session = Depends(get_db)):
    return crud.enroll_class_in_db(db, studntID, classID)

@app.post("/inserttext")
def insert_text(classid: int, text: str, db: Session = Depends(get_db)):
    crud.insert_question(mls(text).getResponse())
    return "OK"

@app.get("/getquestion")
def get_last_question(classID: int, studentID: int, db: Session = Depends(get_db)):
    return crud.QuestionTest(db, classID, studentID).get_question_unasked()

@app.get("/submitresponse")
def submit_responsee(questionID: int, studentID: int, valid: bool, db: Session = Depends(get_db)):
    return crud.submit_response(db, studentID, questionID, valid)

@app.get("/getteacherinfo")
def get_teacher_info(teacherID: int, db: Session = Depends(get_db)):
    return crus.get_teacher_info(db, teacherID)
