import sys
from pathlib import Path
from sqlalchemy import DDL, event

# Add project root so models.base is importable
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.base import Base

create_schedule_view_ddl = DDL(
    """
    CREATE OR REPLACE VIEW schedule AS
    SELECT
      COALESCE(c.id, -1)       AS event_id,
      c.id                     AS class_id,
      NULL::integer            AS session_id,
      c.room_id                AS room_id,
      c.start_time,
      c.end_time,
      c.trainer_id,
      'class'                  AS schedule_type
    FROM classes c
    UNION ALL
    SELECT
      COALESCE(s.id, -1)       AS event_id,
      NULL::integer            AS class_id,
      s.id                     AS session_id,
      s.room_id                AS room_id,
      s.start_time,
      s.end_time,
      s.trainer_id,
      'session'                AS schedule_type
    FROM sessions s;
    """
)

drop_schedule_view_ddl = DDL("DROP VIEW IF EXISTS schedule;")

# attach listeners so the view is created after tables and dropped before tables
event.listen(Base.metadata, "after_create", create_schedule_view_ddl.execute_if(dialect="postgresql"))
event.listen(Base.metadata, "before_drop", drop_schedule_view_ddl.execute_if(dialect="postgresql"))