let chart = null;
let flowChart = null;




const SCALE = 100;
// 
// let netDiffChart;              // persistent
// let netDiffHistory = [];/
// let netDiffLabels = [];
// let prevNetDiff = 0;
// const MAX_BARS = 100;





/* ==============================
   DATA LOADER
================================ */
async function loadData() {
  const res = await fetch("/data");
  const data = await res.json();

  if (!data || !data.pullers) return;

  renderSummary(data);
  renderTables(data);
  renderBarChart(data);
  renderFlowChart(data);
  // renderFlowChart(liveData);

}

/* ==============================
   SUMMARY CARDS
================================ */
function renderSummary(data) {
  const pullers = data.pullers || [];
  const draggers = data.draggers || [];

  const pullForce = pullers.reduce((s, x) => s + (x.contribution || 0), 0);
  const dragForce = draggers.reduce((s, x) => s + (x.contribution || 0), 0);
  const netForce  = pullForce + dragForce;

  document.getElementById("posForce").innerText =
    (pullForce * SCALE).toFixed(2);

  document.getElementById("negForce").innerText =
    (dragForce * SCALE).toFixed(2);

  document.getElementById("netForce").innerText =
    (netForce * SCALE).toFixed(2);
}



/* ==============================
   TABLES
================================ */
function renderTables(data) {
  renderTable("pullers", data.pullers || []);
  renderTable("draggers", data.draggers || []);
}

function renderTable(id, stocks) {
  let html = `
    <tr>
      <th>Symbol</th>
      <th>LTP</th>
      <th>Δ</th>
      <th>%</th>
      <th>Flow</th>
    </tr>`;

  stocks.forEach(s => {
    const flow = s.contribution || 0;
    const flowDisplay = (flow * SCALE).toFixed(2);

    html += `
      <tr>
        <td>${s.symbol}</td>
        <td>${s.ltp.toFixed(2)}</td>

        <td class="${s.change >= 0 ? "green" : "red"}">
          ${s.change.toFixed(2)}
        </td>

        <td class="${s.percent >= 0 ? "green" : "red"}">
          ${s.percent.toFixed(2)}%
        </td>

        <td class="${flow >= 0 ? "green" : "red"}">
          ${flowDisplay}
        </td>
      </tr>`;
  });

  document.getElementById(id).innerHTML = html;
}


/* ==============================
   BAR CHART (RELATIVE FLOW)
================================ */
function renderBarChart(data) {
  const all = [...(data.pullers || []), ...(data.draggers || [])];

  if (!all.length) return;

  const labels = all.map(x => x.symbol);

  // KEEP PRECISION (IMPORTANT)
  const values = all.map(x => +(x.contribution * SCALE).toFixed(2));

  const colors = all.map(x =>
    x.contribution >= 0 ? "#00ff99" : "#ff4d4d"
  );

  const maxAbs = Math.max(...values.map(v => Math.abs(v))) || 1;

  if (chart) chart.destroy();

  chart = new Chart(document.getElementById("chart"), {
    type: "bar",
    data: {
      labels,
      datasets: [{
        data: values,
        backgroundColor: colors,
        borderRadius: 6,
        barThickness: 18
      }]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { display: false },
        tooltip: {
          callbacks: {
            label: ctx => `Flow: ${ctx.raw}`
          }
        }
      },
      scales: {
        y: {
          min: -maxAbs * 1.2,
          max: maxAbs * 1.2,
          ticks: {
            color: "#fff",
            callback: v => v
          },
          grid: {
            color: ctx => ctx.tick.value === 0 ? "#fff" : "#222",
            lineWidth: ctx => ctx.tick.value === 0 ? 2 : 1
          }
        },
        x: {
          ticks: { color: "#fff" },
          grid: { color: "#222" }
        }
      }
    }
  });
}


 /*==============================
   FLOW CHART (CORE SIGNAL)
================================ */
function renderFlowChart(data) {
  const pullers = data.pullers;
  const draggers = data.draggers;

  const maxLen = Math.max(pullers.length, draggers.length);

  let pSum = 0;
  let dSum = 0;

  const pullCum = [];
  const dragCum = [];
  const netCum = [];

  for (let i = 0; i < maxLen; i++) {
    if (pullers[i]) pSum += pullers[i].contribution;
    if (draggers[i]) dSum += draggers[i].contribution;

    pullCum.push(pSum * SCALE);
    dragCum.push(dSum * SCALE);
    netCum.push((pSum + dSum) * SCALE);
  }

  /* -------- Momentum -------- */
  const momentum = netCum.map((v, i) =>
    i === 0 ? 0 : v - netCum[i - 1]
  );

  /* -------- Market State -------- */
  let state = "Neutral";
  const lastNet = netCum.at(-1);
  const lastMom = momentum.at(-1);

  if (lastNet > 0 && lastMom > 0) state = "Bullish Expansion";
  else if (lastNet > 0 && lastMom < 0) state = "Bullish Exhaustion";
  else if (lastNet < 0 && lastMom < 0) state = "Bearish Expansion";
  else if (lastNet < 0 && lastMom > 0) state = "Bearish Exhaustion";

  document.getElementById("marketState").innerText = state;

  const labels = Array.from({ length: maxLen }, (_, i) => i + 1);

  if (flowChart) flowChart.destroy();

  flowChart = new Chart(document.getElementById("flowChart"), {
    type: "line",
    data: {
      labels,
      datasets: [
        {
          label: "Zero",
          data: Array(maxLen).fill(0),
          borderColor: "#ffffff",
          borderWidth: 3,
          borderDash: [6, 6],
          pointRadius: 0
        },
        {
          label: "Positive Force",
          data: pullCum,
          borderColor: "#00ff99",
          borderWidth: 2,
          pointRadius: 0,
          tension: 0.3
        },
        {
          label: "Negative Force",
          data: dragCum,
          borderColor: "#ff4d4d",
          borderWidth: 2,
          pointRadius: 0,
          tension: 0.3
        },
        {
          label: "Net Index Flow",
          data: netCum,
          borderColor: "#ffffff",
          borderWidth: 3,
          pointRadius: 0,
          tension: 0.3
        },
        {
          label: "Flow Momentum",
          data: momentum,
          borderColor: "#ffaa00",
          borderWidth: 2,
          pointRadius: 0,
          tension: 0.3
        }
      ]
    },
    options: {
      plugins: {
        legend: {
          labels: { color: "#fff" }
        }
      },
      scales: {
        y: {
          ticks: { color: "#fff" },
          grid: {
            color: ctx =>
              ctx.tick.value === 0 ? "#ffffff" : "#222",
            lineWidth: ctx =>
              ctx.tick.value === 0 ? 3 : 1
          }
        },
        x: {
          ticks: { color: "#fff" },
          grid: { color: "#222" }
        }
      }
    }
  });
}

