import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

from routes.brain import brain_bp
from routes.campaigns import campaigns_bp
from routes.connectors import connectors_bp
from routes.leads import leads_bp
from routes.nurture import nurture_bp
from routes.outreach import outreach_bp
from routes.reports import reports_bp


def create_app():
    app = Flask(__name__)
    CORS(app, origins=os.getenv("FRONTEND_URL", "*"))

    app.register_blueprint(brain_bp, url_prefix="/api/brain")
    app.register_blueprint(campaigns_bp, url_prefix="/api/campaigns")
    app.register_blueprint(connectors_bp, url_prefix="/api/connectors")
    app.register_blueprint(leads_bp, url_prefix="/api/leads")
    app.register_blueprint(nurture_bp, url_prefix="/api/nurture")
    app.register_blueprint(outreach_bp, url_prefix="/api/outreach")
    app.register_blueprint(reports_bp, url_prefix="/api/reports")

    @app.route("/api/health")
    def health():
        return jsonify({"status": "ok"})

    if os.getenv("ENVIRONMENT") == "production":
        from jobs.daily_sourcing import run_daily_sourcing
        from jobs.sequence_engine import run_sequence_engine
        from jobs.branching_engine import run_branching_engine
        from jobs.nurture_runner import run_nurture_runner
        from jobs.learning_cycle import run_learning_cycle

        scheduler = BackgroundScheduler()
        scheduler.add_job(lambda: run_daily_sourcing(app), "cron", hour=7)
        scheduler.add_job(lambda: run_sequence_engine(app), "interval", hours=1)
        scheduler.add_job(lambda: run_branching_engine(app), "interval", minutes=30)
        scheduler.add_job(lambda: run_nurture_runner(app), "cron", hour=8)
        scheduler.add_job(lambda: run_learning_cycle(app), "interval", days=14)
        scheduler.start()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
