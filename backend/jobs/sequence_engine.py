from datetime import datetime,timezone
from db import get_supabase
def run_sequence_engine(app):
    """Runs hourly. Fires due sequence steps (email/linkedin)."""
    with app.app_context():
        sb=get_supabase()
        now=datetime.now(timezone.utc).isoformat()
        due=sb.table("sequence_enrolments").select("*").eq("status","active").lte("next_step_at",now).execute().data
        for e in due:
            print(f"[sequence_engine] Firing step for enrolment {e['id']}")
