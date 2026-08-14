# Add these imports near the top of app.py
import os
from dotenv import load_dotenv
from flask import jsonify
from ai_service import generate_ai_response

load_dotenv()

# Add this route to app.py
@app.route("/api/ai/analyze", methods=["POST"])
def ai_analyze():
    data = request.get_json(silent=True) or {}
    review = (data.get("review") or "").strip()

    if not review:
        return jsonify({"error": "Review is required"}), 400

    if len(review) > 5000:
        return jsonify({"error": "Review is too long"}), 400

    try:
        result = generate_ai_response(review)
        return jsonify({
            "success": True,
            "review": review,
            "result": result
        }), 200
    except Exception as exc:
        app.logger.exception("AI request failed")
        return jsonify({
            "success": False,
            "error": "AI service is temporarily unavailable"
        }), 502
