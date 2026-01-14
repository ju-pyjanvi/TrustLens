// Store analysis results for export
let currentResults = null
const analysisHistory = []

async function analyzeText() {
  const text = document.getElementById("inputText").value.trim()

  if (!text) {
    alert("Please enter some text to analyze")
    return
  }

  try {
    const res = await fetch("http://127.0.0.1:8000/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    })

    const data = await res.json()
    currentResults = data

    renderResults(data, text.substring(0, 50) + "...")
  } catch (err) {
    console.error("Error:", err)
    alert("Error connecting to backend. Make sure the server is running.")
  }
}

async function analyzeUrl() {
  const url = document.getElementById("inputUrl").value.trim()

  if (!url) {
    alert("Please enter a URL to analyze")
    return
  }

  if (!url.startsWith("http://") && !url.startsWith("https://")) {
    alert("Please enter a valid URL starting with http:// or https://")
    return
  }

  const loadingCard = document.getElementById("loadingCard")
  const urlAnalyzeBtn = document.getElementById("urlAnalyzeBtn")

  try {
    // Show loading state
    loadingCard.classList.remove("hidden")
    urlAnalyzeBtn.disabled = true
    urlAnalyzeBtn.innerHTML = `
      <svg class="btn-spinner" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M21 12a9 9 0 1 1-6.219-8.56"></path>
      </svg>
      Analyzing...
    `

    // Simulate progress steps
    simulateProgress()

    const res = await fetch("http://127.0.0.1:8000/analyze-url", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url }),
    })

    const data = await res.json()
    currentResults = data

    // Hide loading state
    loadingCard.classList.add("hidden")
    resetAnalyzeButton()

    if (data.error) {
      alert("Error: " + data.error)
      return
    }

    renderResults(data, url)
    addToHistory(url, data)
  } catch (err) {
    console.error("Error:", err)
    loadingCard.classList.add("hidden")
    resetAnalyzeButton()
    alert("Error connecting to backend. Make sure the server is running.")
  }
}

function resetAnalyzeButton() {
  const urlAnalyzeBtn = document.getElementById("urlAnalyzeBtn")
  urlAnalyzeBtn.disabled = false
  urlAnalyzeBtn.innerHTML = `
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      <circle cx="11" cy="11" r="8"></circle>
      <path d="m21 21-4.35-4.35"></path>
    </svg>
    Analyze
  `
}

function simulateProgress() {
  const steps = document.querySelectorAll(".step")
  const progressFill = document.querySelector(".progress-bar-fill")
  const stepCount = document.querySelector(".progress-step-count")

  let currentStep = 0
  const interval = setInterval(() => {
    if (currentStep < steps.length) {
      steps.forEach((s, i) => {
        s.classList.remove("active")
        if (i < currentStep) s.classList.add("completed")
      })
      steps[currentStep].classList.add("active")
      progressFill.style.width = `${((currentStep + 1) / steps.length) * 100}%`
      stepCount.textContent = `${currentStep + 1} of ${steps.length}`
      currentStep++
    } else {
      clearInterval(interval)
    }
  }, 800)
}

function renderResults(data, source) {
  // Show results sections
  document.getElementById("intentSection").classList.remove("hidden")
  document.getElementById("resultsSection").classList.remove("hidden")

  // Render intent charts
  renderIntentCharts(data.intent_breakdown || {})

  // Render pattern cards
  renderPatternCards(data.detections || [])
}

function renderIntentCharts(intentBreakdown) {
  const container = document.getElementById("intentCharts")
  container.innerHTML = ""

  // Calculate aggregate scores
  const urgencyScore = (intentBreakdown.urgency_scarcity || 0) + (intentBreakdown.fomo_emotion || 0)
  const persuasiveScore = (intentBreakdown.social_proof || 0) + (intentBreakdown.pricing_tricks || 0)
  const informativeScore = Math.max(0, 100 - urgencyScore - persuasiveScore)

  const intents = [
    { name: "Manipulative Intent", value: Math.min(100, Math.round(urgencyScore)), color: "danger" },
    { name: "Persuasive Intent", value: Math.min(100, Math.round(persuasiveScore)), color: "warning" },
    { name: "Informative Intent", value: Math.round(informativeScore / 3), color: "success" },
  ]

  intents.forEach(({ name, value, color }) => {
    const radius = 48
    const circumference = 2 * Math.PI * radius
    const offset = circumference - (value / 100) * circumference

    const chart = document.createElement("div")
    chart.className = "intent-chart"
    chart.innerHTML = `
      <div class="circular-progress">
        <svg width="120" height="120">
          <circle class="circle-bg" cx="60" cy="60" r="${radius}"></circle>
          <circle class="circle-progress ${color}" cx="60" cy="60" r="${radius}" 
                  style="stroke-dasharray: ${circumference}; stroke-dashoffset: ${circumference};"
                  data-offset="${offset}"></circle>
        </svg>
        <div class="progress-content">
          <div class="progress-text">${value}%</div>
        </div>
      </div>
      <div class="intent-label">${name}</div>
    `
    container.appendChild(chart)

    // Animate the circle
    setTimeout(() => {
      chart.querySelector(".circle-progress").style.strokeDashoffset = offset
    }, 100)
  })
}

