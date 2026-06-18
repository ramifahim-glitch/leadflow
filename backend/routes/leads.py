from flask import Blueprint, request, jsonify
from db import get_supabase
from hubspot_sync import sync_lead
from clay_sync import push_lead_for_enrichment

leads_bp = Blueprint("leads", __name__)


@leads_bp.route("/", methods=["GET"])
def list_leads():
    sb = get_supabase()
    return jsonify(sb.table("leads").select("*").limit(100).execute().data)


@leads_bp.route("/source/apollo", methods=["POST"])
def source_apollo():
    return jsonify({"leads": []})


@leads_bp.route("/enrich/<id>", methods=["POST"])
def enrich_lead(id):
    sb = get_supabase()
    res = sb.table("leads").select("*").eq("id", id).execute()
    if not res.data:
        return jsonify({"error": "lead not found"}), 404

    lead = res.data[0]
    result = push_lead_for_enrichment(lead)

    if result.get("pushed"):
        return jsonify({"status": "enrichment_requested"})
    return jsonify({"status": "enrichment_skipped", "reason": result})


@leads_bp.route("/<id>", methods=["PATCH"])
def update_lead(id):
    sb = get_supabase()
    data = request.json
    res = sb.table("leads").update(data).eq("id", id).execute()
    updated_lead = res.data[0]

    # Real-time one-way sync to HubSpot on every status change.
    # Safe no-op if HUBSPOT_API_KEY isn't set; never blocks the response on failure.
    if "status" in data:
        try:
            sync_lead(updated_lead)
        except Exception as e:
            print(f"[leads.update_lead] HubSpot sync failed: {e}")

    return jsonify(updated_lead)
