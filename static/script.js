// ===== TRUST SCORE CALCULATION =====
function calculateTrustScore() {
    let apps = document.querySelectorAll(".app-card");
    let riskyApps = 0;

    apps.forEach(app => {
        let risk = app.getAttribute("data-risk");
        if (risk === "high") {
            riskyApps++;
        }
    });

    let score = 100 - (riskyApps * 15);

    if (score < 0) score = 0;

    document.getElementById("score").innerText = score + "%";
}

// ===== REVOKE ACCESS FUNCTION =====
function revokeAccess(button) {
    let card = button.parentElement;

    // Remove the app card
    card.remove();

    alert("Access revoked successfully!");

    // Recalculate score after removal
    calculateTrustScore();
}

// ===== ALERT SYSTEM =====
function checkAlerts() {
    let apps = document.querySelectorAll(".app-card");
    let alertBox = document.getElementById("alerts");

    if (!alertBox) return;

    if (apps.length > 4) {
        alertBox.innerHTML = "⚠️ You have many apps connected. Review permissions!";
    } else {
        alertBox.innerHTML = "✅ Your data is under control.";
    }
}

// ===== RUN WHEN PAGE LOADS =====
window.onload = function () {
    calculateTrustScore();
    checkAlerts();
};
