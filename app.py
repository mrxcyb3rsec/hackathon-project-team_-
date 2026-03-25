from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# 🔹 Load fake data
def load_data():
    return {
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


# 🔹 Calculate Trust Score dynamically
def calculate_score(apps):
    score = 100
    for app in apps:
        if app["risk"] == "High":
            score -= 15
        elif app["risk"] == "Medium":
            score -= 8
    return max(score, 0)


# 🔹 Generate alerts
def generate_alerts(apps):
    alerts = []

    high_risk_apps = [app for app in apps if app["risk"] == "High"]

    if len(high_risk_apps) > 1:
        alerts.append("⚠️ Multiple high-risk apps connected")

    for app in apps:
        if "Location" in app["permissions"]:
            alerts.append(f"📍 {app['name']} is accessing your location")

    return alerts


# 🔹 API route
@app.route("/data", methods=["GET"])
def get_data():
    data = load_data()
    apps = data["apps"]

    score = calculate_score(apps)
    alerts = generate_alerts(apps)

    return jsonify({
        "trust_score": score,
        "apps": apps,
        "alerts": alerts
    })


# 🔹 Home route (fixes "Cannot GET /")
@app.route("/")
def home():
    return "🚀 Trust Dashboard Backend Running Successfully!"


# 🔥 IMPORTANT FOR GITHUB CODESPACES
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
