import os,json
from flask import Blueprint,request,jsonify
import anthropic
brain_bp=Blueprint("brain",__name__)
client=anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
@brain_bp.route("/analyse",methods=["POST"])
def analyse():
    data=request.json
    prompt=f"Analyse this business and return JSON with personas, value_props, buying_signals: Offering: {data.get('offering')}"
    resp=client.messages.create(model="claude-sonnet-4-6",max_tokens=2000,messages=[{"role":"user","content":prompt}])
    try:
        result=json.loads(resp.content[0].text)
    except:
        result={}
    return jsonify(result)
@brain_bp.route("/score-lead",methods=["POST"])
def score_lead():
    return jsonify({"fit_score":75})
@brain_bp.route("/personalise",methods=["POST"])
def personalise():
    return jsonify({"first_line":""})
@brain_bp.route("/classify-reply",methods=["POST"])
def classify_reply():
    return jsonify({"sentiment":"neutral"})
