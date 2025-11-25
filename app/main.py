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
#logged out help message
helpMsg = (
    "\nValid commands are:\n"
    "   help                                                                            "
    "list all commands\n"
    "   registerMember <username> <password> <name> <dob> <gender> <email> <phone>      "
    "register as a member\n"
    "   login <login_type> <username> <password>                                        "
    "login\n"
    "   exit                                                                            "
    "exit the program\n"
)
#logged member help message
memberHelpMsg = (
    "\nValid commands are:\n"
    "   help                                                                            "
    "list all commands\n"
    "   viewProfile                                                                     "
    "view your profile\n"
    "   updateMemberEmail <email>                                                       "
    "update your current email address\n"
    "   updateMemberPhone <phone>                                                       "
    "update your current phone number\n"
    "   logGoal <target_date> <weight> <height> <VO2max> <body_comp> <resting_hr>       "
    "add a new goal or update your current goal\n"
    "   logMetrics <weight> <height> <VO2max> <body_comp> <resting_hr>                  "
    "log your current health metrics\n"
    "   showDashboard                                                                   "
    "display your goal and health metrics\n"
    "   exit                                                                            "
    "exit the program\n"
)
#logged trainer help message
trainerHelpMsg = (
    "\nValid commands are:\n"
    "   help                                                                            "
    "list all commands\n"
    "   registerMember <username> <password> <name> <dob> <gender> <email> <phone>      "
    "register as a member\n"
    "   login <login_type> <username> <password>                                        "
    "login\n"
    "   exit                                                                            "
    "exit the program\n"
)
#logged admin help message
adminHelpMsg = (
    "\nValid commands are:\n"
    "   help                                                                            "
    "list all commands\n"
    "   registerMember <username> <password> <name> <dob> <gender> <email> <phone>      "
    "register as a member\n"
    "   login <login_type> <username> <password>                                        "
    "login\n"
    "   exit                                                                            "
    "exit the program\n"
)

#########################
##  Session Variables  ##
#########################

# object to store session data
session_data = {}

########################
##  Helper Functions  ##
########################

def printMember(member):
    print(f"\nId: {member.id},\nUsername: {member.username},\nName: {member.name},\nDOB: {member.dob}\nGender: {member.gender},\nEmail: {member.email},\nPhone: {member.phone}\n")

def printMetric(metric):
    if metric.record_type == "goal":
        print(f"Target Date: {metric.date}, Weight: {metric.weight}, Height: {metric.height}, VO2max: {metric.vo2Max}, Body Composition: {metric.body_composition}, Resting Heart Rate: {metric.resting_hr}")
    else:
        print(f"Log Date: {metric.date}, Weight: {metric.weight}, Height: {metric.height}, VO2max: {metric.vo2Max}, Body Composition: {metric.body_composition}, Resting Heart Rate: {metric.resting_hr}")

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
    return 'id' in session_data

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

            session_data['id'] = user.id
            session_data['username'] = user.username
            session_data['type'] = 'member'

            print("Logged in.")

        case "trainer":
            #login as trainer
            user_query = select(Trainer).where(Trainer.username == args[1], Trainer.password_hash == args[2])
            user = session.scalars(user_query).first()

            if user == None:
                #login failed
                print("incorrect username or password.")
                return

            session_data['id'] = user.id
            session_data['username'] = user.username
            session_data['type'] = 'trainer'

            print("Logged in.")

        case "admin":
            #login as administrator
            user_query = select(Administrator).where(Administrator.username == args[1], Administrator.password_hash == args[2])
            user = session.scalars(user_query).first()

            if user == None:
                #login failed
                print("incorrect username or password.")
                return

            session_data['id'] = user.id
            session_data['username'] = user.username
            session_data['type'] = 'admin'

            print("Logged in.")

        case _:
            print("invalid login type.\naccepted login types are:\n\n-> member\n-> trainer\n-> admin\n")

def logout():
    print("Logging out...")
    session_data.clear()
    print("Logged out.")


########################
##  Member Functions  ##
########################

## Function 1 -- User Registration
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

    user = session.get(Member, session_data['id'])

    printMember(user)

## Update personal details   
def updateMemberEmail(args):

    #check for correct number of arguments
    if not (checkArgumentCount(args, 1)):
        return

    if not (validEmail(args[0])):
        return

    print("updating current user email...")

    user = session.get(Member, session_data['id'])
    user.email = args[0]

    session.commit()

