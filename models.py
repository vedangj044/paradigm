# coding: utf-8
from sqlalchemy import Column, Date, DateTime, ForeignKey, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Course(Base):
    __tablename__ = 'course'

    courseName = Column(String(100), nullable=False)
    courseID = Column(INTEGER(11), primary_key=True)


class QuestionType(Base):
    __tablename__ = 'questionType'

    questionTypeID = Column(INTEGER(11), primary_key=True)
    questionTypeName = Column(String(10), nullable=False)


class Student(Base):
    __tablename__ = 'student'

    name = Column(String(100), nullable=False)
    gender = Column(String(10), nullable=False)
    age = Column(INTEGER(11))
    profilePicture = Column(String(500), server_default=text("'https://www.pngitem.com/pimgs/m/41-415019_profile-man-male-free-picture-male-avatar-clipart.png'"))
    studentID = Column(INTEGER(11), primary_key=True)


class Teacher(Base):
    __tablename__ = 'teacher'

    teacherID = Column(INTEGER(11), primary_key=True)
    teacherName = Column(String(100), nullable=False)
    teacherEmail = Column(String(100), nullable=False)


class Clas(Base):
    __tablename__ = 'class'

    classID = Column(INTEGER(11), primary_key=True)
    courseID = Column(ForeignKey('course.courseID'), nullable=False, index=True)
    date = Column(Date, nullable=False)
    time = Column(DateTime, nullable=False)
    duration = Column(INTEGER(11), nullable=False)
    active = Column(TINYINT(1), nullable=False)
    teacherID = Column(ForeignKey('teacher.teacherID'), nullable=False, index=True)

    course = relationship('Course')
    teacher = relationship('Teacher')


class CourseStudent(Base):
    __tablename__ = 'course_student'

    course_studentID = Column(String(10), primary_key=True)
    studentID = Column(ForeignKey('student.studentID', ondelete='CASCADE'), nullable=False, index=True)
    courseID = Column(ForeignKey('course.courseID', ondelete='CASCADE'), nullable=False, index=True)

    course = relationship('Course')
    student = relationship('Student')


class CourseTeacher(Base):
    __tablename__ = 'course_teacher'

    course_teacherID = Column(String(100), primary_key=True)
    courseID = Column(ForeignKey('course.courseID'), nullable=False, index=True)
    teacherID = Column(ForeignKey('teacher.teacherID'), nullable=False, index=True)

    course = relationship('Course')
    teacher = relationship('Teacher')


class Enroll(Base):
    __tablename__ = 'enroll'

    enrollID = Column(INTEGER(11), primary_key=True)
    classID = Column(ForeignKey('class.classID'), nullable=False, index=True)
    studentID = Column(ForeignKey('student.studentID'), nullable=False, index=True)

    clas = relationship('Clas')
    student = relationship('Student')


class Question(Base):
    __tablename__ = 'question'

    questionID = Column(INTEGER(11), primary_key=True)
    questionTypeID = Column(ForeignKey('questionType.questionTypeID'), nullable=False, index=True)
    text = Column(Text, nullable=False)
    option = Column(Text)
    correctOption = Column(INTEGER(11))
    correctTF = Column(TINYINT(1))
    classID = Column(ForeignKey('class.classID'), nullable=False, index=True)
    asked = Column(TINYINT(1), nullable=False)

    clas = relationship('Clas')
    questionType = relationship('QuestionType')


class Score(Base):
    __tablename__ = 'score'

    scoreID = Column(INTEGER(11), primary_key=True)
    classID = Column(ForeignKey('class.classID'), nullable=False, index=True)
    studentID = Column(ForeignKey('student.studentID'), nullable=False, index=True)
    totalScore = Column(INTEGER(11), nullable=False)
    rank = Column(INTEGER(11))

    clas = relationship('Clas')
    student = relationship('Student')


class QuestionAsked(Base):
    __tablename__ = 'question_asked'

    questionAsked = Column(String(10), primary_key=True)
    questionID = Column(ForeignKey('question.questionID'), nullable=False, index=True)
    studentID = Column(ForeignKey('student.studentID'), nullable=False, index=True)

    question = relationship('Question')
    student = relationship('Student')


class Response(Base):
    __tablename__ = 'response'

    responseID = Column(INTEGER(11), primary_key=True)
    questionID = Column(ForeignKey('question.questionID', ondelete='CASCADE'), nullable=False, index=True)
    studentID = Column(ForeignKey('student.studentID', ondelete='CASCADE'), nullable=False, index=True)
    valid = Column(TINYINT(1), nullable=False)

    question = relationship('Question')
    student = relationship('Student')
