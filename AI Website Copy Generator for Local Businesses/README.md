# ⚡ CopyForge — AI Website Copy Generator for Local Businesses

A clean, fast web app that generates full website copy (Homepage, About, Services, Why Choose Us, CTA) from a simple form. Powered by FastAPI + Groq (with a built-in simulation fallback).

---

## 📁 Project Structure

```
project/
├── app.py                  # FastAPI backend
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html          # Main HTML page
└── static/
    ├── style.css           # Styles
    └── script.js           # Frontend logic
```

---

## 🚀 How to Run

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 2. (Optional) Add your Groq API Key

If you have a Groq API key, set it as an environment variable:

```bash
# macOS / Linux
export GROQ_API_KEY=your_groq_api_key_here

# Windows (Command Prompt)
set GROQ_API_KEY=your_groq_api_key_here

# Windows (PowerShell)
$env:GROQ_API_KEY="your_groq_api_key_here"
```

> **No key?** No problem. The app automatically uses a built-in simulation that generates realistic copy — great for testing.

### 3. Start the server

```bash
cd project
uvicorn app:app --reload
```

### 4. Open in browser

```
http://localhost:8000
```

---

## 🧠 How It Works

1. User fills in: business type, location, services, target audience, tone
2. Frontend sends a POST request to `/generate`
3. Backend builds a structured prompt and calls Groq API (or falls back to simulation)
4. JSON response is rendered into 5 copy sections with copy-to-clipboard support

---

## 🔑 Getting a Groq API Key (Free)

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up for a free account
3. Navigate to **API Keys** → **Create API Key**
4. Copy the key and set it as `GROQ_API_KEY`

The app uses `llama3-70b-8192` model via Groq's API (fast, free tier available).

---

## ✨ Features

- ⚡ Instant copy generation
- 🎯 5 complete copy sections
- 🗣️ 6 tone options (Professional, Friendly, Casual, Urgent, Premium, Community)
- 📋 Copy individual sections or all at once
- 📱 Mobile responsive
- 🔄 Loading state with cycling messages
- 🛡️ Input validation and error handling
- 🧪 Works without any API key (simulation mode)
