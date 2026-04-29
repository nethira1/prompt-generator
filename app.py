from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get API key from environment variable
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set. Please set it in .env file or your system environment.")

client = Groq(api_key=GROQ_API_KEY)

@app.route("/")
def home():
    return jsonify({"message": "Prompt Generator API running!"})

@app.route("/v1/chat/completions", methods=["POST"])
def generate():
    text = None
    try:
        data = request.json
        original_prompt = data.get("prompt", "")
        num_variations = data.get("variations", 5)
        
        if not original_prompt:
            return jsonify({"error": "Prompt is required"}), 400
        
        instruction = f"""You are a world-class prompt engineer. Take this basic prompt and rewrite it into {num_variations} highly optimized versions.

Each variation must:
1. Start with a specific expert role (e.g. "You are a senior data scientist...")
2. Include detailed context and background
3. Give clear, specific instructions
4. Define the exact output format expected
5. Be 3-5x more detailed than the original

Return ONLY a valid JSON array of {num_variations} strings. No markdown, no explanation.
Example: ["Full prompt 1...", "Full prompt 2..."]

Original prompt: {original_prompt}"""

        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": instruction}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        text = message.choices[0].message.content.strip()
        
        # Clean markdown code blocks if present
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        text = text.strip()
        
        # Parse JSON
        variations = json.loads(text)
        
        # Ensure it's a list
        if not isinstance(variations, list):
            variations = [str(variations)]
        
        return jsonify({"variations": variations})
    
    except json.JSONDecodeError as e:
        return jsonify({"error": f"JSON parse error: {str(e)}", "raw_response": text}), 400
    except Exception as e:
        return jsonify({"error": f"API Error: {str(e)}", "error_type": type(e).__name__}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)