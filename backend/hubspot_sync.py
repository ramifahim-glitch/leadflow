"""
HubSpot one-way sync: pushes lead status changes from Supabase into HubSpot as contacts.
Supabase remains the source of truth; HubSpot is a read-only mirror for the sales team.
Fails silently (logs only) so a HubSpot outage never blocks LeadFlow's own operations.
"""
import os
import requests

HUBSPOT_BASE = "https://api.hubapi.com"


def _headers():
    key = os.getenv("HUBSPOT_API_KEY")
    if not key:
        return None
    return {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}


def _find_contact_by_email(email):
    headers = _headers()
    if not headers or not email:
        return None
    try:
        resp = requests.post(
            f"{HUBSPOT_BASE}/crm/v3/objects/contacts/search",
            headers=headers,
            json={
                "filterGroups": [
                    {"filters": [{"propertyName": "email", "operator": "EQ", "value": email}]}
                ],
                "limit": 1,
            },
            timeout=10,
        )
        results = resp.json().get("results", [])
        return results[0]["id"] if results else None
    except Exception as e:
        print(f"[hubspot_sync] lookup failed: {e}")
        return None


def sync_lead(lead):
    """
    Push a single lead dict (as stored in Supabase 'leads' table) into HubSpot.
    Creates the contact if it doesn't exist, otherwise updates it.
    Safe to call on every status change — no-ops cleanly if HUBSPOT_API_KEY is unset.
    """
    headers = _headers()
    if not headers:
        return {"skipped": "no_hubspot_key"}

    email = lead.get("email")
    if not email:
        return {"skipped": "no_email"}

    properties = {
        "email": email,
        "firstname": lead.get("first_name", ""),
        "lastname": lead.get("last_name", ""),
        "company": lead.get("company", ""),
        "jobtitle": lead.get("title", ""),
        "leadflow_status": lead.get("status", ""),
        "leadflow_fit_score": str(lead.get("fit_score", "")),
    }

    try:
        contact_id = _find_contact_by_email(email)
        if contact_id:
            resp = requests.patch(
                f"{HUBSPOT_BASE}/crm/v3/objects/contacts/{contact_id}",
                headers=headers,
                json={"properties": properties},
                timeout=10,
            )
        else:
            resp = requests.post(
                f"{HUBSPOT_BASE}/crm/v3/objects/contacts",
                headers=headers,
                json={"properties": properties},
                timeout=10,
            )
        if resp.status_code >= 400:
            print(f"[hubspot_sync] HubSpot returned {resp.status_code}: {resp.text}")
            return {"error": resp.status_code}
        return {"synced": True}
    except Exception as e:
        print(f"[hubspot_sync] sync failed: {e}")
        return {"error": str(e)}


def log_activity_note(lead, note_text):
    """
    Attach a timeline note to a contact (e.g. 'Replied positively', 'Hot lead — assigned to rep').
    Best-effort — silently skips if the contact can't be found or HubSpot isn't configured.
    """
    headers = _headers()
    if not headers:
        return {"skipped": "no_hubspot_key"}

    email = lead.get("email")
    contact_id = _find_contact_by_email(email)
    if not contact_id:
        return {"skipped": "contact_not_found"}

    try:
        resp = requests.post(
            f"{HUBSPOT_BASE}/crm/v3/objects/notes",
            headers=headers,
            json={
                "properties": {"hs_note_body": note_text},
                "associations": [
                    {
                        "to": {"id": contact_id},
                        "types": [
                            {
                                "associationCategory": "HUBSPOT_DEFINED",
                                "associationTypeId": 202,
                            }
                        ],
                    }
                ],
            },
            timeout=10,
        )
        return {"logged": resp.status_code < 400}
    except Exception as e:
        print(f"[hubspot_sync] note logging failed: {e}")
        return {"error": str(e)}
