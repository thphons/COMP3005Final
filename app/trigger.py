import sys
from pathlib import Path
from sqlalchemy import text

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def create_room_conflict_trigger(session):
    """Create trigger to prevent room conflicts"""
    trigger_sql = """
    CREATE OR REPLACE FUNCTION check_room_conflict()
    RETURNS TRIGGER AS $$
    BEGIN
      IF EXISTS (
        SELECT 1 FROM classes 
        WHERE room_id = NEW.room_id
        AND (
          (NEW.start_time < end_time AND NEW.end_time > start_time)
        )
      ) OR EXISTS (
        SELECT 1 FROM sessions
        WHERE room_id = NEW.room_id
        AND (
          (NEW.start_time < end_time AND NEW.end_time > start_time)
        )
      ) THEN
        RAISE EXCEPTION 'Room % is already booked during this time', NEW.room_id;
      END IF;
      RETURN NEW;
    END;
    $$ LANGUAGE plpgsql;

    DROP TRIGGER IF EXISTS prevent_class_room_conflict ON classes;
    CREATE TRIGGER prevent_class_room_conflict
    BEFORE INSERT OR UPDATE ON classes
    FOR EACH ROW
    EXECUTE FUNCTION check_room_conflict();

    DROP TRIGGER IF EXISTS prevent_session_room_conflict ON sessions;
    CREATE TRIGGER prevent_session_room_conflict
    BEFORE INSERT OR UPDATE ON sessions
    FOR EACH ROW
    EXECUTE FUNCTION check_room_conflict();
    """
    
    try:
        session.execute(text(trigger_sql))
        session.commit()
        print("Created room conflict prevention triggers")
    except Exception as e:
        print(f"Triggers already exist: {e}")