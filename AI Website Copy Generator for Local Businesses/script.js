// ─── LOADING MESSAGES ──────────────────────────────
const loadingMessages = [
  "Studying your business…",
  "Crafting your headlines…",
  "Writing conversion copy…",
  "Polishing the final words…",
  "Almost there…",
];

let loadingInterval = null;

function cycleLoadingMessages() {
  let idx = 0;
  const el = document.getElementById("loadingLabel");
  el.textContent = loadingMessages[0];
  loadingInterval = setInterval(() => {
    idx = (idx + 1) % loadingMessages.length;
    el.textContent = loadingMessages[idx];
  }, 1800);
}

function stopLoadingMessages() {
  if (loadingInterval) {
    clearInterval(loadingInterval);
    loadingInterval = null;
  }
}

// ─── SHOW / HIDE STATES ────────────────────────────
function showLoading() {
  document.getElementById("emptyState").style.display = "none";
  document.getElementById("results").style.display = "none";
  document.getElementById("loadingState").style.display = "flex";
  cycleLoadingMessages();
}

function showResults() {
  document.getElementById("loadingState").style.display = "none";
  document.getElementById("emptyState").style.display = "none";
  document.getElementById("results").style.display = "block";
  stopLoadingMessages();
}

function showEmpty() {
  document.getElementById("loadingState").style.display = "none";
  document.getElementById("results").style.display = "none";
  document.getElementById("emptyState").style.display = "block";
  stopLoadingMessages();
}

function showError(msg) {
  const box = document.getElementById("errorBox");
  box.textContent = "⚠️ " + msg;
  box.style.display = "block";
}

function clearError() {
  const box = document.getElementById("errorBox");
  box.style.display = "none";
  box.textContent = "";
}

// ─── VALIDATION ────────────────────────────────────
function getFormValues() {
  return {
    business_type: document.getElementById("business_type").value.trim(),
    location: document.getElementById("location").value.trim(),
    services: document.getElementById("services").value.trim(),
    target_audience: document.getElementById("target_audience").value.trim(),
    tone: document.getElementById("tone").value,
  };
}

function validate(values) {
  if (!values.business_type) return "Please enter your business type.";
  if (!values.location) return "Please enter your location.";
  if (!values.services) return "Please describe your services.";
  if (!values.target_audience) return "Please describe your target audience.";
  return null;
}

// ─── RENDER COPY ───────────────────────────────────
function renderCopy(copy) {
  // Homepage
  document.getElementById("homepage-headline").textContent = copy.homepage.headline;
  document.getElementById("homepage-subheadline").textContent = copy.homepage.subheadline;
  document.getElementById("homepage-hero").textContent = copy.homepage.hero_description;

  // About
  document.getElementById("about-title").textContent = copy.about.title;
  document.getElementById("about-body").textContent = copy.about.body;

  // Services
  document.getElementById("services-title").textContent = copy.services.title;
  document.getElementById("services-intro").textContent = copy.services.intro;

  const servicesList = document.getElementById("services-list");
  servicesList.innerHTML = "";
  (copy.services.list || []).forEach((svc) => {
    const li = document.createElement("li");
    li.innerHTML = `
      <div class="service-name">${escapeHtml(svc.name)}</div>
      <div class="service-desc">${escapeHtml(svc.description)}</div>
    `;
    servicesList.appendChild(li);
  });

  // Why Choose Us
  document.getElementById("why-title").textContent = copy.why_choose_us.title;
  const whyGrid = document.getElementById("why-grid");
  whyGrid.innerHTML = "";
  (copy.why_choose_us.points || []).forEach((pt) => {
    const div = document.createElement("div");
    div.className = "why-point";
    div.innerHTML = `
      <div class="why-icon">${escapeHtml(pt.icon || "✓")}</div>
      <div class="why-content">
        <div class="why-title">${escapeHtml(pt.title)}</div>
        <div class="why-body">${escapeHtml(pt.body)}</div>
      </div>
    `;
    whyGrid.appendChild(div);
  });

  // CTA
  document.getElementById("cta-headline").textContent = copy.cta.headline;
  document.getElementById("cta-subtext").textContent = copy.cta.subtext;
  document.getElementById("cta-button").textContent = copy.cta.button_text;
  document.getElementById("cta-secondary").textContent = copy.cta.secondary_text;
}

