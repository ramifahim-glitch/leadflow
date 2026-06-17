from flask import Blueprint,request,jsonify
from db import get_supabase
leads_bp=Blueprint("leads",__name__)
@leads_bp.route("/",methods=["GET"])
def list_leads():
    sb=get_supabase()
    return jsonify(sb.table("leads").select("*").limit(100).execute().data)
@leads_bp.route("/source/apollo",methods=["POST"])
def source_apollo():
    return jsonify({"leads":[]})
@leads_bp.route("/enrich/<id>",methods=["POST"])
def enrich_lead(id):
    return jsonify({"status":"enriched"})
@leads_bp.route("/<id>",methods=["PATCH"])
def update_lead(id):
    sb=get_supabase()
    data=request.json
    res=sb.table("leads").update(data).eq("id",id).execute()
    return jsonify(res.data[0])
