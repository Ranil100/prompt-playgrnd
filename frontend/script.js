const API_URL = "http://127.0.0.1:8000";

const taskInput = document.getElementById("taskInput");
const runBtn = document.getElementById("runBtn");
const statusEl = document.getElementById("status");
const temperature = document.getElementById("temperature");
const tempValue = document.getElementById("tempValue");
const resultsSection = document.getElementById("resultsSection");
const resultGrid = document.getElementById("resultGrid");
const winnerBadge = document.getElementById("winnerBadge");
const winnerReason = document.getElementById("winnerReason");

temperature.addEventListener("input", () => {
  tempValue.textContent = temperature.value;
});

document.querySelectorAll("[data-example]").forEach(button => {
  button.addEventListener("click", () => {
    taskInput.value = button.dataset.example;
    taskInput.focus();
  });
});

function setStatus(text, type) {
  statusEl.textContent = text;
  statusEl.className = `status ${type}`;
}

function titleCase(value) {
  return value.replace("-", " ").replace(/\b\w/g, c => c.toUpperCase());
}

function renderResults(data) {
  resultGrid.innerHTML = "";

  const maxScore = Math.max(...data.results.map(r => r.score), 1);

  data.results.forEach(result => {
    const isWinner = result.strategy === data.winner;
    const card = document.createElement("article");
    card.className = `result-card ${isWinner ? "winner" : ""}`;

    card.innerHTML = `
      <div class="card-head">
        <div>
          <div class="strategy">${titleCase(result.strategy)} ${isWinner ? "🏆" : ""}</div>
          <div class="meta">${result.latency_ms} ms response time</div>
        </div>
        <div class="meta">${result.score}/100</div>
      </div>
      <div class="output"></div>
      <div class="scorebar">
        <div class="score-label"><span>Quality score</span><span>${result.score}%</span></div>
        <div class="bar"><div class="fill" style="width:${result.score}%"></div></div>
      </div>
      <details class="prompt-details">
        <summary>View generated prompt</summary>
        <div class="prompt-text"></div>
      </details>
    `;

    card.querySelector(".output").textContent = result.output;
    card.querySelector(".prompt-text").textContent = result.prompt;
    resultGrid.appendChild(card);
  });

  winnerBadge.textContent = `🏆 Best: ${titleCase(data.winner)}`;
  winnerReason.textContent = data.winner_reason;
  resultsSection.classList.remove("hidden");
  resultsSection.scrollIntoView({ behavior: "smooth", block: "start" });
}

runBtn.addEventListener("click", async () => {
  const task = taskInput.value.trim();

  if (!task) {
    taskInput.focus();
    setStatus("Enter a task first", "idle");
    return;
  }

  runBtn.disabled = true;
  setStatus("Running 3 prompts…", "running");

  try {
    const response = await fetch(`${API_URL}/api/experiment`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        task,
        temperature: Number(temperature.value)
      })
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Experiment failed");
    }

    renderResults(data);
    setStatus("Experiment complete", "done");
  } catch (error) {
    console.error(error);
    setStatus("Error", "idle");
    alert(error.message);
  } finally {
    runBtn.disabled = false;
  }
});