// ─── GENERATE ──────────────────────────────────────
async function generateCopy() {
  clearError();

  const values = getFormValues();
  const validationError = validate(values);
  if (validationError) {
    showError(validationError);
    return;
  }

  const btn = document.getElementById("generateBtn");
  btn.classList.add("loading");
  btn.querySelector(".btn-text").textContent = "Generating…";

  showLoading();

  // Scroll output into view on mobile
  if (window.innerWidth <= 900) {
    document.getElementById("outputPanel").scrollIntoView({ behavior: "smooth" });
  }

  try {
    const response = await fetch("/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    });

    const data = await response.json();

    if (!response.ok || !data.success) {
      throw new Error(data.error || "Server returned an error. Please try again.");
    }

    renderCopy(data.copy);
    showResults();
  } catch (err) {
    showEmpty();
    showError(err.message || "Something went wrong. Please check your connection and try again.");
  } finally {
    btn.classList.remove("loading");
    btn.querySelector(".btn-text").textContent = "Generate Website Copy";
  }
}

// ─── COPY TO CLIPBOARD ─────────────────────────────
function getCardText(cardId) {
  const card = document.getElementById(cardId);
  if (!card) return "";
  // Collect all visible text nodes, excluding button
  const btn = card.querySelector(".copy-btn");
  const label = card.querySelector(".card-label");
  let text = "";
  card.querySelectorAll("h3, p, .service-name, .service-desc, .why-title, .why-body, .cta-button-preview").forEach((el) => {
    if (!btn.contains(el)) {
      text += el.textContent.trim() + "\n";
    }
  });
  if (label) text = label.textContent.trim() + "\n" + "─".repeat(30) + "\n" + text;
  return text.trim();
}

function copySection(cardId) {
  const text = getCardText(cardId);
  const card = document.getElementById(cardId);
  const btn = card.querySelector(".copy-btn");

  navigator.clipboard.writeText(text).then(() => {
    btn.textContent = "Copied!";
    btn.classList.add("copied");
    setTimeout(() => {
      btn.textContent = "Copy";
      btn.classList.remove("copied");
    }, 2000);
  }).catch(() => {
    // Fallback
    const ta = document.createElement("textarea");
    ta.value = text;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
    btn.textContent = "Copied!";
    btn.classList.add("copied");
    setTimeout(() => {
      btn.textContent = "Copy";
      btn.classList.remove("copied");
    }, 2000);
  });
}

function copyAll() {
  const sections = ["card-homepage", "card-about", "card-services", "card-why", "card-cta"];
  const allText = sections.map((id) => getCardText(id)).join("\n\n" + "═".repeat(40) + "\n\n");
  const btn = document.querySelector(".copy-all-btn");

  navigator.clipboard.writeText(allText).then(() => {
    btn.textContent = "✓ All Copied!";
    setTimeout(() => { btn.textContent = "📋 Copy All"; }, 2500);
  }).catch(() => {
    const ta = document.createElement("textarea");
    ta.value = allText;
    document.body.appendChild(ta);
    ta.select();
    document.execCommand("copy");
    document.body.removeChild(ta);
    btn.textContent = "✓ All Copied!";
    setTimeout(() => { btn.textContent = "📋 Copy All"; }, 2500);
  });
}

// ─── HELPERS ───────────────────────────────────────
function escapeHtml(str) {
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

// ─── ENTER KEY SUPPORT ─────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  ["business_type", "location", "services", "target_audience"].forEach((id) => {
    document.getElementById(id).addEventListener("keydown", (e) => {
      if (e.key === "Enter") generateCopy();
    });
  });
});
