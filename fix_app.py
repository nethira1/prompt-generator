 code = """from flask import Flask, request, jsonify
from flask_cors import CORS
import google.genai as genai
import json

app = Flask(__name__)
CORS(app)

client = genai.Client(api_key="AIzaSyDNXOD6ScWtKRFr3LaLe7SdCjw5g_uGX7E")

@app.route("/")
def home():
    return jsonify({"message": "Prompt Generator API running!"})

@app.route("/v1/chat/completions", methods=["POST"])
def generate():
    data = request.json
    original_prompt = data.get("prompt", "")
    num_variations = data.get("variations", 5)
    instruction = f\"\"\"You are a world-class prompt engineer. Your task is to take a basic prompt and rewrite it into {num_variations} highly optimized, professional versions.

Each variation must:
1. Start with a specific expert role (e.g. "You are a senior data scientist...")
2. Include detailed context and background
3. Give clear, specific instructions
4. Define the exact output format expected
5. Be 3-5x more detailed than the original

Return ONLY a valid JSON array of {num_variations} strings. No markdown. No explanation.

Original prompt: {original_prompt}\"\"\"

    response = client.models.generate_content(model="gemini-2.0-flash", contents=instruction)
    text = response.text.strip()
    if "```" in text:
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    variations = json.loads(text.strip())
    return jsonify({"variations": variations})

if __name__ == "__main__":
    app.run(port=5000, debug=True)
"""

with open("app.py", "w", encoding="utf-8") as f:
    f.write(code)
print("app.py updated successfully!")
