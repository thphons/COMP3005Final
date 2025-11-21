##  Cal McLelland
#   Final Project
##  COMP 3005 Fall 2025
#   main.py

import code
import re
import sys
import os
from pathlib import Path
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.engine import URL
from sqlalchemy import Column, Integer, String, DateTime, Text, text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

Base = declarative_base()

## add paths for imports
model_dir = os.path.abspath('./../models/')
sys.path.append(model_dir)

## imports for models
from member import Member
from admin import Administrator
from availability import Availability
from health_metric import Health_Metric
from room import Room
from session import Session
from trainer import Trainer

## import test data creation
from test_data import createInitialRecords

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

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# insert initial records
createInitialRecords(session)

## define banner, exit and help messages
bannerMsg = "COMP3005 Final Project!"
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
    


def addStudent(args):
    print("adding new student...")


def updateStudentEmail(args):
    print("updating student email...")


def deleteStudent(args):
    print("deleting student...")


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
