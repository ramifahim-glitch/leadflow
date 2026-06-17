import requests
from db import get_supabase
def run_daily_sourcing(app):
    """Runs 7am daily. Sources leads for all active campaigns via Apollo."""
    with app.app_context():
        sb=get_supabase()
        campaigns=sb.table("campaigns").select("*").eq("status","active").execute().data
        for c in campaigns:
            print(f"[daily_sourcing] Campaign {c['id']}: sourcing leads...")
