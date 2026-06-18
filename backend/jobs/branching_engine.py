"""Branching rules engine - runs every 30 min. Evaluates engagement signals and fires actions."""
import os
import requests
from datetime import datetime, timezone
from db import get_supabase
from hubspot_sync import sync_lead, log_activity_note

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK_URL")


def run_branching_engine(app):
    with app.app_context():
        sb = get_supabase()
        active = (
            sb.table("sequence_enrolments")
            .select("*, leads(*)")
            .eq("status", "active")
            .execute()
            .data
        )
        for e in active:
            try:
                _evaluate(sb, e)
            except Exception as ex:
                print(ex)


def _evaluate(sb, enrolment):
    lead_id = enrolment["lead_id"]
    lead = enrolment.get("leads") or {}
    rules = (
        sb.table("branching_rules")
        .select("*")
        .eq("active", True)
        .order("priority")
        .execute()
        .data
    )
    logs = sb.table("outreach_log").select("*").eq("lead_id", lead_id).execute().data
    replied = any(l.get("replied_at") for l in logs)

    for rule in rules:
        trigger = rule.get("trigger_event")

        if trigger == "replied_positive" and replied:
            sb.table("sequence_enrolments").update({"status": "paused"}).eq(
                "id", enrolment["id"]
            ).execute()
            updated = (
                sb.table("leads")
                .update({"status": "hot"})
                .eq("id", lead_id)
                .execute()
                .data
            )
            hot_lead = updated[0] if updated else {**lead, "status": "hot"}

            # Real-time sync: push the hot lead to HubSpot and log the activity.
            try:
                sync_lead(hot_lead)
                log_activity_note(hot_lead, "Replied positively — marked as hot lead by LeadFlow")
            except Exception as ex:
                print(f"[branching_engine] HubSpot sync failed: {ex}")

            if SLACK_WEBHOOK:
                requests.post(SLACK_WEBHOOK, json={"text": f"Hot reply for lead {lead_id}"})
            break

        elif trigger == "replied_negative" and replied:
            sb.table("sequence_enrolments").update({"status": "removed"}).eq(
                "id", enrolment["id"]
            ).execute()
            updated = (
                sb.table("leads")
                .update({"status": "disqualified"})
                .eq("id", lead_id)
                .execute()
                .data
            )
            disq_lead = updated[0] if updated else {**lead, "status": "disqualified"}
            try:
                sync_lead(disq_lead)
            except Exception as ex:
                print(f"[branching_engine] HubSpot sync failed: {ex}")
            break
