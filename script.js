const API_URL = "/data"; // 🔥 IMPORTANT

fetch(API_URL)
  .then(response => response.json())
  .then(data => {
    console.log(data);

    // Trust Score
    document.getElementById("score").innerText = data.trust_score + "%";

    // Alerts
    let alertBox = document.getElementById("alerts");
    alertBox.innerHTML = "";

    data.alerts.forEach(alert => {
      alertBox.innerHTML += `<div class="alert-box">${alert}</div>`;
    });

    // Apps
    let appSection = document.getElementById("apps");
    appSection.innerHTML = "";

    data.apps.forEach(app => {
      appSection.innerHTML += `
        <div class="card">
          <h4>${app.name}</h4>
          <p>Permissions: ${app.permissions.join(", ")}</p>
          <p>Risk: ${app.risk}</p>
          <button onclick="revokeAccess('${app.name}')">Revoke</button>
        </div>
      `;
    });
  })
  .catch(err => console.error("Error:", err));

// Button function
function revokeAccess(appName) {
  alert(appName + " access revoked!");
}
