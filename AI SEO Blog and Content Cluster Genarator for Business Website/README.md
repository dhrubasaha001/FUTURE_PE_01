# AI SEO Blog & Content Cluster Generator

A high-performing, AI-powered web application designed to automatically formulate high-converting SEO strategies, Blog Outlines, and Content Clusters for business websites using the bleeding-fast Groq AI API.

## Features

- **SEO Blog Outlines**: Instantly generates structurally perfect (H1-H3) outlines optimized for user intent.
- **Long-Form Blogs**: Formulates fully-written SEO blog posts ready for publishing.
- **Content Clusters**: Creates intelligent internal linking ideas and semantic content cluster webs.
- **Local SEO Adaptations**: Automatically adapts the content strategy for local businesses (City + Service mapping).
- **Stunning UI**: Features a modern, responsive Glassmorphism design built purely with beautiful CSS and JavaScript.
- **Speed**: Powered natively by the powerful `llama-3.3-70b-versatile` model via Groq API.

## Tech Stack

- **Backend**: Python, Flask, Python-Dotenv
- **Frontend**: HTML5, CSS3 (Custom Glassmorphism theme), Vanilla JS.
- **AI Integration**: Groq Python SDK

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd "AI SEO Blog and Content Cluster Generator for Business Website"
   ```

2. **Setup your environment:**
   Create a `.env` file in the root directory and add your Groq API Key:
   ```env
   GROQ_API_KEY=your_actual_api_key_here
   ```

3. **Install Dependencies:**
   Ensure you have Python installed, then install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application:**
   ```bash
   python app.py
   ```
   *The application will start securely on `http://127.0.0.1:5000/`*

## How to Use

1. Navigate to the local web app address in your browser (`http://127.0.0.1:5000/`).
2. Enter your campaign specifics:
    - **Topic / Keyword:** The central theme or keyword (e.g., *Emergency AC Repair*).
    - **Business Name:** Your local or digital business entity's name (e.g., *Austin HVAC Experts*).
    - **Target Location / City:** The target demographic region.
    - **Target Audience:** Brief description of your ideal clientele (e.g., *Homeowners needing quick repairs*).
3. Click **Generate SEO Pack**. 
4. The system will hit the Groq infrastructure and immediately structure out the response, dynamically populating the strategy under the four dedicated viewing tabs!

## Project Structure

```text
├── app.py                  # Main Flask application and API integration
├── requirements.txt        # Python Dependencies (Flask, Groq, Dotenv)
├── .env                    # Environment file (must create yourself)
├── static/
│   ├── css/style.css       # Premium Glassmorphism styling and animations
│   └── js/script.js        # Fetch API form handler and Tab switching UI logic
└── templates/
    └── index.html          # Main HTML5 structure for the single page app
```
