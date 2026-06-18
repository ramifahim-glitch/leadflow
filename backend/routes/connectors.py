from flask import Blueprint, request, jsonify
import os
from clay_sync import handle_enrichment_callback

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


@connectors_bp.route("/inboxes", methods=["GET"])
def inboxes():
    from db import get_supabase
    sb = get_supabase()
    return jsonify(sb.table("inboxes").select("*").execute().data)


@connectors_bp.route("/maildoso/create", methods=["POST"])
def create_inboxes():
    data = request.json
    return jsonify({"status": "queued", "count": data.get("count", 5)})


@connectors_bp.route("/clay/webhook", methods=["POST"])
def clay_webhook():
    """
    Receives the enriched row back from Clay once the '@ Work Email'
    column resolves (configured as a 'Send to Webhook' export on the Clay table).
    """
    payload = request.json or {}
    result = handle_enrichment_callback(payload)
    return jsonify(result)
