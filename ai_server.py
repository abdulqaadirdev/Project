from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
from dotenv import load_dotenv

# Load API key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = Flask(__name__)
CORS(app)  # Allow frontend requests

@app.route("/api/ai-advisor", methods=["POST"])
def ai_advisor():
    try:
        data = request.get_json()
        user_prompt = data.get("prompt", "")

        if not user_prompt.strip():
            return jsonify({"success": False, "message": "Prompt is empty."})

        # Call OpenAI
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a helpful AI loan advisor for UAE loans."},
                {"role": "user", "content": user_prompt}
            ],
            max_tokens=200
        )

        answer = response.choices[0].message.content.strip()
        return jsonify({"success": True, "response": answer})

    except Exception as e:
        return jsonify({"success": False, "message": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
