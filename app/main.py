##  Cal McLelland
#   Final Project
##  COMP 3005 Fall 2025
#   main.py

import code
import re
import sys
from pathlib import Path
from sqlalchemy import create_engine, event, DDL, text
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select, insert, update, delete
from sqlalchemy import Column, Integer
from datetime import datetime
from sqlalchemy import Table, MetaData
from sqlalchemy.orm import registry

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
from models.class_ import Class
from models.trainer import Trainer

# Import test data
from test_data import createInitialRecords, reset

# Import trigger
from trigger import create_room_conflict_trigger

# Import view
import view

DEBUG = False
# Set this flag to True to reset database
RESET_DATABASE = True

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

create_room_conflict_trigger(session)

metadata_reflect = MetaData()
schedule_table = Table(
    "schedule",
    metadata_reflect,
    Column("event_id", Integer, primary_key=True),  # explicit PK for the view
    autoload_with=engine,
)

mapper_registry = registry()

@mapper_registry.mapped
class ScheduleView:
    __table__ = schedule_table

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
    "   logGoal <target_date> <weight> <height> <vo2max> <body_comp> <resting_hr>       "
    "add a new goal or update your current goal\n"
    "   logMetrics <weight> <height> <vo2max> <body_comp> <resting_hr>                  "
    "log your current health metrics\n"
    "   logHealthHistory <date> <weight> <height> <vo2max> <body_comp> <resting_hr>     "
    "log historic health metrics\n"
    "   showDashboard                                                                   "
    "display your goal and health metrics\n"
    "   logout                                                                          "
    "log out of the session\n"
    "   exit                                                                            "
    "exit the program\n"
)
#logged trainer help message
trainerHelpMsg = (
    "\nValid commands are:\n"
    "   help                                                                            "
    "list all commands\n"
    "   lookupMember <name>                                                             "
    "lookup the member with the specified name\n"
    "   addAvailability <start_time> <end_time>                                         "
    "add a new availability\n"
    "   logout                                                                          "
    "log out of the session\n"
    "   exit                                                                            "
    "exit the program\n"
)
#logged admin help message
adminHelpMsg = (
    "\nValid commands are:\n"
    "   help                                                                            "
    "list all commands\n"
    "   bookClass <class_id> <room_id>                                                  "
    "assign the specified class to the specified room\n"
    "   bookSession <session_id> <room_id>                                              "
    "assign the specified session to the specified room\n"
    "   createNewClass <room_id> <start_time> <end_time> <trainer_id>                   "
    "create a new class with the specified data\n"
    "   assignTrainerToClass <class_id> <trainer_id>                                    "
    "assign the specified trainer to the specified class\n"
    "   assignTrainerToSession <session_id> <trainer_id>                                "
    "assign the specified trainer to the specified session\n"
    "   updateClassTime <class_id> <start_time> <end_time>                              "
    "update the time for the specified class\n"
    "   updateSessionTime <session_id> <start_time> <end_time>                          "
    "update the time for the specified session\n"
    "   viewSchedule                                                                    "
    "view the current schedule of classes and sessions\n"
    "   logout                                                                          "
    "log out of the session\n"
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

def printMemberDetails(member):
    print(f"\nId: {member.id},\nUsername: {member.username},\nName: {member.name},\nDOB: {member.dob}\nGender: {member.gender},\nEmail: {member.email},\nPhone: {member.phone}\n")

    #show goal
    goal_query = select(Health_Metric).where(Health_Metric.user_id == member.id, Health_Metric.record_type == "goal")
    goal = session.scalars(goal_query).first()

    if not goal:
        print("No current goal.\n")
    else:
        print("Current Goal:")
        printMetric(goal)

    #show health stats
    record_query = select(Health_Metric).where(Health_Metric.user_id == member.id, Health_Metric.record_type == "record").order_by(Health_Metric.date.desc())
    record = session.scalars(record_query).first()

    if not record:
        print("\nNo logged health metrics.\n")
    else:
        print("\nShowing Latest Record:")
        printMetric(record)

def printSchedule(schedule):
    for event in schedule:
        print(f"Room ID: {event.room_id}, Start Time: {event.start_time}, End Time: {event.end_time}, Trainer ID: {event.trainer_id}, Event Type: {event.schedule_type}")

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
        dateCheck = datetime.fromisoformat(date)
        return True
    except ValueError:
        print("invalid Dob.\ndate format must be iso format")
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

def checkAvailabilities(trainer_id, start_time, end_time):
    availabilities_query = select(Availability).where(Availability.trainer_id == trainer_id)
    availabilities = session.scalars(availabilities_query).all()

    for availability in availabilities:
        if (availability.start_time <= start_time and 
            availability.end_time >= end_time):
            return True

    return False

def checkConflict(start_time_a, end_time_a, start_time_b, end_time_b):
    return  ((start_time_a < start_time_b and 
             end_time_a > start_time_b) or
            (start_time_a > start_time_b and
             end_time_a < end_time_b) or
            (start_time_a < end_time_b and
             end_time_a > end_time_b) or
            (start_time_a < start_time_b and
             end_time_a > end_time_b))

def checkRoomAvailability(room_id, start_time, end_time):
    classes_query = select(Class).where(Class.room_id == room_id)
    classes = session.scalars(classes_query).all()

    private_sessions_query = select(TrainingSession).where(TrainingSession.room_id == room_id)
    private_sessions = session.scalars(private_sessions_query).all()

    for each_class in classes:
        if checkConflict(start_time, end_time, each_class.start_time, each_class.end_time):
            return False

    for private_session in private_sessions:
        if checkConflict(start_time, end_time, private_session.start_time, private_session.end_time):
            return False

    return True

def checkTrainerAvailability(trainer_id, start_time, end_time):
    classes_query = select(Class).where(Class.trainer_id == trainer_id)
    classes = session.scalars(classes_query).all()

    private_sessions_query = select(TrainingSession).where(TrainingSession.trainer_id == trainer_id)
    private_sessions = session.scalars(private_sessions_query).all()

    ## TODO: -- print errors here?

    for each_class in classes:
        if checkConflict(start_time, end_time, each_class.start_time, each_class.end_time):
            return False

    for private_session in private_sessions:
        if checkConflict(start_time, end_time, private_session.start_time, private_session.end_time):
            return False

    if not checkAvailabilities(trainer_id, start_time, end_time):
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
##################################

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
###################################

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
###############################

def logHealthHistory(args):
    print("showing member health history...")
    
    #check arguments...
    if not checkArgumentCount(args, 6):
        return

    if not validDate(args[0]):
        return

    newRecord = Health_Metric(
        date = datetime(args[0]),
        record_type = 'record',
        user_id = session_data['id'],
        weight = args[1],
        height = args[2],
        vo2Max = args[3],
        body_composition = args[4],
        resting_hr = args[5],
    )

    session.add(newRecord)
    session.commit()

## Function 4 -- Dashboard #TODO: -- classes / sessions?
############################################

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
    records_query = select(Health_Metric).where(Health_Metric.user_id == session_data['id'], Health_Metric.record_type == "record").order_by(Health_Metric.date.desc())
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
#################################

def addAvailability(args):
    print("adding new availability...")

    #check arguments
    if not checkArgumentCount(args, 2):
        return
    
    if not validDate(args[0]):
        return 

    if not validDate(args[1]):
        return

    startTime = datetime.fromisoformat(args[0])
    endTime = datetime.fromisoformat(args[1])

    if endTime < startTime:
        print("the end time of an availability cannot be before the start time.")
        return

    #check for availability conflicts
    if checkTrainerAvailability(session_data['id'], startTime, endTime):
        print("found conflict with current availabilities.")
        return
    
    ## TODO: -- check for scheduled conflicts

    newAvailability = Availability(
        trainer_id = session_data['id'],
        start_time = args[0],
        end_time = args[1],
    )

    session.add(newAvailability)
    session.commit()

    print("Successfully added new availability.")

## Function 6 -- Member Lookup
##############################

def lookupMember(args): 
    print("looking up member...")

    #check arguments --  allow for one or two
    if len(args) == 2:
        member_name = args[0] + " " + args[1]
    elif len(args) == 1:
        member_name = args[0]
    else:
        checkArgumentCount(args, -1)

    #track start time
    query_start = datetime.now()

    ## TODO: -- case insensitive
    member_query = select(Member).where(Member.name == member_name)
    member = session.scalars(member_query).first()

    #track start time
    query_end = datetime.now()

    print(f"Member lookup completed in {((query_end - query_start) * 1000)} milliseconds.")

    if not member:
        print(f"no member found named {member_name}")
        return

    printMemberDetails(member)

###############################
##  Administrative Functions ##
###############################

## Function 7 -- Room Booking
#############################

def bookClass(args):
    print("book a room for a class...")

    #check arguments
    checkArgumentCount(args, 2)

    #check that the room is free
    currentClass = session.get(Class, args[0])
    
    if not currentClass:
        print("no class found with the specified id")
        return

    currentRoom = session.get(Room, args[1])

    if not currentRoom:
        print("no room found with the specified id")
        return

    #update the room for the class
    currentClass.room_id = currentRoom.id
    session.commit()

def bookSession(args):
    print("book a room for a session...")

    #check arguments
    checkArgumentCount(args, 2)

    #check that the room is free
    currentSession = session.get(TrainingSession, args[0])
    
    if not currentSession:
        print("no class found with the specified id")
        return
    
    if not checkRoomAvailability(args[1], currentSession.start_time, currentSession.end_time):
        print("found time conflict with the specified room.")
        return

    #update the room for the class
    currentSession.room_id = args[1]
    session.commit()

## Function 8 -- Class Management
#################################

def createNewClass(args):
    print("creating a new class...")

    checkArgumentCount(args, 4)

    #check for valid datetimes
    if not validDate(args[1]):
        print("invalid datetime format for start time")
        return

    if not validDate(args[2]):
        print("invalid datetime format for start time")
        return

    #check for valid trainer id
    currentTrainer = session.get(Trainer, args[3])

    if not currentTrainer:
        print("not trainer for the specified trainer id")
        return

    start_time = datetime.fromisoformat(args[1])
    end_time = datetime.fromisoformat(args[2])

    #check room availability
    if not checkRoomAvailability(args[0], start_time, end_time):
        print("found time conflict for the specified room")
        return

    #check trainer availability
    if not checkTrainerAvailability(args[3], start_time, end_time):
        print("trainer not available at the specified time")
        return

    newClass = Class(
        room_id = args[0],
        start_time = start_time,
        end_time = end_time,
        trainer_id = args[3],
    )

    session.add(newClass)
    session.commit()

def assignTrainerToClass(args):
    print("assigning a trainer to a class...")

    #check arguments
    checkArgumentCount(args, 2)

    currentClass = session.get(Class, args[0])

    if not currentClass:
        print("no class found with the specified id")
        return

    currentTrainer = session.get(Trainer, args[1])

    if not currentTrainer:
        print("no trainer found with the specified id")
        return

    #check availability
    if not checkTrainerAvailability(trainer_id, currentClass.start_time, currentClass.end_time):
        print("the trainer is not available at the specified time")

    currentClass.trainer_id = currentTrainer.trainer_id
    session.commit()

def assignTrainerToSession(args):
    print("assigning a trainer to a session...")

    #check arguments
    checkArgumentCount(args, 2)

    currentSession = session.get(TrainingSession, args[0])

    if not currentSession:
        print("no session found with the specified id")
        return

    currentTrainer = session.get(Trainer, args[1])

    if not currentTrainer:
        print("no trainer found with the specified id")
        return

    #check availability
    if not checkTrainerAvailability(trainer_id, currentSession.start_time, currentSession.end_time):
        print("the trainer is not available at the specified time")

    currentSession.trainer_id = currentTrainer.trainer_id
    session.commit()

def updateClassTime(args):
    print("updating session time...")

    checkArgumentCount(args, 3)

    currentClass = session.get(Class, args[0])

    if not currentClass:
        print("no class found with the specified id")
        return

    #check valid datetimes
    if not validDate(args[1]):
        print("start time is not a valid datetime")

    newStartTime = datetime(args[1])

    if not validDate(args[2]):
        print("end time is not a valid datetime")

    newEndTime = datetime(args[2])        

    if not checkTrainerAvailability(currentClass.trainer_id, newStartTime, newEndTime):
        print("trainer not available at the specified time")

    currentClass.start_time = newStartTime
    currentClass.end_time = newEndTime
    session.commit()

def updateSessionTime(args):
    print("updating session time...")

    checkArgumentCount(args, 3)

    checkArgumentCount(args, 3)

    currentSession = session.get(TrainingSession, args[0])

    if not currentSession:
        print("no session found with the specified id")
        return

    #check valid datetimes
    if not validDate(args[1]):
        print("start time is not a valid datetime")

    newStartTime = datetime(args[1])

    if not validDate(args[2]):
        print("end time is not a valid datetime")

    newEndTime = datetime(args[2])        

    if not checkTrainerAvailability(currentSession.trainer_id, newStartTime, newEndTime):
        print("trainer not available at the specified time")

    currentSession.start_time = newStartTime
    currentSession.end_time = newEndTime
    session.commit()

def viewSchedule():
    schedule_query = select(ScheduleView).order_by(ScheduleView.start_time)
    schedule = session.scalars(schedule_query).all()
    if not schedule:
        print("No classes or sessions scheduled found")
        return
    printSchedule(schedule)

##########################
##  Command Processing  ##
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
        case "logHealthHistory":
            logHealthHistory(args)
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
        case "addAvailability":
            addAvailability(args)
        case "lookupMember":
            lookupMember(args)
        case _:
            print("trainer command not recognized:", source)

def commandAdmin(command, args, source):
    match command:
        case "help":
            print(adminHelpMsg)
        case "logout":
            logout()
        case "bookClass":
            bookClass(args)
        case "bookSession":
            bookSession(args)
        case "createNewClass":
            createNewClass(args)
        case "assignTrainerToClass":
            assignTrainerToClass(args)
        case "assignTrainerToSession":
            assignTrainerToSession(args)
        case "updateClassTime":
            updateClassTime(args)
        case "updateSessionTime":
            updateSessionTime(args)
        case "viewSchedule":
            viewSchedule()
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
