from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import random
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# ================= GLOBAL STATES =================
simulation_mode = False
dynamic_risk = 40

# Per-app risk history storage (last 30 days)
risk_history = {}

# ================= DATA =================
def load_data():
    global risk_history
    apps = [
        {"name": "Instagram", "permissions": ["Contacts", "Photos"], "risk": "High", "last_accessed": "2 hours ago"},
        {"name": "Google Maps", "permissions": ["Location"], "risk": "Medium", "last_accessed": "10 minutes ago"},
        {"name": "Spotify", "permissions": ["Email"], "risk": "Low", "last_accessed": "1 day ago"},
        {"name": "Shopping App", "permissions": ["Location", "Payment Info"], "risk": "High", "last_accessed": "5 hours ago"},
        {"name": "Hushh AI", "permissions": ["Internal"], "risk": "Low", "last_accessed": "Always Safe"}
    ]

    now = datetime.now()
    for app in apps:
        if app["name"] not in risk_history:
            history = []
            for i in range(30):
                day = now - timedelta(days=30 - i)
                value = 5 if app["name"] == "Hushh AI" else random.randint(10, 40)
                history.append({"date": day.strftime("%Y-%m-%d"), "risk": value})
            risk_history[app["name"]] = history

    return apps

# ================= TRUST SCORE =================
def calculate_score(apps):
    score = 100
    for app in apps:
        if app["risk"] == "High":
            score -= 15
        elif app["risk"] == "Medium":
            score -= 8
    return max(score, 0)

# ================= ALERT SYSTEM =================
def generate_alerts(apps):
    alerts = []
    high_risk = [a for a in apps if a["risk"] == "High"]
    if len(high_risk) > 1:
        alerts.append("⚠️ Multiple high-risk apps connected")
    for app in apps:
        if "Location" in app["permissions"]:
            alerts.append(f"📍 {app['name']} is accessing your location")
    return alerts

# ================= AI EXPLANATION =================
def generate_explanation(risk):
    reasons = []
    if risk > 50:
        reasons.append("Unusual app behavior detected")
    if risk > 65:
        reasons.append("Multiple high-risk permissions active")
    if risk > 80:
        reasons.append("Critical threat pattern identified")
    return reasons

# ================= AUTO RESPONSE =================
def auto_response(risk):
    if risk > 80:
        return "🔒 AUTO LOCK ACTIVATED"
    elif risk > 60:
        return "⚠️ RECOMMEND ENABLE MFA"
    else:
        return "✅ SYSTEM NORMAL"

# ================= UPDATE RISK HISTORY =================
def update_risk_history(apps, dynamic_risk_val):
    now = datetime.now().strftime("%Y-%m-%d")
    for app in apps:
        if app["name"] == "Hushh AI":
            risk = 5
        else:
            if simulation_mode:
                risk = min(100, random.randint(dynamic_risk_val, dynamic_risk_val + 15))
            else:
                risk = max(0, random.randint(dynamic_risk_val - 5, dynamic_risk_val + 10))
        risk_history[app["name"]].append({"date": now, "risk": risk})
        risk_history[app["name"]] = risk_history[app["name"]][-30:]
    return risk_history

# ================= MAIN API =================
@app.route("/data")
def data():
    global dynamic_risk, simulation_mode
    apps = load_data()
    trust_score = calculate_score(apps)

    # 🔥 Dynamic Risk Engine
    if simulation_mode:
        dynamic_risk += random.randint(15, 30)
    else:
        dynamic_risk += random.randint(-5, 10)
    dynamic_risk = max(0, min(100, dynamic_risk))

    # Update per-app risk history
    histories = update_risk_history(apps, dynamic_risk)

    return jsonify({
        "trust_score": trust_score,
        "risk_score": dynamic_risk,
        "status": "SAFE" if dynamic_risk < 50 else "WARNING" if dynamic_risk < 80 else "DANGER",
        "apps": apps,
        "alerts": generate_alerts(apps),
        "reasons": generate_explanation(dynamic_risk),
        "action": auto_response(dynamic_risk),
        "risk_history": histories
    })

# ================= SIMULATION MODE =================
@app.route("/simulate")
def simulate():
    global simulation_mode
    simulation_mode = True
    return jsonify({"message": "🚨 Attack Simulation Started"})

# ================= RESET =================
@app.route("/reset")
def reset():
    global simulation_mode, dynamic_risk, risk_history
    simulation_mode = False
    dynamic_risk = 40
    risk_history = {}
    return jsonify({"message": "System Reset"})

# ================= FRONTEND =================
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

# ================= RUN =================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