def updateMemberPhone(args):

    #check for correct number of arguments
    if not (checkArgumentCount(args, 1)):
        return

    if not (validPhone(args[0])):
        return

    print("updating current user email...")

    user = session.get(Member, session_data['id'])
    user.phone = args[0]

    session.commit()

def logGoal(args):
    print("adding/updating goal for current user...")

    #check arguments...
    if not checkArgumentCount(args, 6):
        return

    if not validDate(args[0]):
        return

    #check if user has a goal...
    goal_query = select(Health_Metric).where(Health_Metric.user_id == session_data['id'], Health_Metric.record_type == "goal")
    goal = session.scalars(goal_query).first()

    #no goal, add one
    if not goal:
        newGoal = Health_Metric(
            date = args[0],
            record_type = 'goal',
            user_id = session_data['id'],
            weight = args[1],
            height = args[2],
            vo2Max = args[3],
            body_composition = args[4],
            resting_hr = args[5],
        )

        session.add(newGoal)
        session.commit()
        return

    #update current goal
    goal.date = args[0]  
    goal.weight = args[1]
    goal.height = args[2]
    goal.vo2Max = args[3]
    goal.body_composition = args[4]
    goal.resting_hr = args[5]  

    session.commit()

def logMetrics(args):
    print("adding a new health metric measurement...")

    #check arguments...
    if not checkArgumentCount(args, 5):
        return

    newRecord = Health_Metric(
        date = datetime.now(),
        record_type = 'record',
        user_id = session_data['id'],
        weight = args[0],
        height = args[1],
        vo2Max = args[2],
        body_composition = args[3],
        resting_hr = args[4],
    )

    session.add(newRecord)
    session.commit()

## Function 3 -- Health History
def healthHistory(args):
    print("showing member health history...")

## TODO: -- add multiple health metrics at once?

## Function 4 -- Dashboard TODO: -- classes?
def showDashboard(args):
    print("showing member dashboard...\n")

    #show goal
    goal_query = select(Health_Metric).where(Health_Metric.user_id == session_data['id'], Health_Metric.record_type == "goal")
    goal = session.scalars(goal_query).first()

    if not goal:
        print("No current goal.\n")
    else:
        print("Current Goal:")
        printMetric(goal)

    #show health stats
    records_query = select(Health_Metric).where(Health_Metric.user_id == session_data['id'], Health_Metric.record_type == "record")
    records = session.scalars(records_query).all()

    if not records:
        print("\nNo logged health metrics.\n")
    else:
        print("\nShowing Records:")
        for record in records:
            printMetric(record)


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

##########################
##  Command processing  ##
##########################

def commandLoggedOut(command, args, source):
    match command:
        case "help":
            print(helpMsg)
        # logged out features
        case "registerMember":
            registerMember(args)
        case "login":
            login(args)
        case _:
                print("command not recognized:", source)
            

def commandMember(command, args, source):
    match command:
        case "help":
            print(memberHelpMsg)
        case "logout":
            logout()
        case "viewProfile":
            viewProfile(args)
        case "updateMemberEmail":
            updateMemberEmail(args)
        case "updateMemberPhone":
            updateMemberPhone(args)
        case "logGoal":
            logGoal(args)
        case "logMetrics":
            logMetrics(args)
        case "healthHistory":
            healthHistory(args)
        case "showDashboard":
            showDashboard(args)
        case _:
            print("member command not recognized:", source)

def commandTrainer(command, args, source):
    match command:
        case "help":
            print(trainerHelpMsg)
        case "logout":
            logout()
        case _:
            print("trainer command not recognized:", source)

def commandAdmin(command, args, source):
    match command:
        case "help":
            print(adminHelpMsg)
        case "logout":
            logout()
        case _:
            print("admin command not recognized:", source)
    

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
            print(f"\nCurrent User: {session_data['username']}\n")

        if ((command == "exit") or (command == "quit")):
            exit(0)

        if loggedIn():
            print(f"Current session: {session_data['type']} -> {session_data['username']}")
            match session_data['type']:
                case "member":
                    commandMember(command, args, source)
                case "trainer":
                    commandTrainer(command, args, source)
                case "admin":
                    commandAdmin(command, args, source)
                case _:
                    commandLoggedOut(command, args, source)
            return
        
        commandLoggedOut(command, args, source)

## create an interactive console
repl = Repl()
repl.interact(banner=bannerMsg, exitmsg=exitMsg)
