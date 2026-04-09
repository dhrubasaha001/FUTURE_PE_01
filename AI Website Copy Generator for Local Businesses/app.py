import os
import json
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

app = FastAPI(title="AI Website Copy Generator")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


class BusinessInput(BaseModel):
    business_type: str
    location: str
    services: str
    target_audience: str
    tone: str


def build_prompt(data: BusinessInput) -> str:
    return f"""You are an expert website copywriter specializing in local businesses. 
Write compelling, conversion-focused website copy for the following business.

Business Details:
- Business Type: {data.business_type}
- Location: {data.location}
- Services Offered: {data.services}
- Target Audience: {data.target_audience}
- Desired Tone: {data.tone}

Generate complete website copy with these EXACT sections. Return ONLY valid JSON — no markdown, no backticks, no extra text.

{{
  "homepage": {{
    "headline": "A punchy, memorable headline (max 10 words)",
    "subheadline": "A supporting sentence that clarifies what you do and for whom (max 20 words)",
    "hero_description": "2-3 sentences describing what makes this business special, written in the specified tone. Be specific, not generic."
  }},
  "about": {{
    "title": "About Us section title",
    "body": "3-4 sentences about the business story, values, and commitment to the local community. Make it human and warm."
  }},
  "services": {{
    "title": "Services section title",
    "intro": "One sentence introducing the services",
    "list": [
      {{"name": "Service 1 Name", "description": "1-2 sentence description of this service and its benefit"}},
      {{"name": "Service 2 Name", "description": "1-2 sentence description"}},
      {{"name": "Service 3 Name", "description": "1-2 sentence description"}}
    ]
  }},
  "why_choose_us": {{
    "title": "Why Choose Us section title",
    "points": [
      {{"icon": "✓", "title": "Point 1 Title", "body": "One sentence elaboration"}},
      {{"icon": "✓", "title": "Point 2 Title", "body": "One sentence elaboration"}},
      {{"icon": "✓", "title": "Point 3 Title", "body": "One sentence elaboration"}},
      {{"icon": "✓", "title": "Point 4 Title", "body": "One sentence elaboration"}}
    ]
  }},
  "cta": {{
    "headline": "Urgent, action-oriented headline (max 12 words)",
    "subtext": "1-2 sentences encouraging immediate action. Make it feel low-risk and high-reward.",
    "button_text": "Call-to-action button label (max 5 words)",
    "secondary_text": "A short reassurance line below the button (e.g. no commitment, free consultation)"
  }}
}}

Rules:
- Write in the {data.tone} tone throughout
- Be specific to {data.business_type} in {data.location}
- Avoid clichés like "world-class", "cutting-edge", "passionate team"
- Use natural, conversational language that builds trust
- Focus on customer benefits, not just features
"""


def simulate_copy(data: BusinessInput) -> dict:
    """Fallback simulated response when no API key is available."""
    business = data.business_type
    location = data.location
    audience = data.target_audience

    return {
        "homepage": {
            "headline": f"Trusted {business} Services in {location}",
            "subheadline": f"Helping {audience} get exactly what they need — without the hassle.",
            "hero_description": (
                f"We're a locally rooted {business} serving {location} and the surrounding area. "
                f"Whether you're a first-timer or a returning customer, we make the process simple, "
                f"transparent, and stress-free. Your satisfaction isn't a goal — it's our baseline."
            ),
        },
        "about": {
            "title": f"Who We Are",
            "body": (
                f"We started as a small {business} in {location} with one simple belief: "
                f"good work speaks louder than any advertisement. Over the years, we've built "
                f"a reputation for showing up on time, doing the job right, and treating every "
                f"customer like a neighbour — because most of you are. We're proud to be part of this community."
            ),
        },
        "services": {
            "title": "What We Offer",
            "intro": f"Here's how we help {audience} solve real problems:",
            "list": [
                {
                    "name": data.services.split(",")[0].strip() if "," in data.services else data.services,
                    "description": f"Our core offering, built around what {audience} actually need. No fluff, just results.",
                },
                {
                    "name": "Consultation & Planning",
                    "description": f"We sit down with you, understand your situation, and map out the best path forward — no pressure.",
                },
                {
                    "name": "Ongoing Support",
                    "description": f"We don't disappear after the job's done. Reach out anytime and we'll be there.",
                },
            ],
        },
        "why_choose_us": {
            "title": "Why Locals Choose Us",
            "points": [
                {"icon": "✓", "title": "Local & Accountable", "body": f"We live and work in {location} — our reputation is everything to us."},
                {"icon": "✓", "title": "No Hidden Fees", "body": "You get a clear quote upfront. What we say is what you pay."},
                {"icon": "✓", "title": "Fast Turnaround", "body": "We respect your time. Jobs are completed on schedule, every time."},
                {"icon": "✓", "title": "Real Reviews", "body": f"Hundreds of happy customers in {location} can vouch for our work."},
            ],
        },
        "cta": {
            "headline": f"Ready to Get Started? Let's Talk.",
            "subtext": (
                f"Getting a quote takes less than 5 minutes. We'll listen, give you honest advice, "
                f"and never push you into something you don't need."
            ),
            "button_text": "Book a Free Consultation",
            "secondary_text": "No obligation. No sales pitch. Just straight answers.",
        },
    }


async def call_groq(data: BusinessInput) -> dict:
    """Call Groq API or fall back to simulation."""
    api_key = os.environ.get("GROQ_API_KEY", "")

    if not api_key:
        return simulate_copy(data)

    try:
        import httpx

        prompt = build_prompt(data)
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 2000,
                },
            )
            result = response.json()
            raw = result["choices"][0]["message"]["content"]
            # Strip markdown fences if present
            raw = raw.strip()
            if raw.startswith("```"):
                raw = raw.split("```")[1]
                if raw.startswith("json"):
                    raw = raw[4:]
            return json.loads(raw)
    except Exception as e:
        print(f"Groq API error: {e} — falling back to simulation")
        return simulate_copy(data)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate")
async def generate(data: BusinessInput):
    try:
        copy = await call_groq(data)
        return JSONResponse(content={"success": True, "copy": copy})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)},
        )
