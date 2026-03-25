fetch("http://127.0.0.1:5000/data")
  .then(response => response.json())
  .then(data => {
    console.log(data);

    // Update Trust Score
    document.getElementById("score").innerText = data.trust_score + "%";

    // Alerts
    let alertBox = document.getElementById("alerts");
    alertBox.innerHTML = "";
    data.alerts.forEach(alert => {
      alertBox.innerHTML += `<div class="alert">${alert}</div>`;
    });

    // Apps
    let appSection = document.getElementById("apps");
    appSection.innerHTML = "";
    data.apps.forEach(app => {
      appSection.innerHTML += `
        <div class="app-card">
          <h3>${app.name}</h3>
          <p>Permissions: ${app.permissions.join(", ")}</p>
          <p>Risk: ${app.risk}</p>
          <button onclick="revokeAccess('${app.name}')">Revoke</button>
        </div>
      `;
    });
  });
