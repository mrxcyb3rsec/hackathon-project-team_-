 from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import random
from datetime import datetime, timedelta

app = Flask(__name__, static_folder='.', static_url_path='')
CORS(app)

# ═══════════════════════════════════════════════════════════
# GLOBAL STATES
# ═══════════════════════════════════════════════════════════
simulation_mode = False

# Store risk history per app
risk_history = {}

# ═══════════════════════════════════════════════════════════
# DATA
# ═══════════════════════════════════════════════════════════
def load_data():
    return {
        "apps": [
            {"name": "Instagram", "permissions": ["Contacts", "Photos"], "risk": 70, "status": True},
            {"name": "Google Maps", "permissions": ["Location"], "risk": 50, "status": True},
            {"name": "Spotify", "permissions": ["Email"], "risk": 30, "status": True},
            {"name": "Shopping App", "permissions": ["Location", "Payment Info"], "risk": 80, "status": False},
            {"name": "Health App", "permissions": ["Health Data"], "risk": 55, "status": False},
            {"name": "Banking", "permissions": ["Financial Data"], "risk": 75, "status": False},
            {"name": "Hushh AI", "permissions": ["Secure Data"], "risk": 5, "status": True}  # TRUSTED
        ]
    }

# ═══════════════════════════════════════════════════════════
# INIT HISTORY
# ═══════════════════════════════════════════════════════════
def init_history(apps):
    global risk_history
    for app in apps:
        if app["name"] not in risk_history:
            risk_history[app["name"]] = []

# ═══════════════════════════════════════════════════════════
# UPDATE RISK HISTORY
# ═══════════════════════════════════════════════════════════
def update_risk(apps):
    global simulation_mode

    for app in apps:
        name = app["name"]

        # Hushh AI always safe
        if name == "Hushh AI":
            risk = 5
        else:
            if simulation_mode:
                risk = app["risk"] + random.randint(10, 25)
            else:
                risk = app["risk"] + random.randint(-5, 5)

        risk = max(0, min(100, risk))

        # Save history
        risk_history[name].append({
            "time": datetime.now().isoformat(),
            "risk": risk
        })

        # Update current risk
        app["risk"] = risk

# ═══════════════════════════════════════════════════════════
# FILTER HISTORY BY TIME
# ═══════════════════════════════════════════════════════════
def filter_history(app_name, range_type):
    now = datetime.now()

    if range_type == "day":
        cutoff = now - timedelta(days=1)
    elif range_type == "3days":
        cutoff = now - timedelta(days=3)
    elif range_type == "week":
        cutoff = now - timedelta(weeks=1)
    else:
        cutoff = now - timedelta(days=30)

    return [
        point for point in risk_history.get(app_name, [])
        if datetime.fromisoformat(point["time"]) >= cutoff
    ]

# ═══════════════════════════════════════════════════════════
# MAIN DASHBOARD API
# ═══════════════════════════════════════════════════════════
@app.route("/data")
def data():
    data = load_data()
    apps = data["apps"]

    init_history(apps)
    update_risk(apps)

    avg_risk = sum(a["risk"] for a in apps) // len(apps)

    if avg_risk < 50:
        status = "SAFE"
    elif avg_risk < 80:
        status = "WARNING"
    else:
        status = "DANGER"

    return jsonify({
        "apps": apps,
        "risk_score": avg_risk,
        "status": status
    })

# ═══════════════════════════════════════════════════════════
# APP DETAIL PAGE DATA
# ═══════════════════════════════════════════════════════════
@app.route("/app/<app_name>")
def app_page(app_name):
    return send_from_directory(".", "app.html")

# API for graph data
@app.route("/app/<app_name>/data")
def app_data(app_name):
    range_type = "day"
    history = filter_history(app_name, range_type)

    return jsonify({
        "app": app_name,
        "history": history
    })

# API for timeline switch
@app.route("/app/<app_name>/history/<range_type>")
def app_history(app_name, range_type):
    history = filter_history(app_name, range_type)

    return jsonify({
        "app": app_name,
        "range": range_type,
        "history": history
    })

# ═══════════════════════════════════════════════════════════
# SIMULATION MODE
# ═══════════════════════════════════════════════════════════
@app.route("/simulate")
def simulate():
    global simulation_mode
    simulation_mode = True
    return jsonify({"message": "🚨 Attack Simulation Started"})

# ═══════════════════════════════════════════════════════════
# RESET
# ═══════════════════════════════════════════════════════════
@app.route("/reset")
def reset():
    global simulation_mode, risk_history
    simulation_mode = False
    risk_history = {}
    return jsonify({"message": "System Reset"})

# ═══════════════════════════════════════════════════════════
# STATIC FILES
# ═══════════════════════════════════════════════════════════
@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/app.html")
def app_html():
    return send_from_directory(".", "app.html")

@app.route("/<path:path>")
def static_files(path):
    return send_from_directory(".", path)

# ═══════════════════════════════════════════════════════════
# RUN
# ═══════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("🚀 Hushh AI Dashboard Running...")
    app.run(host="0.0.0.0", port=5000, debug=True)
