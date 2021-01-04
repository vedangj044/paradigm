from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine, func
import models
import datetime
import random


class BasicInfo():

    def __init__(self, db: Session, user_id: int):
        self.userId = user_id
        self.db = db

    def get_profile_picture(self):
        return self.db.query(models.Student).filter(models.Student.studentID == self.userId).first().__dict__

    def get_active_classes(self):
        self.active_classes = self.db.query(models.CourseStudent, models.Clas).filter(models.CourseStudent.studentID == self.userId).filter(models.Clas.courseID == models.CourseStudent.courseID).filter(models.Clas.active == 1).all()

        responseList = []
        for i in self.active_classes:
            response = {}
            response["class_id"] = i[1].classID
            response["course_name"] = self.db.query(models.Course).filter(models.Course.courseID == i[0].courseID).first().courseName
            response["participants"] = len(self.db.query(models.Enroll).filter(models.Enroll.classID == i[1].classID).all())
            response["isEnrolled"] = len(self.db.query(models.Enroll).filter(models.Enroll.studentID == self.userId).filter(models.Enroll.classID == i[1].classID).all()) != 0
            responseList.append(response)

        return responseList

    def get_history_classes(self):

        self.history_classes = self.db.query(models.Enroll).filter(models.Enroll.studentID == self.userId).all()

        historyResponseList = []
        _taken_Class = []

        kld = []

        for i in self.history_classes:
            _tk_class = self.db.query(models.Clas).filter(models.Clas.classID == i.classID).first()

            if _tk_class.active == 1:
                continue

            _tk_score = self.db.query(models.Score).filter(models.Score.classID == _tk_class.classID).filter(models.Score.studentID == self.userId).first()

            kld.append((i, _tk_score, _tk_class))


        for i in kld:
            hresponse = {}
            hresponse["classID"] = i[2].classID
            hresponse["course_name"] = self.db.query(models.Course).filter(models.Course.courseID == i[2].courseID).first().courseName
            hresponse["date"] = i[2].date
            hresponse["rank"] = i[1].rank
            hresponse["score"] = str(i[1].totalScore) + "/" + str(len(self.db.query(models.Question).filter(models.Question.classID == i[2].classID).all()))

            historyResponseList.append(hresponse)
            if hresponse["classID"] not in _taken_Class:

                _taken_Class.append(hresponse["classID"])

        return historyResponseList

    def get_response_basic(self):

        resp = {}
        resp["profile"] = self.get_profile_picture()
        resp["history"] = self.get_history_classes()
        resp["active"] = self.get_active_classes()
        resp["profile"].pop('_sa_instance_state', None)

        return resp


class TestReview():

    def __init__(self, session, classID, studentID):
        self.db = session
        self.classID = classID
        self.userId = studentID

    def get_test_review(self):

        questionList = []
        for i in self.db.query(models.Question).filter(models.Question.classID == self.classID).all():
            resp = {}
            resp["questionText"] = i.text
            if i.questionTypeID == 1:
                resp["option"] = i.option.split("@")
                resp["correctOption"] = i.correctOption
                resp["correctTF"] = 0
            else:
                resp["correctTF"] = i.correctTF
                resp["option"] = []
                resp["correctOption"] = 0
            resp["questionType"] = i.questionTypeID
            resp["response"] = self.db.query(models.Response).filter(models.Response.questionID == i.questionID).filter(models.Response.studentID == self.userId).first().valid

            questionList.append(resp)

        respList = {}

        clasObj = self.db.query(models.Clas).filter(models.Clas.classID == self.classID).first()
        respList["date"] = str(clasObj.date)
        respList["course_name"] = self.db.query(models.Course).filter(models.Course.courseID == clasObj.courseID).first().courseName
        scoreObj = self.db.query(models.Score).filter(models.Score.classID == self.classID).filter(models.Score.studentID == self.userId).first()
        respList["score"] = scoreObj.totalScore
        respList["rank"] = scoreObj.rank
        respList["questionList"] = questionList

        return respList

