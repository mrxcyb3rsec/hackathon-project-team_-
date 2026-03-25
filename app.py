from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

def load_data():
    return {
        "apps": [
            {"name": "Instagram", "permissions": ["Contacts", "Photos"], "risk": "High", "last_accessed": "2 hours ago"},
            {"name": "Google Maps", "permissions": ["Location"], "risk": "Medium", "last_accessed": "10 minutes ago"},
            {"name": "Spotify", "permissions": ["Email"], "risk": "Low", "last_accessed": "1 day ago"},
            {"name": "Shopping App", "permissions": ["Location", "Payment Info"], "risk": "High", "last_accessed": "5 hours ago"}
        ]
    }

def calculate_score(apps):
    score = 100
    for app in apps:
        if app["risk"] == "High":
            score -= 15
        elif app["risk"] == "Medium":
            score -= 8
    return max(score, 0)

def generate_alerts(apps):
    alerts = []

    high_risk = [a for a in apps if a["risk"] == "High"]
    if len(high_risk) > 1:
        alerts.append("⚠️ Multiple high-risk apps connected")

    for app in apps:
        if "Location" in app["permissions"]:
            alerts.append(f"📍 {app['name']} is accessing your location")

    return alerts


# 🔹 API
@app.route("/data")
def data():
    data = load_data()
    apps = data["apps"]

    return jsonify({
        "trust_score": calculate_score(apps),
        "apps": apps,
        "alerts": generate_alerts(apps)
    })


# 🔥 SERVE FRONTEND (THIS IS THE FIX)
@app.route("/")
def serve_index():
    return send_from_directory(".", "index.html")


# 🔥 OPTIONAL (for CSS + JS)
@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
