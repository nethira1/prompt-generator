from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from groq import Groq
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, template_folder=".", static_folder=".")
CORS(app)

# Get API key from environment
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY environment variable is not set")

client = Groq(api_key=GROQ_API_KEY)

# ==================== API Endpoints ====================

@app.route("/", methods=["GET"])
def index():
    """Serve the HTML UI"""
    return render_template("prompt_generator.html")

@app.route("/api/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "message": "Prompt Generator API is running"})

@app.route("/api/generate-variations", methods=["POST"])
def api_generate_variations():
    """Generate prompt variations using Groq"""
    data = request.json
    base_prompt = data.get("prompt", "")
    num_variations = data.get("num_variations", 5)
    
    if not base_prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    try:
        instruction = f"""You are a world-class prompt engineer. Take this basic prompt and rewrite it into {num_variations} highly optimized versions.

Each variation must:
1. Start with a specific expert role (e.g. "You are a senior data scientist...")
2. Include detailed context and background
3. Give clear, specific instructions
4. Define the exact output format expected
5. Be 3-5x more detailed than the original

Return ONLY a valid JSON array of {num_variations} strings. No markdown, no explanation.
Example: ["Full prompt 1...", "Full prompt 2..."]

Original prompt: {base_prompt}"""

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
        return jsonify({"error": f"JSON parse error: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"API Error: {str(e)}", "error_type": type(e).__name__}), 500

@app.route("/api/test-prompt", methods=["POST"])
def api_test_prompt():
    """Test a prompt with Groq"""
    data = request.json
    prompt = data.get("prompt", "")
    
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    
    try:
        message = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        response = message.choices[0].message.content.strip()
        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": f"API Error: {str(e)}"}), 500

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    host = os.getenv("HOST", "0.0.0.0")
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    
    print("=" * 60)
    print("  Prompt Generator — Powered by Groq")
    print(f"  Running on {host}:{port}")
    print("=" * 60)
    app.run(host=host, port=port, debug=debug_mode)
