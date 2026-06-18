"""
Clay integration: pushes a lead's name + domain into a Clay webhook table to
trigger the email-finding enrichment. Clay does not offer a public REST API for
reading rows back — the only supported path is webhook in, webhook out.
So: we POST to CLAY_WEBHOOK_URL to push leads in, and we expose
/api/connectors/clay/webhook on our own backend (see routes/connectors.py) for
Clay's "Send to Webhook" export to call back into once enrichment finishes.
"""
import os
import requests


def push_lead_for_enrichment(lead):
    """
    Push a lead's name + domain into the Clay webhook table.
    Fire-and-forget: Clay processes asynchronously and will call back into
    our /clay/webhook endpoint once the '@ Work Email' column resolves.
    """
    webhook_url = os.getenv("CLAY_WEBHOOK_URL")
    if not webhook_url:
        return {"skipped": "no_clay_webhook_url"}

    name = f"{lead.get('first_name','')} {lead.get('last_name','')}".strip()
    domain = lead.get("company_domain") or lead.get("domain")
    if not name or not domain:
        return {"skipped": "missing_name_or_domain"}

    try:
        resp = requests.post(
            webhook_url,
            json={
                "Name": name,
                "Domain": domain,
                "lead_id": lead.get("id"),  # pass through so the callback can match it
            },
            timeout=10,
        )
        if resp.status_code >= 400:
            print(f"[clay_sync] push failed {resp.status_code}: {resp.text}")
            return {"error": resp.status_code}
        return {"pushed": True}
    except Exception as e:
        print(f"[clay_sync] push error: {e}")
        return {"error": str(e)}


def handle_enrichment_callback(payload):
    """
    Called by routes/connectors.py when Clay's "Send to Webhook" export fires
    after enrichment completes. Expects 'lead_id' (passed through on push)
    and the enriched email field, then writes it back into Supabase.
    """
    from db import get_supabase

    lead_id = payload.get("lead_id")
    email = payload.get("@ Work Email") or payload.get("email")
    if not lead_id or not email:
        return {"skipped": "missing_lead_id_or_email"}

    sb = get_supabase()
    res = sb.table("leads").update({"email": email}).eq("id", lead_id).execute()
    return {"updated": bool(res.data)}
