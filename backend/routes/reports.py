from flask import Blueprint,jsonify
from db import get_supabase
reports_bp=Blueprint("reports",__name__)
@reports_bp.route("/today",methods=["GET"])
def today():
    sb=get_supabase()
    res=sb.table("daily_reports").select("*").order("report_date",desc=True).limit(1).execute().data
    return jsonify(res[0] if res else {})
@reports_bp.route("/activity",methods=["GET"])
def activity():
    return jsonify([])
@reports_bp.route("/hot-replies",methods=["GET"])
def hot_replies():
    sb=get_supabase()
    return jsonify(sb.table("leads").select("*").eq("status","hot").execute().data)
