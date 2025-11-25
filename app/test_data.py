import sys
from pathlib import Path
from datetime import datetime

# Add parent directory to path so models is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import models with proper paths
from models.member import Member
from models.admin import Administrator
from models.trainer import Trainer
from models.base import Base


def reset(engine):
    Base.metadata.drop_all(engine)


def createInitialRecords(session):

    # 30 unique members with real names
    member_data = [
        ("alice_smith", "Alice Smith", "1992-03-15", "Female", "alice.smith@example.com", "5550000101"),
        ("bob_johnson", "Bob Johnson", "1988-07-22", "Male", "bob.johnson@example.com", "5550000102"),
        ("carol_williams", "Carol Williams", "1995-11-08", "Female", "carol.williams@example.com", "5550000103"),
        ("david_brown", "David Brown", "1990-05-14", "Male", "david.brown@example.com", "5550000104"),
        ("emma_davis", "Emma Davis", "1993-09-19", "Female", "emma.davis@example.com", "5550000105"),
        ("frank_miller", "Frank Miller", "1987-01-26", "Male", "frank.miller@example.com", "5550000106"),
        ("grace_wilson", "Grace Wilson", "1994-06-12", "Female", "grace.wilson@example.com", "5550000107"),
        ("henry_moore", "Henry Moore", "1989-04-03", "Male", "henry.moore@example.com", "5550000108"),
        ("iris_taylor", "Iris Taylor", "1996-08-21", "Female", "iris.taylor@example.com", "5550000109"),
        ("jack_anderson", "Jack Anderson", "1991-02-10", "Male", "jack.anderson@example.com", "5550000110"),
        ("karen_thomas", "Karen Thomas", "1993-12-05", "Female", "karen.thomas@example.com", "5550000111"),
        ("liam_jackson", "Liam Jackson", "1990-10-17", "Male", "liam.jackson@example.com", "5550000112"),
        ("mia_white", "Mia White", "1994-07-29", "Female", "mia.white@example.com", "5550000113"),
        ("noah_harris", "Noah Harris", "1988-03-11", "Male", "noah.harris@example.com", "5550000114"),
        ("olivia_martin", "Olivia Martin", "1995-09-25", "Female", "olivia.martin@example.com", "5550000115"),
        ("peter_garcia", "Peter Garcia", "1992-05-08", "Male", "peter.garcia@example.com", "5550000116"),
        ("quinn_rodriguez", "Quinn Rodriguez", "1991-11-30", "Female", "quinn.rodriguez@example.com", "5550000117"),
        ("ryan_martinez", "Ryan Martinez", "1989-08-14", "Male", "ryan.martinez@example.com", "5550000118"),
        ("sophie_hernandez", "Sophie Hernandez", "1996-02-22", "Female", "sophie.hernandez@example.com", "5550000119"),
        ("thomas_lopez", "Thomas Lopez", "1993-06-19", "Male", "thomas.lopez@example.com", "5550000120"),
        ("uma_gonzalez", "Uma Gonzalez", "1992-01-07", "Female", "uma.gonzalez@example.com", "5550000121"),
        ("victor_perez", "Victor Perez", "1987-09-16", "Male", "victor.perez@example.com", "5550000122"),
        ("wendy_sanchez", "Wendy Sanchez", "1994-04-13", "Female", "wendy.sanchez@example.com", "5550000123"),
        ("xavier_morris", "Xavier Morris", "1990-12-28", "Male", "xavier.morris@example.com", "5550000124"),
        ("yara_rogers", "Yara Rogers", "1995-03-05", "Female", "yara.rogers@example.com", "5550000125"),
        ("zoe_reed", "Zoe Reed", "1993-10-11", "Female", "zoe.reed@example.com", "5550000126"),
        ("adam_cook", "Adam Cook", "1988-06-20", "Male", "adam.cook@example.com", "5550000127"),
        ("bella_morgan", "Bella Morgan", "1996-08-09", "Female", "bella.morgan@example.com", "5550000128"),
        ("charlie_bell", "Charlie Bell", "1991-02-14", "Male", "charlie.bell@example.com", "5550000129"),
        ("diana_murphy", "Diana Murphy", "1994-11-23", "Female", "diana.murphy@example.com", "5550000130"),
    ]
    
    members = [
        Member(
            username=username,
            password_hash="password",
            name=name,
            dob=datetime.fromisoformat(dob),
            gender=gender,
            email=email,
            phone=phone,
        )
        for username, name, dob, gender, email, phone in member_data
    ]
    
    # 7 trainers with real names
    trainer_data = [
        ("trainer_sarah", "Sarah Thompson", "1985-05-12", "Female", "sarah.thompson@example.com", "5550000201"),
        ("trainer_michael", "Michael Chen", "1983-09-24", "Male", "michael.chen@example.com", "5550000202"),
        ("trainer_jessica", "Jessica Martinez", "1987-03-08", "Female", "jessica.martinez@example.com", "5550000203"),
        ("trainer_christopher", "Christopher Lee", "1984-11-19", "Male", "christopher.lee@example.com", "5550000204"),
        ("trainer_amanda", "Amanda Foster", "1986-07-15", "Female", "amanda.foster@example.com", "5550000205"),
        ("trainer_james", "James Bennett", "1982-01-30", "Male", "james.bennett@example.com", "5550000206"),
        ("trainer_rachel", "Rachel Stewart", "1988-06-22", "Female", "rachel.stewart@example.com", "5550000207"),
    ]
    
    trainers = [
        Trainer(
            username=username,
            password_hash="password",
            name=name,
            dob=datetime.fromisoformat(dob),
            gender=gender,
            email=email,
            phone=phone,
        )
        for username, name, dob, gender, email, phone in trainer_data
    ]
    
    # 2 administrators with real names
    administrators = [
        Administrator(
            username="admin_robert",
            password_hash="password",
            name="Robert Jenkins",
            dob=datetime(1980, 4, 10),
            gender="Male",
            email="robert.jenkins@example.com",
            phone="5550000301",
        ),
        Administrator(
            username="admin_patricia",
            password_hash="password",
            name="Patricia Hudson",
            dob=datetime(1982, 8, 18),
            gender="Female",
            email="patricia.hudson@example.com",
            phone="5550000302",
        ),
    ]
    
    # Check and add members
    existing_members = session.query(Member).all()
    if len(existing_members) == 0:
        session.add_all(members)
        session.commit()
        print(f"Added {len(members)} members")
    
    # Check and add trainers
    existing_trainers = session.query(Trainer).all()
    if len(existing_trainers) == 0:
        session.add_all(trainers)
        session.commit()
        print(f"Added {len(trainers)} trainers")
    
    # Check and add administrators
    existing_admins = session.query(Administrator).all()
    if len(existing_admins) == 0:
        session.add_all(administrators)
        session.commit()
        print(f"Added {len(administrators)} administrators")
