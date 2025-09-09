from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from GKE App! 🎉"

if __name__ == "__main__":
    # Bind to 0.0.0.0 so Kubernetes service can reach it
    app.run(host="0.0.0.0", port=5000, debug=True)
