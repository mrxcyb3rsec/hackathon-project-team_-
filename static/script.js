// 🔗 CHANGE THIS to your Codespaces URL
const API_URL = "https://studious-space-goldfish-p56gj746gqrc6wjq-5000.app.github.dev/data";

// Fetch data from backend
fetch(API_URL)
  .then(response => response.json())
  .then(data => {
    console.log("Backend Data:", data);

    // ✅ Trust Score
    document.getElementById("score").innerText = data.trust_score + "%";

    // ✅ Alerts Section
    let alertBox = document.getElementById("alerts");
    alertBox.innerHTML = "";

    data.alerts.forEach(alert => {
      let div = document.createElement("div");
      div.className = "alert-box";
      div.innerText = alert;
      alertBox.appendChild(div);
    });

    // ✅ Apps Section
    let appSection = document.getElementById("apps");
    appSection.innerHTML = "";

    data.apps.forEach(app => {
      let card = document.createElement("div");
      card.className = "app-card";

      card.innerHTML = `
        <h3>${app.name}</h3>
        <p><b>Permissions:</b> ${app.permissions.join(", ")}</p>
        <p><b>Risk:</b> ${app.risk}</p>
        <p><b>Last Used:</b> ${app.last_accessed}</p>
        <button onclick="revokeAccess('${app.name}')">Revoke Access</button>
      `;

      appSection.appendChild(card);
    });
  })
  .catch(error => {
    console.error("Error fetching data:", error);
  });


// 🔥 Revoke Function
function revokeAccess(appName) {
  alert(appName + " access revoked!");

  // Optional: remove card visually
  const cards = document.querySelectorAll(".app-card");
  cards.forEach(card => {
    if (card.innerText.includes(appName)) {
      card.remove();
    }
  });
}
