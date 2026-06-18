from flask import Blueprint, request, jsonify
import os
connectors_bp = Blueprint("connectors", __name__)

@connectors_bp.route("/status", methods=["GET"])
def status():
    keys = {
        "clay": "CLAY_API_KEY",
        "maildoso": "MAILDOSO_API_KEY",
        "instantly": "INSTANTLY_API_KEY",
        "apollo": "APOLLO_API_KEY",
        "apify": "APIFY_API_KEY",
        "hubspot": "HUBSPOT_API_KEY",
        "heyreach": "HEYREACH_API_KEY",
        "anthropic": "ANTHROPIC_API_KEY",
        "supabase": "SUPABASE_URL",
        "slack": "SLACK_WEBHOOK_URL",
    }
    connectors = {k: bool(os.getenv(v)) for k, v in keys.items()}
    return jsonify({"connectors": connectors})

@connectors_bp.route("/debug", methods=["GET"])
def debug():
    raw_url = os.getenv("SUPABASE_URL")
    raw_key = os.getenv("SUPABASE_SERVICE_KEY")
    return jsonify({
        "SUPABASE_URL_present": raw_url is not None,
        "SUPABASE_URL_value": raw_url,
        "SUPABASE_URL_len": len(raw_url) if raw_url else 0,
        "SUPABASE_SERVICE_KEY_present": raw_key is not None,
        "SUPABASE_SERVICE_KEY_len": len(raw_key) if raw_key else 0,
        "all_env_keys_containing_SUPABASE": [k for k in os.environ.keys() if "SUPABASE" in k.upper()],
    })

@connectors_bp.route("/inboxes", methods=["GET"])
def inboxes():
    from db import get_supabase
    sb = get_supabase()
    return jsonify(sb.table("inboxes").select("*").execute().data)

@connectors_bp.route("/maildoso/create", methods=["POST"])
def create_inboxes():
    data = request.json
    return jsonify({"status": "queued", "count": data.get("count", 5)})
