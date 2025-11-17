##  Cal McLelland
#   Final Project
##  COMP 3005 Fall 2025
#   main.py

import code
import re
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy import Column, Integer, String, DateTime, Text, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

debug = False

# engine for Postgres
url = URL.create(
    drivername="postgresql+psycopg2",
    username="calmclelland",
    password="password123",
    host="localhost",
    port=5432,
    database="student",
)

engine = create_engine(url)

Base = declarative_base()

#table definition
class Student(Base):
    __tablename__ = "students"
    student_id = Column(Integer(), primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    dob = Column(DateTime(), default=datetime.now)


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

## define banner, exit and help messages
bannerMsg = "COMP3005 A3!"
exitMsg = "bye!"
helpMsg = (
    "\nValid commands are:\n"
    "   help                                                    "
    "list all commands\n"
    "   listStudents                                            "
    "list all student records\n"
    "   addStudent <first_name> <last_name> <email> <dob>       "
    "add a new student record with the specified values\n"
    "   updateStudentEmail <student_id> <new_email>             "
    "find the student with the specified id and update their email address\n"
    "   deleteStudent <student_id>                              "
    "delete the student record with the specified id\n"
    "   exit                                                    "
    "exit the program\n"
)
emailRegex = r"[^@]+@[^@]+\.[^@]+"

#initial insert statements
def createInitialRecords():
    john = Student(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        dob="2023-09-01",
    )
    jane = Student(
        first_name="Jane",
        last_name="Smith",
        email="jane.smith@example.com",
        dob="2023-09-01",
    )
    jim = Student(
        first_name="Jim",
        last_name="Beam",
        email="jim.beam@example.com",
        dob="2023-09-02",
    )

    students = session.query(Student).all()

    if students == []:
        session.add_all([john, jane, jim])
        session.commit()


# insert initial records
createInitialRecords()


# helper functions
def printStudent(student):
    print(
        "[Id: "
        + str(student.student_id)
        + ", First Name: "
        + student.first_name
        + ", Last Name: "
        + student.last_name
        + ", Email: "
        + student.email
        + ", DOB: "
        + str(student.dob)
        + "]"
    )


def listStudents():
    print("listing all students...")
    allStudents = session.query(Student).all()
    for student in allStudents:
        printStudent(student)


def addStudent(args):
    print("adding new student...")
    # check for valid arguments
    if len(args) != 4:
        print("incorrect number of arguments!")
        print("arguments should be:")
        print("<first_name> <last_name> <email> <dob>")
        return

    # check for valid email
    if not re.match(emailRegex, args[2]):
        print("not a valid email.\nstudent record not added")
        return

    # check for valid date
    try:
        dateCheck = datetime.strptime(args[3], "%Y-%m-%d")
    except ValueError:
        print("invalid Dob.\ndate format is YYYY-mm-dd\nstudent record not added.")
        return

    # create the new student object and add it
    newStudent = Student(
        first_name=args[0], last_name=args[1], email=args[2], dob=args[3]
    )
    session.add(newStudent)
    session.commit()


def updateStudentEmail(args):
    print("updating student email...")
    # check for valid arguments
    if len(args) != 2:
        print("incorrect number of arguments!")
        print("arguments should be:")
        print("<student_id> <email>")
        return

    # check for valid email
    if not re.match(emailRegex, args[1]):
        print("not a valid email.\nstudent record not updated")
        return

    # check if student exists
    allStudents = session.query(Student)
    currentStudent = allStudents.filter(Student.student_id == args[0]).first()

    if currentStudent is None:
        print("no student found with the specified student_id.")
        return

    # update the students email
    currentStudent.email = args[1]


def deleteStudent(args):
    print("deleting student...")
    # check for valid arguments
    if len(args) != 1:
        print("incorrect number of arguments!")
        print("arguments should be:")
        print("<student_id>")
        return

    # check if student exists
    allStudents = session.query(Student)
    currentStudent = allStudents.filter(Student.student_id == args[0]).first()

    if currentStudent is None:
        print("no student found with the specified student_id.")
        return

    printStudent(currentStudent)

    # delete student
    session.delete(currentStudent)
    session.commit()


# create a read-eval-print loop
class Repl(code.InteractiveConsole):
    def runsource(self, source, filename="<input>", symbol="single"):
        tokens = source.split()
        command = tokens[0]
        args = tokens[1:]
        if debug:
            print("command received: " + command + "\n")
            print("arguments: ")
            print(args)
            print("\n")
        match command:
            case "help":
                print(helpMsg)
            case "listStudents":
                listStudents()
            case "addStudent":
                addStudent(args)
            case "updateStudentEmail":
                updateStudentEmail(args)
            case "deleteStudent":
                deleteStudent(args)
            case "exit" | "quit":
                exit(0)
            case _:
                print("command not recognized:", source)


## create an interactive console
repl = Repl()
repl.interact(banner=bannerMsg, exitmsg=exitMsg)
