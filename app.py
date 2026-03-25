from flask import Flask, jsonify
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Load fake data
def load_data():
    data = {
        "trust_score": 78,
        "apps": [
            {
                "name": "Instagram",
                "permissions": ["Contacts", "Photos"],
                "risk": "High",
                "last_accessed": "2 hours ago"
            },
            {
                "name": "Google Maps",
                "permissions": ["Location"],
                "risk": "Medium",
                "last_accessed": "10 minutes ago"
            },
            {
                "name": "Spotify",
                "permissions": ["Email"],
                "risk": "Low",
                "last_accessed": "1 day ago"
            },
            {
                "name": "Shopping App",
                "permissions": ["Location", "Payment Info"],
                "risk": "High",
                "last_accessed": "5 hours ago"
            }
        ]
    }
    return data


# Generate alerts
def generate_alerts(data):
    alerts = []
    
    high_risk_apps = [app for app in data["apps"] if app["risk"] == "High"]

    if len(high_risk_apps) > 1:
        alerts.append("⚠️ Multiple high-risk apps connected")

    for app in data["apps"]:
        if "Location" in app["permissions"]:
            alerts.append(f"📍 {app['name']} is accessing your location")

    return alerts


@app.route("/data", methods=["GET"])
def get_data():
    data = load_data()
    alerts = generate_alerts(data)

    response = {
        "trust_score": data["trust_score"],
        "apps": data["apps"],
        "alerts": alerts
    }

    return jsonify(response)


@app.route("/")
def home():
    return "Trust Dashboard Backend Running!"


if __name__ == "__main__":
    app.run(debug=True)