// function renderFlowChart(data) {
//   const pullers = data.pullers || [];
//   const draggers = data.draggers || [];

//   // ---- NET DIFF CALC ----
//   let pSum = 0, dSum = 0;
//   for (const p of pullers) pSum += p.contribution || 0;
//   for (const d of draggers) dSum += d.contribution || 0;

//   const netDiff = (pSum + dSum) * SCALE;

//   // ---- STORE HISTORY ----
//   netDiffHistory.push(+netDiff.toFixed(2));
//   netDiffLabels.push(new Date().toLocaleTimeString());

//   if (netDiffHistory.length > MAX_BARS) {
//     netDiffHistory.shift();
//     netDiffLabels.shift();
//   }

//   // ---- CREATE ONCE ----
//   if (!netDiffChart) {
//     netDiffChart = new Chart(document.getElementById("flowChart"), {
//       type: "bar",
//       data: {
//         labels: netDiffLabels,
//         datasets: [{
//           label: "Net Diff",
//           data: netDiffHistory,
//           backgroundColor: ctx =>
//             ctx.raw >= 0 ? "#00ff99" : "#ff4d4d",
//           barThickness: 10,
//           borderRadius: 4
//         }]
//       },
//       options: {
//         animation: false,
//         plugins: {
//           legend: { display: false }
//         },
//         scales: {
//           y: {
//             ticks: { color: "#fff" },
//             grid: {
//               color: ctx =>
//                 ctx.tick.value === 0 ? "#ffffff" : "#222",
//               lineWidth: ctx =>
//                 ctx.tick.value === 0 ? 3 : 1
//             }
//           },
//           x: {
//             ticks: { color: "#aaa", maxRotation: 0 },
//             grid: { display: false }
//           }
//         }
//       }
//     });
//   } else {
//     // ---- UPDATE ONLY ----
//     netDiffChart.update("none");
//   }
// }

// 


// function renderFlowChart(data) {
//   const pullers = data.pullers || [];
//   const draggers = data.draggers || [];

//   let pSum = 0, dSum = 0;
//   pullers.forEach(p => pSum += p.contribution || 0);
//   draggers.forEach(d => dSum += d.contribution || 0);

//   const netDiff = (pSum + dSum) * SCALE;

//   // 🔥 KEY CHANGE (DELTA)
//   const delta = +(netDiff - prevNetDiff).toFixed(3);
//   prevNetDiff = netDiff;

//   netDiffHistory.push(delta);
//   netDiffLabels.push(new Date().toLocaleTimeString());

//   if (netDiffHistory.length > MAX_BARS) {
//     netDiffHistory.shift();
//     netDiffLabels.shift();
//   }

//   if (!netDiffChart) {
//     netDiffChart = new Chart(document.getElementById("flowChart"), {
//       type: "bar",
//       data: {
//         labels: netDiffLabels,
//         datasets: [{
//           data: netDiffHistory,
//           backgroundColor: ctx =>
//             ctx.raw >= 0 ? "#00ff99" : "#ff4d4d",
//           barThickness: 10,
//           borderRadius: 3
//         }]
//       },
//       options: {
//         animation: false,
//         plugins: { legend: { display: false } },
//         scales: {
//           y: {
//             suggestedMin: -0.05,
//             suggestedMax: 0.05,
//             ticks: { color: "#fff" },
//             grid: {
//               color: v => v.tick.value === 0 ? "#fff" : "#222",
//               lineWidth: v => v.tick.value === 0 ? 2 : 1
//             }
//           },
//           x: {
//             ticks: { color: "#aaa", maxRotation: 0 },
//             grid: { display: false }
//           }
//         }
//       }
//     });
//   } else {
//     netDiffChart.update("none");
//   }
// }



/* ==============================
   AUTO REFRESH
================================ */
loadData();
setInterval(loadData, 1000);
