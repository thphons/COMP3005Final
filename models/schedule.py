from sqlalchemy import DDL, event
from .base import Base
from .class_ import Class
from .session import Session

create_view = DDL("""
CREATE OR REPLACE VIEW schedule AS
SELECT 
    c.room_id,
    c.start_time,
    c.end_time,
    c.trainer_id,
    'class' as schedule_type
FROM classes c
UNION ALL
SELECT 
    s.room_id,
    s.start_time,
    s.end_time,
    s.trainer_id,
    'session' as schedule_type
FROM sessions s;
""")

drop_view = DDL("DROP VIEW IF EXISTS schedule;")

# create events for view
event.listen(Base.metadata, "after_create", create_view)
event.listen(Base.metadata, "before_drop", drop_view)