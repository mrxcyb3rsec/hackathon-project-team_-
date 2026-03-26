// ================= API =================
const API_URL = "/data";

// 🔊 Alert Sound
const alertSound = new Audio("https://www.soundjay.com/buttons/beep-01a.mp3");

// ================= FETCH LOOP =================
async function fetchData() {
  try {
    const res = await fetch(API_URL);
    const data = await res.json();

    console.log(data);

    // ================= TRUST + RISK =================
    document.getElementById("score").innerText = data.trust_score + "%";
    document.getElementById("risk").innerText = data.risk_score + "%";
    document.getElementById("status").innerText = data.status;

    // ================= STATUS COLOR =================
    const statusEl = document.getElementById("status");
    const body = document.getElementById("body");

    if (data.status === "DANGER") {
      statusEl.className = "text-danger";
      body.style.background = "#2b0000";
      alertSound.play();
    } else if (data.status === "WARNING") {
      statusEl.className = "text-warning";
      body.style.background = "#2b2b00";
    } else {
      statusEl.className = "text-success";
      body.style.background = "#001f1f";
    }

    // ================= ALERTS =================
    let alertBox = document.getElementById("alerts");
    alertBox.innerHTML = "";

    data.alerts.forEach(alert => {
      alertBox.innerHTML += `<div class="alert alert-warning">${alert}</div>`;
    });

    // ================= AI EXPLANATION =================
    let reasonsList = document.getElementById("reasons");
    reasonsList.innerHTML = "";

    data.reasons.forEach(r => {
      reasonsList.innerHTML += `<li class="list-group-item bg-dark text-white">${r}</li>`;
    });

    // ================= ACTION =================
    document.getElementById("action").innerText = data.action;

    // ================= APPS =================
    let appSection = document.getElementById("apps");
    appSection.innerHTML = "";

    data.apps.forEach(app => {
      appSection.innerHTML += `
        <div class="col-md-4">
          <div class="card bg-secondary text-white p-3 mb-3">
            <h5>${app.name}</h5>
            <p>Permissions: ${app.permissions.join(", ")}</p>
            <p>Risk: ${app.risk}</p>
            <button class="btn btn-danger btn-sm" onclick="revokeAccess('${app.name}')">Revoke</button>
          </div>
        </div>
      `;
    });

  } catch (err) {
    console.error("Error:", err);
  }
}

// 🔁 AUTO REFRESH EVERY 2 SEC
setInterval(fetchData, 2000);
fetchData();


// ================= SIMULATION =================
function simulate() {
  fetch("/simulate");
}

// ================= RESET =================
function resetSystem() {
  fetch("/reset");
}


// ================= AI CHAT =================
function askAI() {
  let q = document.getElementById("question").value.toLowerCase();
  let answer = "🤖 Analyzing...";

  if (q.includes("why")) {
    answer = "Risk increased due to unusual app behavior and high-risk permissions.";
  } 
  else if (q.includes("safe")) {
    answer = "System is currently stable with low anomaly detection.";
  } 
  else if (q.includes("risk")) {
    answer = "Risk score is calculated dynamically based on app behavior patterns.";
  } 
  else {
    answer = "Try asking: 'Why risk?', 'Is it safe?', 'What happened?'";
  }

  document.getElementById("answer").innerText = answer;
}


// ================= ACTION =================
function revokeAccess(appName) {
  alert("🚫 " + appName + " access revoked!");
}
