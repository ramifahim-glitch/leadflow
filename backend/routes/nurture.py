from flask import Blueprint,request,jsonify
from db import get_supabase
nurture_bp=Blueprint("nurture",__name__)
@nurture_bp.route("/stats",methods=["GET"])
def stats():
    return jsonify({})
@nurture_bp.route("/tracks",methods=["GET"])
def tracks():
    sb=get_supabase()
    return jsonify(sb.table("nurture_tracks").select("*").execute().data)
@nurture_bp.route("/rules",methods=["GET"])
def rules():
    sb=get_supabase()
    return jsonify(sb.table("branching_rules").select("*").execute().data)
@nurture_bp.route("/enrolments",methods=["GET"])
def enrolments():
    sb=get_supabase()
    return jsonify(sb.table("sequence_enrolments").select("*").execute().data)
@nurture_bp.route("/enrol",methods=["POST"])
def enrol():
    return jsonify({})
