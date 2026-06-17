from flask import Blueprint,request,jsonify
from db import get_supabase
campaigns_bp=Blueprint("campaigns",__name__)
@campaigns_bp.route("/",methods=["GET"])
def list_campaigns():
    sb=get_supabase()
    return jsonify(sb.table("campaigns").select("*").execute().data)
@campaigns_bp.route("/",methods=["POST"])
def create_campaign():
    sb=get_supabase()
    data=request.json
    res=sb.table("campaigns").insert(data).execute()
    return jsonify(res.data[0])
@campaigns_bp.route("/<id>/pause",methods=["POST"])
def pause_campaign(id):
    sb=get_supabase()
    res=sb.table("campaigns").update({"status":"paused"}).eq("id",id).execute()
    return jsonify(res.data[0])
@campaigns_bp.route("/<id>/activate",methods=["POST"])
def activate_campaign(id):
    sb=get_supabase()
    res=sb.table("campaigns").update({"status":"active"}).eq("id",id).execute()
    return jsonify(res.data[0])
