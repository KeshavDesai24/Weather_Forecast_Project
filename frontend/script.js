const backendURL = "http://127.0.0.1:8000";  // Update if backend is deployed

async function getForecast() {
  const res = await fetch(`${backendURL}/forecast`);
  const data = await res.json();
  const forecastDiv = document.getElementById("forecast");

  forecastDiv.innerHTML = "<h3>📅 Forecast:</h3><ul>" +
    data.forecast.map(day =>
      `<li><b>${day.day}</b>: ${day.temperature} °C</li>`
    ).join('') + "</ul>";
}

async function checkHeatwave() {
  const res = await fetch(`${backendURL}/heatwave-detection`);
  const data = await res.json();
  const alertDiv = document.getElementById("heatwave-alerts");

  if (data.heatwave_days.length === 0) {
    alertDiv.innerHTML = "<p>✅ No heatwaves expected.</p>";
  } else {
    alertDiv.innerHTML = "<ul>" + data.heatwave_days.map(item =>
      `<li>
        🔥 <b>${item.day}</b>: ${item.temperature} °C<br/>
        <i>Remedies:</i><ul>${
          Object.entries(item.remedies).map(([tip, desc]) => `<li><b>${tip}</b>: ${desc}</li>`).join('')
        }</ul>
      </li>`
    ).join('') + "</ul>";
  }
}
