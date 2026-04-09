import random
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample predefined hooks for simulation
HOOK_TEMPLATES = [
    "Stop scrolling if you want to fix your {problem} forever.",
    "I tried every {category} product so you don't have to, and this is the only one that worked.",
    "Secret's out! Here is how I solved my {problem} in just 7 days.",
    "If you deal with {problem}, you need to watch this right now."
]

# Sample predefined script structures
SCRIPT_FRAMEWORKS = [
    {
        "framework": "Problem - Agitate - Solution - CTA",
        "script": "Tired of {problem}? I know the feeling. It's frustrating when nothing seems to work and you're just wasting money. That's why I switched to {product_name}. It's a game-changer because {key_feature}. Seriously, my life has been so much easier. Click the link below to get yours today!"
    },
    {
        "framework": "Hook - Story - Offer",
        "script": "I used to struggle with {problem} every single day. I tried everything, but nothing stuck. Then a friend recommended {product_name}. The fact that it has {key_feature} completely blew my mind. Now, I can't imagine my daily routine without it. Grab it now while they still have the 50% discount!"
    }
]

# Sample captions tailored for platform
CAPTIONS = {
    "Instagram": "Say goodbye to {problem}! 👇\n\nMeet your new best friend: {product_name}. With {key_feature}, it's exactly what you need. \n\nTap the link in our bio to shop now! 🛍️✨\n\n#UGC #{category} #{product_name} #Trending",
    "TikTok": "POV: You finally found the solution to {problem}. 🤯 {product_name} is totally worth the hype. Run, don't walk! 🏃‍♀️💨 Link in bio! #{product_name} #TikTokMadeMeBuyIt #Viral",
    "YouTube Shorts": "How {product_name} completely solved my {problem}! 🙌 Watch till the end. Subscribe for more! 👇 Link in the comments! #Shorts #Review"
}

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.form
    product_name = data.get("product_name", "Awesome Product")
    category = data.get("category", "Lifestyle")
    problem = data.get("problem", "daily struggle")
    key_feature = data.get("key_feature", "amazing benefits")
    platform = data.get("platform", "Instagram")
    tone = data.get("tone", "D2C")
    
    # Generate Hooks
    generated_hooks = []
    for _ in range(3):
        hook = random.choice(HOOK_TEMPLATES)
        generated_hooks.append(hook.format(
            problem=problem,
            category=category
        ))
        
    # Generate Scripts
    generated_scripts = []
    for frm in SCRIPT_FRAMEWORKS:
        generated_scripts.append({
            "framework": frm["framework"],
            "script": frm["script"].format(
                problem=problem,
                product_name=product_name,
                key_feature=key_feature
            )
        })
        
    # Generate Caption
    caption_template = CAPTIONS.get(platform, CAPTIONS["Instagram"])
    generated_caption = caption_template.format(
        problem=problem,
        product_name=product_name,
        key_feature=key_feature,
        category=category.replace(" ", "")
    )
    
    # Return data to template
    return render_template(
        "results.html",
        product_name=product_name,
        platform=platform,
        tone=tone,
        hooks=generated_hooks,
        scripts=generated_scripts,
        caption=generated_caption
    )

if __name__ == "__main__":
    app.run(debug=True)
