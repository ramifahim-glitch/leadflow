from datetime import datetime,timezone
from db import get_supabase
def run_nurture_runner(app):
    """Runs 8am daily. Fires due nurture touches."""
    with app.app_context():
        sb=get_supabase()
        now=datetime.now(timezone.utc).isoformat()
        due=sb.table("nurture_enrolments").select("*").eq("status","active").lte("next_touch_at",now).execute().data
        for e in due:
            print(f"[nurture_runner] Touching enrollment {e['id']}")
