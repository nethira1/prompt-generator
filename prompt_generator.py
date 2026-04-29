from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__, template_folder=".", static_folder=".")

# Gemini API backend endpoint
BACKEND_URL = "http://127.0.0.1:5000/v1/chat/completions"

def generate_prompt_variations(base_prompt: str, num_variations: int = 5) -> list:
    """Use Gemini backend to generate prompt variations."""
    try:
        response = requests.post(
            BACKEND_URL,
            json={"prompt": base_prompt, "variations": num_variations},
            timeout=60
        )
        if response.status_code == 200:
            result = response.json()
            variations = result.get("variations", [])
            if isinstance(variations, list) and variations:
                return variations
        return ["Error: Failed to generate variations"]
    except Exception as e:
        return [f"Error connecting to backend: {str(e)}"]

def test_prompt_with_gemini(prompt: str) -> str:
    """Test a prompt by sending it to Gemini directly via the backend."""
    try:
        response = requests.post(
            BACKEND_URL,
            json={"prompt": prompt, "variations": 1},
            timeout=60
        )
        if response.status_code == 200:
            result = response.json()
            variations = result.get("variations", [])
            return variations[0] if variations else "No response"
        return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route("/", methods=["GET"])
def index():
    return render_template("prompt_generator.html")

@app.route("/api/generate-variations", methods=["POST"])
def api_generate_variations():
    data = request.json
    base_prompt = data.get("prompt", "")
    num_variations = data.get("num_variations", 5)
    if not base_prompt:
        return jsonify({"error": "Prompt is required"}), 400
    variations = generate_prompt_variations(base_prompt, num_variations)
    return jsonify({"variations": variations})

@app.route("/api/test-prompt", methods=["POST"])
def api_test_prompt():
    data = request.json
    prompt = data.get("prompt", "")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400
    response = test_prompt_with_gemini(prompt)
    return jsonify({"response": response})

if __name__ == "__main__":
    print("=" * 60)
    print("  Prompt Generator — Powered by Gemini")
    print("  UI:       http://127.0.0.1:3001")
    print("  Backend:  http://127.0.0.1:5000")
    print("=" * 60)
    app.run(host="127.0.0.1", port=3001, debug=True)