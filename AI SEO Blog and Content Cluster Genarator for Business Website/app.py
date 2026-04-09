import os
import json
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq

load_dotenv()
app = Flask(__name__)
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/generate', methods=['POST'])
def generate_content():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400

    topic = data.get('topic', '')
    business_name = data.get('business_name', '')
    location = data.get('location', '')
    target_audience = data.get('target_audience', '')

    prompt = f"""
    You are an expert SEO Content Strategist. Create a complete AI SEO Blog Pack for '{business_name}' located in '{location}'. 
    The main topic is '{topic}' and the target audience is '{target_audience}'.

    Please respond ONLY with a valid JSON object containing the following keys:
    1. "outline": A complete H1-H3 structure for the blog post (Return as a well-structured string with HTML tags like <ul>, <li>, <h3>).
    2. "blog": The long-form SEO-optimized blog content (Return as a well-structured string using HTML formatting like <h2>, <p> for structure. Make it readable).
    3. "cluster": 3-5 Internal linking ideas and content cluster topics related to the main topic (Return as an HTML list).
    4. "local_seo": Brief actionable tips on how to adapt this for local SEO in {location} (Return as an HTML list or paragraphs).
    
    Ensure the content is helpful, readable, and business-focused. 
    """

    try:
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            response_format={"type": "json_object"}
        )
        response_content = completion.choices[0].message.content
        return jsonify(json.loads(response_content))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