function renderPatternCards(detections) {
  const container = document.getElementById("patternCards")
  const countEl = document.getElementById("patternCount")
  container.innerHTML = ""

  if (detections.length === 0) {
    container.innerHTML = `
      <div style="text-align: center; padding: 40px; color: var(--text-muted);">
        <p>No dark patterns detected.</p>
      </div>
    `
    countEl.textContent = "0 patterns found"
    return
  }

  // Deduplicate
  const seen = new Set()
  const uniqueDetections = detections.filter((d) => {
    const key = `${d.pattern}-${d.matched_text}`
    if (seen.has(key)) return false
    seen.add(key)
    return true
  })

  countEl.textContent = `${uniqueDetections.length} patterns found`

  // Group by pattern type
  const grouped = {}
  uniqueDetections.forEach((d) => {
    if (!grouped[d.pattern]) {
      grouped[d.pattern] = { ...d, count: 1, examples: [d.matched_text] }
    } else {
      grouped[d.pattern].count++
      if (grouped[d.pattern].examples.length < 3) {
        grouped[d.pattern].examples.push(d.matched_text)
      }
    }
  })

  Object.values(grouped).forEach((detection) => {
    const severity = getSeverity(detection.category)
    const card = document.createElement("div")
    card.className = "pattern-item"
    card.innerHTML = `
      <div class="pattern-item-header">
        <span class="pattern-name">${detection.pattern}</span>
        <span class="pattern-occurrences">${detection.count}x</span>
      </div>
      <div class="pattern-tags">
        <span class="category-tag">${detection.category}</span>
        <span class="severity-tag ${severity.class}">
          <span class="severity-dot"></span>
          ${severity.label}
        </span>
      </div>
      <p class="pattern-explanation">${detection.explanation}</p>
      <div class="pattern-example">
        <div class="pattern-example-label">Detected Example:</div>
        <div class="pattern-example-text">"${detection.examples[0]}"</div>
      </div>
    `
    container.appendChild(card)
  })
}

function getSeverity(category) {
  const high = ["Urgency & Scarcity", "FOMO & Emotion", "Trust Manipulation"]
  const critical = ["Data Harvesting"]

  if (critical.includes(category)) return { class: "critical", label: "CRITICAL" }
  if (high.includes(category)) return { class: "high", label: "HIGH" }
  return { class: "medium", label: "MEDIUM" }
}

function addToHistory(source, data) {
  const historyCard = document.getElementById("historyCard")
  const historyList = document.getElementById("historyList")
  const historyCount = document.getElementById("historyCount")

  historyCard.classList.remove("hidden")

  const score = Object.values(data.intent_breakdown || {}).reduce((a, b) => a + b, 0)
  const patternCount = (data.detections || []).length

  const item = {
    date: new Date().toLocaleString(),
    source,
    score: Math.round(score / 7),
    patterns: patternCount,
  }

  analysisHistory.unshift(item)
  historyCount.textContent = `${analysisHistory.length} analyses`

  const isUrl = source.startsWith("http")
  const itemEl = document.createElement("div")
  itemEl.className = "history-item"
  itemEl.innerHTML = `
    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
      ${isUrl ? '<circle cx="12" cy="12" r="10"></circle><line x1="2" y1="12" x2="22" y2="12"></line>' : '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>'}
    </svg>
    <div class="history-content">
      <div class="history-date">${item.date}</div>
      <div class="history-score">${item.score}% manipulative</div>
      <div class="history-url">${source}</div>
      <div class="history-patterns">${patternCount} patterns detected</div>
    </div>
  `
  historyList.prepend(itemEl)
}

// Export functions
function exportPDF() {
  alert("PDF export coming soon!")
}

