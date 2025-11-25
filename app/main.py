##  Cal McLelland
#   Final Project
##  COMP 3005 Fall 2025
#   main.py

import code
import re
import sys
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, update, delete
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import Base and all models
from models.base import Base
from models.member import Member
from models.admin import Administrator
from models.availability import Availability
from models.health_metric import Health_Metric
from models.room import Room
from models.session import Session as TrainingSession
from models.trainer import Trainer

# Import test data
from test_data import createInitialRecords, reset

DEBUG = False
# Set this flag to True to reset database
RESET_DATABASE = False

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

# reset if flag is set to true
if RESET_DATABASE:
    reset(engine)

# Create all tables
Base.metadata.create_all(engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

# insert initial records
createInitialRecords(session)

## define banner, exit and help messages
bannerMsg = "COMP3005 Final Project!"
exitMsg = "bye!"
helpMsg = (
    "\nValid commands are:\n"
    "   help                                                    "
    "list all commands\n"
    "   listMembers                                             "
    "list all member records\n"
    "   addMember <username> <name> <email>                     "
    "add a new member\n"
    "   exit                                                    "
    "exit the program\n"
)

#########################
##  Session Variables  ##
#########################

sessionUser = -1
sessionUsername = ""
sessionType = ""

########################
##  Helper Functions  ##
########################

def printMember(member):
    print(f"\nId: {member.id},\nUsername: {member.username},\nName: {member.name},\nDOB: {member.dob}\nGender: {member.gender},\nEmail: {member.email},\nPhone: {member.phone}\n")

def checkArgumentCount(args, count):
    if len(args) != count:
        print("incorrect number of arguments!")
        print(f"this command takes {count} arguments.")
        return False
    return True

def validDate(date):
    try:
        dateCheck = datetime.strptime(date, "%Y-%m-%d")
        return True
    except ValueError:
        print("invalid Dob.\ndate format is YYYY-mm-dd")
        return False

def validEmail(email):
    emailRegex = r"[^@]+@[^@]+\.[^@]+"

    if not re.match(emailRegex, email):
        print("not a valid email.")
        return False
    return True

def validPhone(phone):
    phoneRegex = r"[0-9]{3}[-.\ ]?[0-9]{3}[-.\ ]?[0-9]{4}"

    if not re.match(phoneRegex, phone):
        print("not a valid email.")
        return False
    return True

def loggedIn():
    return not (sessionUser == -1)

######################################
##  Requirement Adjacent Functions  ##
######################################

def login(args):
    print("logging in...")
    if not (checkArgumentCount(args, 3)):
        return
    
    match args[0]:
        case "member":
            #login as member
            user_query = select(Member).where(Member.username == args[1], Member.password_hash == args[2])
            user = session.scalars(user_query).first()

            if user == None:
                #login failed
                print("incorrect username or password.")
                return

            sessionUser = user.id
            sessionUsername = user.username
            sessionType = "member"

            print("Logged in.")

        case "trainer":
            #login as trainer
            user_query = select(Trainer).where(Trainer.username == args[1], Trainer.password_hash == args[2])
            user = session.scalars(user_query).first()

            if user == None:
                #login failed
                print("incorrect username or password.")
                return

            sessionUser = user.id
            sessionUsername = user.username
            sessionType = "trainer"

            print("Logged in.")

        case "admin":
            #login as administrator
            user_query = select(Administrator).where(Administrator.username == args[1], Administrator.password_hash == args[2])
            user = session.scalars(user_query).first()

            if user == None:
                #login failed
                print("incorrect username or password.")
                return

            sessionUser = user.id
            sessionUsername = user.username
            sessionType = "administrator"

            print("Logged in.")

        case _:
            print("invalid login type.\naccepted login types are:\n\n-> member\n-> trainer\n-> admin\n")

def logout():
    print("Logging out...")
    sessionUser = -1
    sessionUsername = ""
    sessionType = ""
    print("Logged out.")


########################
##  Member Functions  ##
########################

## Function 1 -- User Registration
## args -> <name> <>
def registerMember(args):
    print("register a new member...")

    #check for correct number of arguments
    if not (checkArgumentCount(args, 7)):
        return

    #check for valid arguments
    if not (validDate(args[3])):
        return
    
    if not (validEmail(args[5])):
        return

    if not (validPhone(args[6])):
        return

    #register new user
    newMember = Member(
        username=args[0], 
        password_hash=args[1], 
        name=args[2], 
        dob=args[3],
        gender = args[4],
        email = args[5],
        phone = args[6]
    )
    session.add(newMember)
    session.commit()

    print("Member registered!")
    printMember(newMember)
    print("Please login.")

## Function 2 -- Profile Management
def viewProfile(args):
    print("viewing current profile...")

def updateProfile(args):
    print("updating current user...")

def addGoal(args):
    print("adding/updating goal for current user...")

def addHealthMetric(args):
    print("adding a new health metric measurement...")

## Function 3 -- Health History
def healthHistory(args):
    print("showing member health history...")

## TODO: -- add multiple health metrics at once?

## Function 4 -- Dashboard
def showDashboard(args):
    print("showing member dashboard...")


#########################
##  Trainer Functions  ##
#########################

## Function 5 -- Set Availability
def addAvailability(args):
    print("adding new availability...")

## Function 6 -- Member Lookup
def lookupMember(args):
    print("looking up member...")

###############################
##  Administrative Functions ##
###############################

## Function 7 -- Room Booking
def bookRoom(args):
    print("book a room...")

## Function 8 -- Class Management
def createNewClass(args):
    print("creating a new class...")

def assignTrainer(args):
    print("assigning a trainer to a class...")

## TODO: -- update schedules?


# create a read-eval-print loop
class Repl(code.InteractiveConsole):
    def runsource(self, source, filename="<input>", symbol="single"):
        if not source.strip():
            return
        tokens = source.split()
        command = tokens[0]
        args = tokens[1:]
        if DEBUG:
            print(f"command received: {command}\narguments: {args}\n")
        if loggedIn():
            print(f"\nCurrent User: {sessionUsername}\n")
        match command:
            case "help":
                print(helpMsg)
            case "login":
                login(args)
            case "logout":
                logout()
            case "registerMember":
                registerMember(args)
            case "viewProfile":
                viewProfile(args)
            case "healthHistory":
                healthHistory(args)
            case "showDashboard":
                showDashboard(args)
            case "exit" | "quit":
                exit(0)
            case _:
                print("command not recognized:", source)

        


## create an interactive console
repl = Repl()
repl.interact(banner=bannerMsg, exitmsg=exitMsg)
