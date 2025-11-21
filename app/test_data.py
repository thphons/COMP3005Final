import sys
import os

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


def createInitialRecords(session):
    john = Member(
        username="John",
        password_hash="password",
        name="John Doe",
        dob="2023-09-01",
        gender="Male",
        email="john.doe@example.com",
        phone="555-123-4567",
    )
    jane = Trainer(
        username="Jane",
        password_hash="password",
        name="Jane Doe",
        dob="2023-09-01",
        gender="Female",
        email="jane.doe@example.com",
        phone="555-123-7654",
    )
    jim = Administrator(
        username="Jim",
        password_hash="password",
        name="Jim Bo",
        dob="1987-04-17",
        gender="Male",
        email="jim.bo@example.com",
        phone="555-765-4321",
    )

    members = session.query(Member).all()

    if members == []:
        session.add_all([john])
        session.commit()

    if trainers == []:
        session.add_all([jane])
        session.commit()

    if administrators == []:
        session.add_all([jim])
        session.commit()