function exportJSON() {
  if (!currentResults) {
    alert("No analysis results to export")
    return
  }
  const blob = new Blob([JSON.stringify(currentResults, null, 2)], { type: "application/json" })
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = "trustlens-analysis.json"
  a.click()
}

function exportCSV() {
  if (!currentResults || !currentResults.detections) {
    alert("No analysis results to export")
    return
  }
  const headers = ["Pattern", "Category", "Matched Text", "Explanation"]
  const rows = currentResults.detections.map((d) => [
    d.pattern,
    d.category,
    `"${d.matched_text}"`,
    `"${d.explanation}"`,
  ])
  const csv = [headers.join(","), ...rows.map((r) => r.join(","))].join("\n")
  const blob = new Blob([csv], { type: "text/csv" })
  const url = URL.createObjectURL(blob)
  const a = document.createElement("a")
  a.href = url
  a.download = "trustlens-patterns.csv"
  a.click()
}

// Navigation
function navigateTo(view) {
  document.querySelectorAll(".view").forEach((v) => v.classList.remove("active"))
  document.querySelectorAll(".nav-item").forEach((n) => n.classList.remove("active"))
  document.querySelectorAll(".header-nav a").forEach((n) => n.classList.remove("active"))

  const viewMap = {
    home: "homeView",
    analyzer: "analyzerView",
    library: "libraryView",
    research: "researchView",
    about: "aboutView",
  }

  document.getElementById(viewMap[view]).classList.add("active")
  document.querySelector(`.nav-item[data-view="${view}"]`)?.classList.add("active")
  document.querySelector(`.header-nav a[data-view="${view}"]`)?.classList.add("active")
}

function filterPatterns() {
  const category = document.querySelector('input[name="category"]:checked')?.value || "all"
  const severity = document.querySelector('input[name="severity"]:checked')?.value || "all"
  const industry = document.querySelector('input[name="industry"]:checked')?.value || "all"

  const cards = document.querySelectorAll(".library-pattern-card")
  let visibleCount = 0

  cards.forEach((card) => {
    const cardCategory = card.dataset.category
    const cardSeverity = card.dataset.severity
    const cardIndustries = card.dataset.industries?.split(",") || []

    const categoryMatch = category === "all" || cardCategory === category
    const severityMatch = severity === "all" || cardSeverity === severity
    const industryMatch = industry === "all" || cardIndustries.includes(industry)

    if (categoryMatch && severityMatch && industryMatch) {
      card.classList.remove("hidden")
      visibleCount++
    } else {
      card.classList.add("hidden")
    }
  })

  document.getElementById("visibleCount").textContent = visibleCount
}

function resetFilters() {
  document.querySelectorAll('input[name="category"]')[0].checked = true
  document.querySelectorAll('input[name="severity"]')[0].checked = true
  document.querySelectorAll('input[name="industry"]')[0].checked = true
  filterPatterns()
}

// Initialize
document.addEventListener("DOMContentLoaded", () => {
  // Sidebar nav
  document.querySelectorAll(".nav-item").forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault()
      navigateTo(item.dataset.view)
    })
  })

  // Header nav
  document.querySelectorAll(".header-nav a, .header-cta").forEach((item) => {
    item.addEventListener("click", (e) => {
      e.preventDefault()
      navigateTo(item.dataset.view)
    })
  })

  // Input toggle
  document.querySelectorAll(".toggle-btn").forEach((btn) => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".toggle-btn").forEach((b) => b.classList.remove("active"))
      btn.classList.add("active")

      const mode = btn.dataset.mode
      if (mode === "text") {
        document.getElementById("textInputContainer").classList.remove("hidden")
        document.getElementById("urlInputContainer").classList.add("hidden")
      } else {
        document.getElementById("textInputContainer").classList.add("hidden")
        document.getElementById("urlInputContainer").classList.remove("hidden")
      }
    })
  })

  // Keyboard shortcuts
  document.getElementById("inputText")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && (e.metaKey || e.ctrlKey)) {
      analyzeText()
    }
  })

  document.getElementById("inputUrl")?.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      analyzeUrl()
    }
  })

  // Pattern library links
  document.querySelectorAll('a[data-view="library"]').forEach((link) => {
    link.addEventListener("click", (e) => {
      e.preventDefault()
      navigateTo("library")
    })
  })

  // Pattern library filters
  document.getElementById("filterForm")?.addEventListener("submit", (e) => {
    e.preventDefault()
    filterPatterns()
  })

  document.getElementById("resetFiltersBtn")?.addEventListener("click", () => {
    resetFilters()
  })
})