class QuestionTest():

    def __init__(self, session, classID, studentID):
        self.db = session
        self.classID = classID
        self.studentID = studentID

    def get_question_unasked(self):

        ques = self.db.query(models.Question).filter(models.Question.classID == self.classID).all()
        asl = self.db.query(models.QuestionAsked).filter(models.QuestionAsked.studentID == self.studentID).all()

        respObj = {}

        _ask = []
        for i in asl:
            _ask.append(i.questionID)

        respObj["blank"] = {}
        respObj["bool"] = {}

        for i in ques:
            if i.questionID not in _ask:
                if i.questionTypeID == 1:
                    opt = i.option.split("@")
                    respObj["blank"]["id"] = i.questionID
                    respObj["blank"]["blank"] = i.text
                    respObj["blank"]["answer"] = i.correctOption + 1
                    respObj["blank"]["option1"] = opt[0]
                    respObj["blank"]["option2"] = opt[1]
                    respObj["blank"]["option3"] = opt[2]
                else:
                    fg = True
                    if i.correctTF == 0:
                        fg = False
                    respObj["bool"]["id"] = i.questionID
                    respObj["bool"]["answer"] = fg
                    respObj["bool"]["bool"] = i.text

                id = "{0}_{1}".format(i.questionID, self.studentID)
                self.db.add(models.QuestionAsked(questionAsked=id, studentID=self.studentID, questionID=i.questionID))
                self.db.commit()

        return respObj

def get_course_teacher(session, email):
    course = session.query(models.CourseTeacher, models.Teacher).filter(models.Teacher.teacherEmail == email).filter(models.CourseTeacher.teacherID == models.Teacher.teacherID).all()

    resp = []
    for i in course:
        resp.append(session.query(models.Course).filter(models.Course.courseID == i[0].courseID).first().courseName)

    return {"course": set(resp)}

def create_class_in_db(session, email, course):
    teacherID = session.query(models.Teacher).filter(models.Teacher.teacherEmail == email).first().teacherID
    course = session.query(models.Course).filter(models.Course.courseName == course).first().courseID
    now = datetime.datetime.now()
    date = now.strftime("%Y-%m-%d")
    _fmin = now.strftime("%m")
    fmin = str(int(_fmin) - int(_fmin)%5)
    time = now.strftime("%Y-%m-%dT%H:"+fmin+":00")

    obj = models.Clas(courseID=course, teacherID=teacherID, date=date, time=time, duration=3600, active=1)
    session.add(obj)
    session.commit()

    session.refresh(obj)
    return obj.classID

def submit_response(session, studentID, questionID, response):
    vale = 0
    if response:
        vale = 1
    obj = models.Response(studentID=studentID, questionID=questionID, valid=vale)
    session.add(obj)
    session.commit()

    return {"message": "Submitted"}

def stop_class(session, classID):
    clas =  session.query(models.Clas).filter(models.Clas.classID == classID).first()
    clas.active = 0

    # _id = clas.classID
    #
    # _scoreboard = []
    #
    # for i in session.query(models.Question).filter(models.Question.classID == _id):
    #     for j in session.query(models.Response, func.count(models.Response)).filter(models.Response.questionID == i).filter(models.Response.valid == 1).group_by(models.Response.studentID).all()
    #         _scoreboard.append((j[0].studentID,j[1]))
    #
    # _scoreboard = sorted(_scoreboard, key=lambda x:x[1], reverse=True)
    #
    # rank = 1
    # for i in _scoreboard:
    #     session.add(models.Score(classID=_id, studentID=i[0], totalScore=i[1], rank=rank))
    #     rank += 1

    session.commit()

def enroll_class_in_db(session, studntID, classID):
    session.add(models.Enroll(classID=classID, studentID=studntID))
    session.commit()
    return {"message": "Enrolled"}


if __name__ == '__main__':
    engine = create_engine('mysql+pymysql://vedangj:password@localhost/paradigm')
    Session = sessionmaker(bind=engine)
    session = Session()
    stop_class(session, 2)
