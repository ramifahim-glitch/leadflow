from db import get_supabase
def run_learning_cycle(app):
    """Runs every 14 days. Analyses results and adjusts signal weights."""
    with app.app_context():
        sb=get_supabase()
        campaigns=sb.table("campaigns").select("id").execute().data
        for c in campaigns:
            print(f"[learning_cycle] Analysing campaign {c['id']}")
