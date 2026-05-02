from flask import Blueprint, jsonify, request

from services.ai_service import AIServiceError, analyze_debug_issue

analyze_bp = Blueprint("analyze", __name__)


@analyze_bp.post("/analyze")
def analyze():
    payload = request.get_json(silent=True) or {}

    code = (payload.get("code") or "").strip()
    error = (payload.get("error") or "").strip()
    language = (payload.get("language") or "").strip()

    if not code or not error or not language:
        return (
            jsonify(
                {
                    "error": "The fields 'code', 'error', and 'language' are required."
                }
            ),
            400,
        )

    try:
        result = analyze_debug_issue(code=code, error=error, language=language)
        return jsonify(result)
    except AIServiceError as exc:
        return jsonify({"error": str(exc)}), 502
    except Exception:
        return jsonify({"error": "Unable to analyze the submitted issue right now."}), 500
