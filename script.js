// ================= API =================
const API_URL = "/data";

// 🔊 Alert Sound
const alertSound = new Audio("https://www.soundjay.com/buttons/beep-01a.mp3");

// ================= FETCH LOOP =================
async function fetchData() {
  try {
    const res = await fetch(API_URL);
    const data = await res.json();

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

    // ================= APPS WITH CHART =================
    let appSection = document.getElementById("apps");
    appSection.innerHTML = "";

    data.apps.forEach(app => {
      const chartId = `chart-${app.name.replace(/\s+/g, '-')}`;

      appSection.innerHTML += `
        <div class="col-md-6">
          <div class="card bg-secondary text-white p-3 mb-3">
            <h5>${app.name}</h5>
            <p>Permissions: ${app.permissions.join(", ")}</p>
            <p>Risk: ${app.risk}</p>
            <canvas id="${chartId}" height="100"></canvas>
            <button class="btn btn-danger btn-sm mt-2" onclick="revokeAccess('${app.name}')">Revoke</button>
          </div>
        </div>
      `;

      // Draw or update chart
      drawChart(chartId, data.risk_history[app.name]);
    });

  } catch (err) {
    console.error("Error:", err);
  }
}

// ================= CHARTS =================
const chartMap = {}; // store Chart.js instances

function drawChart(canvasId, history) {
  const ctx = document.getElementById(canvasId).getContext('2d');
  const labels = history.map(h => h.date);
  const data = history.map(h => h.risk);

  if (chartMap[canvasId]) {
    // Update existing chart
    chartMap[canvasId].data.labels = labels;
    chartMap[canvasId].data.datasets[0].data = data;
    chartMap[canvasId].update();
  } else {
    // Create new chart
    chartMap[canvasId] = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Risk Level',
          data: data,
          borderColor: appColor(canvasId),
          backgroundColor: 'rgba(255,255,255,0.1)',
          tension: 0.3,
          fill: true
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        scales: {
          y: { min: 0, max: 100 }
        },
        plugins: {
          legend: { display: false }
        }
      }
    });
  }
}

// Assign colors to apps
function appColor(canvasId) {
  if (canvasId.includes("Hushh-AI")) return "#22c55e"; // safe green
  return "#f59e0b"; // orange for other apps
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
