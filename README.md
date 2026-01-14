# TrustLens

**See Through The Noise.**

TrustLens is a transparent dark pattern detector that analyzes websites to reveal psychological tricks used to manipulate users. Using NLP, regex, and psychology research, it identifies urgency, social proof, fear tactics, framing biases, and more. Empower yourself to make informed decisions online.

---

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [Running the Application](#running-the-application)
- [Inspiration](#inspiration)
- [What TrustLens Does](#what-trustlens-does)
- [Challenges & Solutions](#challenges--solutions)
- [Future Roadmap](#future-roadmap)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

---

## Introduction

Turning 18 and opening my first bank account was a milestone—an exciting step into independence. But that thrill quickly soured as I navigated the online shopping world. Everywhere I looked, websites bombarded me with fake urgency: countdown timers, "only 2 left!" messages, and manipulative offers that pushed me to decide—fast.

That experience sparked a question: _How many others are falling for these tricks, unknowingly?_ 

**TrustLens** was born to answer that question—a tool to uncover and decode the dark patterns embedded in websites and online marketing.

---

## Features

- **Analyzes entire websites** and extracts content in JSON format
- **Detects dark patterns** including urgency tricks, social proof, fear tactics, framing bias, and conversion manipulation
- **Highlights suspicious text** that triggers detection
- **Provides plain-language explanations** of each detected tactic
- **Interactive pattern cards** showing detected manipulation strategies
- **Intent breakdown rings** visualizing psychological intent with smooth animations
- **Text & URL analysis** - paste marketing copy or analyze entire websites
- **Professional, minimal interface** designed for credibility and transparency

---

## Tech Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **Selenium** - Web scraping with JavaScript rendering
- **webdriver-manager** - Automatic ChromeDriver management
- **BeautifulSoup4** - HTML parsing
- **Requests** - HTTP client for URL fetching
- **Uvicorn** - ASGI server

### Frontend
- **HTML5** - Semantic markup
- **CSS3** - Modern styling with custom design tokens
- **Vanilla JavaScript** - Interactive features and API communication
- **Playfair Display & Inter fonts** - Professional typography

### Deployment
- **Frontend:** GitHub Pages
- **Backend:** Render

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ju-pyjanvi/trustlens.git
   cd trustlens
   ```

2. **Create a virtual environment (optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

### Backend (FastAPI + Uvicorn)

Start the backend server:

```bash
uvicorn app.main:app --reload
```

The server will run at `http://localhost:8000`

**Interactive API Documentation:**
- Visit `http://localhost:8000/docs` to test endpoints using Swagger UI
- Visit `http://localhost:8000/redoc` for ReDoc documentation

**Available Endpoints:**
- `POST /analyze-text` - Analyze marketing copy or website text
- `POST /analyze-url` - Analyze an entire website by URL

### Frontend

The frontend is a static HTML/CSS/JS application. To run locally:

1. **Simple method** - Open `app/frontend/index.html` directly in your browser

2. **Better method** - Use a local server:
   ```bash
   # Python 3
   python -m http.server 8080
   # Then visit http://localhost:8080/app/frontend/
   ```

---

## API Usage Examples

### Analyze Text

```bash
curl -X POST "http://localhost:8000/analyze-text" \
  -H "Content-Type: application/json" \
  -d '{"text": "Only 2 rooms left! People are viewing this now"}'
```

### Analyze URL

```bash
curl -X POST "http://localhost:8000/analyze-url" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://www.example.com"}'
```

---

## What TrustLens Does

**TrustLens** is a dark pattern detector that uncovers:

- **Urgency tricks** - "Only 2 left!" countdowns
- **Social proof pressure** - "Join thousands of happy customers!"
- **Fear-based persuasion** - Warnings about missing out
- **Framing bias** - Highlighting benefits while hiding downsides
- **Emotional nudges** - Appeals to guilt or desire
- **Conversion tactics** - Pushy pop-ups, limited-time offers

Using a _transparent, rule-based approach_—powered by NLP, regex logic, and psychology research—TrustLens provides:

- **Pattern cards** explaining each tactic
- **Highlighted text** that triggered detection
- **Plain-language explanations** of what's happening
- **Intent rings** showing the psychological goal

---

## Challenges & Solutions

**Detecting Complex Patterns**
- Required extensive tuning of NLP and regex rules
- Many patterns weren't consistent, so we iterated multiple times to improve accuracy

**Web Scraping**
- Initially used BeautifulSoup, but many sites load content dynamically
- Transitioned to **Selenium** for real-time page data capture
- Steep learning curve but crucial for accurate analysis

**Professional Interface Design**
- Built a clean, minimal interface to convey seriousness
- Avoided gimmicks to maintain credibility and trust

**Performance Optimization**
- Balanced depth of analysis with server response times
- Optimized ring animations and pattern rendering

---

## Future Roadmap

- **Full-site crawling** and behavioral logging
- **Export options** - PDF, CSV, JSON reports
- **Enhanced categorization** with more dark pattern types
- **Browser extension** for real-time detection
- **Expanded reach** to researchers, journalists, watchdogs, and everyday users

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See `LICENSE` for details.

---

## Contact

For questions, feedback, or support, reach out:
- **Email:** janviupreti08@gmail.com

---

## Live Demo

- **Frontend:** https://ju-pyjanvi.github.io/
- **Backend API Docs:** https://trustlens-cutx.onrender.com/docs

---

**Empower yourself to see through manipulation and make informed decisions online with TrustLens.**

_In essence, TrustLens is about restoring trust, one website at a time._
