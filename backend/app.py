from flask import Flask, jsonify, send_from_directory
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="/")

@app.route("/")
def index():
    return send_from_directory("../frontend", "index.html")

@app.route("/api/hello")
def hello():
    return jsonify({"message": "Hello from Flask backend 🚀 running on GKE!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
