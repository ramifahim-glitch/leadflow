"""Branching rules engine - runs every 30 min. Evaluates engagement signals and fires actions."""
import os,requests
from datetime import datetime,timezone
from db import get_supabase
SLACK_WEBHOOK=os.getenv("SLACK_WEBHOOK_URL")
def run_branching_engine(app):
    with app.app_context():
        sb=get_supabase()
        active=sb.table("sequence_enrolments").select("*, leads(*)").eq("status","active").execute().data
        for e in active:
            try: _evaluate(sb,e)
            except Exception as ex: print(ex)
def _evaluate(sb,enrolment):
    lead_id=enrolment["lead_id"]
    rules=sb.table("branching_rules").select("*").eq("active",True).order("priority").execute().data
    logs=sb.table("outreach_log").select("*").eq("lead_id",lead_id).execute().data
    replied=any(l.get("replied_at") for l in logs)
    for rule in rules:
        if rule.get("trigger_event")=="replied_positive" and replied:
            sb.table("sequence_enrolments").update({"status":"paused"}).eq("id",enrolment["id"]).execute()
            sb.table("leads").update({"status":"hot"}).eq("id",lead_id).execute()
            if SLACK_WEBHOOK:
                requests.post(SLACK_WEBHOOK,json={"text":f"Hot reply for lead {lead_id}"})
            break
