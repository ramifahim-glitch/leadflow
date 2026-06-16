import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
load_dotenv()
from routes.campaigns import campaigns_bp
from routes.nurture import nurture_bp
def create_app():
    app = Flask(__name__)
    return app
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
