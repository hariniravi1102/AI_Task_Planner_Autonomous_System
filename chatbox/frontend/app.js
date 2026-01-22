
const API = "http://localhost:8000";


let collectedText = "";
let lastSummary = "";
let jobId = crypto.randomUUID();
let map = null;
let drawnItems = null;


function showLoader(msg) {
  document.getElementById("loaderText").innerText = msg;
  document.getElementById("loader").style.display = "block";
}

function hideLoader() {
  document.getElementById("loader").style.display = "none";
}


document.getElementById("sendBtn").onclick = sendMessage;


async function sendMessage() {
  const msg = document.getElementById("userMessage").value.trim();
  const btn = document.getElementById("sendBtn");
  const out = document.getElementById("output");

  if (!msg) return;

  btn.disabled = true;
  out.innerHTML = "";
  showLoader("Thinking...");

  try {
    const res = await fetch(`${API}/chat`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg })
    });

    const data = await res.json();
    hideLoader();

    if (data.type === "CHAT") {
      out.innerHTML = `<div class="chat-reply">${data.response}</div>`;
      return;
    }

    await generateForm(msg);

  } catch (e) {
    hideLoader();
    alert("Backend error");
  } finally {
    btn.disabled = false;
  }
}



async function generateForm(task) {
  showLoader("Generating input form...");

  const res = await fetch(`${API}/generate-form`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task })
  });

  const data = await res.json();
  hideLoader();
  renderForm(data.form);
}

function renderForm(text) {
  const out = document.getElementById("output");
  out.innerHTML = "";

  const lines = text.split("\n");
  let block = null;

  lines.forEach(l => {
    l = l.trim();
    if (!l) return;

    if (l.startsWith("#")) {
      block = document.createElement("div");
      block.className = "question-block";
      block.innerHTML = `<div class="question">${l.slice(1)}</div>`;
      out.appendChild(block);
      return;
    }

    if (l.startsWith("-") && block) {
      block.innerHTML += `
        <div class="option">
          <label><input type="checkbox"> ${l.slice(1)}</label>
        </div>
      `;
    }
  });

  document.querySelectorAll(".question-block").forEach(b => {
    b.innerHTML += `
      <div class="note">
        <input type="text" placeholder="Notes / clarification (optional)">
      </div>
    `;
  });

  out.innerHTML += `
    <br>
    <button id="confirmBtn" onclick="collectAndConfirm()">Confirm Inputs</button>
  `;
}


function collectAndConfirm() {
  const btn = document.getElementById("confirmBtn");
  btn.disabled = true;
  showLoader("Confirming inputs...");

  setTimeout(async () => {
    collectedText = "";

    document.querySelectorAll(".question-block").forEach(block => {
      collectedText += block.querySelector(".question").innerText + "\n";

      block.querySelectorAll("input[type=checkbox]").forEach(cb => {
        if (cb.checked) {
          collectedText += "- " + cb.parentElement.innerText + "\n";
        }
      });

      const note = block.querySelector("input[type=text]").value;
      if (note) collectedText += "Note: " + note + "\n";

      collectedText += "\n";
    });

    const res = await fetch(`${API}/confirm`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: collectedText })
    });

    const data = await res.json();
    hideLoader();
    lastSummary = data.confirmation;
    renderConfirmation(lastSummary);
    btn.disabled = false;
  }, 0);
}


function renderConfirmation(text) {
  const summary = text
    .split("Is this correct?")[0]
    .replace("Final understanding:", "")
    .trim();

  document.getElementById("output").innerHTML = `
    <p><strong>Final understanding:</strong></p>
    <p>${summary}</p>
    <button onclick="proceed()">Yes, proceed</button>
    <button onclick="showRefine()">No, refine</button>
  `;
}

function showRefine() {
  document.getElementById("output").innerHTML += `
    <textarea id="refineText" placeholder="Refine your requirement"></textarea>
    <br><button onclick="refine()">Submit refinement</button>
  `;
}

async function refine() {
  const text = document.getElementById("refineText").value.trim();
  if (!text) return;

  showLoader("Updating understanding...");

  const res = await fetch(`${API}/refine`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      previous_summary: lastSummary,
      refinement_text: text
    })
  });

  const data = await res.json();
  hideLoader();
  lastSummary = data.confirmation;
  renderConfirmation(lastSummary);
}



function proceed() {
  document.getElementById("dataSection").style.display = "block";

  document.getElementById("output").innerHTML += `
    <p style="margin-top:15px; color:green;">
      Task confirmed. Upload files, draw AOI, or add external preference.
    </p>
  `;

  setTimeout(() => {
    if (!map) initMap();
  }, 300);
}



function initMap() {
  map = L.map("map").setView([20.5937, 78.9629], 5);

  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    attribution: "© OpenStreetMap"
  }).addTo(map);

  drawnItems = new L.FeatureGroup();
  map.addLayer(drawnItems);

  const drawControl = new L.Control.Draw({
    draw: {
      polygon: true,
      rectangle: true,
      circle: false,
      polyline: false,
      marker: false
    },
    edit: { featureGroup: drawnItems }
  });

  map.addControl(drawControl);

  map.on(L.Draw.Event.CREATED, e => {
    drawnItems.clearLayers();   // ONE AOI ONLY
    drawnItems.addLayer(e.layer);
  });
}



async function saveAllData() {
  showLoader("Saving spatial data...");

  const tasks = [];

  /* ---------- FILE UPLOAD ---------- */
  const files = document.getElementById("fileInput").files;
  if (files.length > 0) {
    const fd = new FormData();
    fd.append("job_id", jobId);
    for (let f of files) fd.append("files", f);

    tasks.push(fetch(`${API}/upload`, {
      method: "POST",
      body: fd
    }));
  }


  if (drawnItems && drawnItems.getLayers().length > 0) {
    const aoiGeoJSON = drawnItems.toGeoJSON();

    tasks.push(fetch(`${API}/save-aoi`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        job_id: jobId,
        geojson: aoiGeoJSON
      })
    }));
  }

  const external = document.getElementById("externalText").value.trim();
  if (external) {
    tasks.push(fetch(`${API}/save-external`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        job_id: jobId,
        text: external
      })
    }));
  }

  if (tasks.length === 0) {
    hideLoader();
    alert("Please upload files, draw AOI, or provide external preference.");
    return;
  }

  await Promise.all(tasks);

  hideLoader();
  document.getElementById("uploadResult").innerHTML =
    "<b style='color:green'>All spatial inputs saved successfully.</b>";
}
