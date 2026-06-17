from flask import Blueprint,request,jsonify
outreach_bp=Blueprint("outreach",__name__)
@outreach_bp.route("/send-email",methods=["POST"])
def send_email():
    return jsonify({"status":"queued"})
@outreach_bp.route("/send-linkedin",methods=["POST"])
def send_linkedin():
    return jsonify({"status":"queued"})
@outreach_bp.route("/reply-webhook",methods=["POST"])
def reply_weblook():
    return jsonify({"status":"received"})
