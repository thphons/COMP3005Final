import sys
from pathlib import Path
from datetime import datetime, timedelta

# Add parent directory to path so models is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import models with proper paths
from models.member import Member
from models.admin import Administrator
from models.trainer import Trainer
from models.room import Room
from models.health_metric import Health_Metric
from models.base import Base


def reset(engine):
    Base.metadata.drop_all(engine)


def createInitialRecords(session):

    # 150 unique members with real names
    member_names = [
        "Alice Smith", "Bob Johnson", "Carol Williams", "David Brown", "Emma Davis",
        "Frank Miller", "Grace Wilson", "Henry Moore", "Iris Taylor", "Jack Anderson",
        "Karen Thomas", "Liam Jackson", "Mia White", "Noah Harris", "Olivia Martin",
        "Peter Garcia", "Quinn Rodriguez", "Ryan Martinez", "Sophie Hernandez", "Thomas Lopez",
        "Uma Gonzalez", "Victor Perez", "Wendy Sanchez", "Xavier Morris", "Yara Rogers",
        "Zoe Reed", "Adam Cook", "Bella Morgan", "Charlie Bell", "Diana Murphy",
        "Ethan Foster", "Fiona Green", "George Hall", "Hannah Hill", "Isaac Jones",
        "Julia King", "Kevin Knight", "Laura Lewis", "Mason Lopez", "Nora Martinez",
        "Oscar Miller", "Piper Moore", "Quinn Nelson", "Rachel Oliver", "Samuel Parker",
        "Tina Peterson", "Ulysses Phillips", "Violet Price", "William Ramirez", "Xena Reed",
        "Yolanda Reynolds", "Zachary Richardson", "Amber Roberts", "Brandon Rodriguez", "Chloe Rogers",
        "Derek Ross", "Elena Russell", "Felix Ryan", "Gina Sanchez", "Hunter Sanders",
        "Ivy Scott", "Jack Sharp", "Kayla Shaw", "Levi Shelton", "Megan Short",
        "Nathan Silva", "Olivia Simpson", "Parker Simmons", "Quinn Smith", "Riley Snyder",
        "Samantha Solis", "Tristan Sparks", "Uma Spears", "Vincent Spencer", "Willa Stacks",
        "Xander Stafford", "Yara Stahl", "Zeke Stanton", "Alice Stark", "Benjamin Stearns",
        "Charlotte Steele", "Daniel Stein", "Evelyn Stephens", "Ethan Stevens", "Fiona Stewart",
        "Gabriel Stokes", "Hannah Stone", "Henry Stout", "Iris Strickland", "Jack Strong",
        "Kayla Stuart", "Liam Stubbs", "Mia Studley", "Noah Sturm", "Olivia Styles",
        "Parker Suarez", "Quinn Summers", "Rachel Summerville", "Samuel Summers", "Tina Sumner",
        "Ulysses Sundberg", "Violet Sunkel", "William Sunner", "Xena Suplee", "Yolanda Swain",
        "Zachary Swam", "Amber Swan", "Brandon Swank", "Chloe Swanson", "Derek Swart",
        "Elena Swartz", "Felix Sweat", "Gina Sweatt", "Hunter Sweeney", "Ivy Sweeney",
        "Jack Sweet", "Kayla Sweetland", "Levi Sweterlitsch", "Megan Swetland", "Nathan Swick",
        "Olivia Swift", "Parker Swindell", "Quinn Swingle", "Riley Swinton", "Samantha Swisher",
        "Tristan Swisshelm", "Uma Swords", "Vincent Swyhart", "Willa Sybert", "Xander Sykes",
        "Yara Sykes", "Zeke Sylk", "Alice Syllabus", "Benjamin Sylvester", "Charlotte Symmes",
        "Daniel Symons", "Evelyn Symson", "Ethan Sypher", "Fiona Syracuse", "Gabriel Syre",
        "Hannah Syrett", "Henry Sysyn", "Iris Syverson", "Jack Syvrud", "Kayla Syzslak",
    ]
    
    member_data = [
        (f"member_{i}", name, f"198{i % 10}-{(i % 12) + 1:02d}-{(i % 28) + 1:02d}", 
         ["Male", "Female"][i % 2], f"member{i}@example.com", f"555000{i:04d}")
        for i, name in enumerate(member_names, 1)
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

    # Add a goal for the first member
    
    # Add 10 health metrics for the first member
    first_member = session.query(Member).first()
    if first_member:
        existing_metrics = session.query(Health_Metric).filter(Health_Metric.user_id == first_member.id).all()
        if len(existing_metrics) == 0:
            base_date = datetime.now() - timedelta(days=9)
            health_metrics = [
                Health_Metric(
                    date = base_date + timedelta(days=i),
                    record_type = 'record',
                    user_id= first_member.id,
                    weight = 80.5 - (i * 0.5),
                    height = 170,
                    vo2Max = 70 - i,
                    body_composition = 30 - i,
                    resting_hr = 70 - i,
                )
                for i in range(10)
            ]
            session.add_all(health_metrics)
            session.commit()
            print(f"Added 10 health metrics for member {first_member.name}")

            # Add a goal for the first member
            newGoal = Health_Metric(
                date = "2025-12-01",
                record_type = 'goal',
                user_id= first_member.id,
                weight = 70,
                height = 170,
                vo2Max = 60,
                body_composition = 20,
                resting_hr = 60,
            )

            session.add(newGoal)
            session.commit()
            print(f"Added a goal for member {first_member.name}")

    #add 3 rooms
    new_rooms = [
        Room(
            room_number = 101,
        ),
        Room(
            room_number = 102,
        ),
        Room(
            room_number = 103,
        )
    ]
    existing_rooms = session.query(Room).all()
    if len(existing_rooms) == 0:
        session.add_all(new_rooms)
        session.commit()
        print(f"Added {len(new_rooms)} rooms")

        
