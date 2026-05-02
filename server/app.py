import os

from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

from routes.analyze import analyze_bp


def create_app():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    frontend_dist_dir = os.path.abspath(os.path.join(base_dir, "..", "client", "dist"))

    app = Flask(__name__, static_folder=frontend_dist_dir, static_url_path="")

    client_origin = os.getenv("CLIENT_ORIGIN", "http://localhost:3000")
    allowed_origins = [
        client_origin,
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]
    CORS(app, resources={r"/analyze": {"origins": allowed_origins}})

    app.register_blueprint(analyze_bp)

    @app.get("/")
    def serve_index():
        index_path = os.path.join(frontend_dist_dir, "index.html")
        if os.path.exists(index_path):
            return send_from_directory(frontend_dist_dir, "index.html")
        return jsonify({"message": "AI Debug Assistant API is running."})

    @app.get("/<path:path>")
    def serve_frontend(path):
        target_path = os.path.join(frontend_dist_dir, path)
        if os.path.exists(target_path):
            return send_from_directory(frontend_dist_dir, path)

        index_path = os.path.join(frontend_dist_dir, "index.html")
        if os.path.exists(index_path):
            return send_from_directory(frontend_dist_dir, "index.html")

        return jsonify({"error": "Resource not found."}), 404

    @app.get("/health")
    def health_check():
        return jsonify({"status": "ok"})

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify({"error": "Resource not found."}), 404

    @app.errorhandler(500)
    def internal_error(_error):
        return jsonify({"error": "An unexpected server error occurred."}), 500

    return app


app = create_app()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
