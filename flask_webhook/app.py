from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

load_dotenv()
app = Flask(name)

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
REPO = os.getenv("GITHUB_REPO")
OWNER = os.getenv("GITHUB_OWNER")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()

    repo_name = data.get("repository", {}).get("repo_name")
    tag = data.get("push_data", {}).get("tag")
    image = f"{repo_name}:{tag}"

    headers = {
        "Authorization": f"token {GITHUB_TOKEN}",
        "Accept": "application/vnd.github.v3+json"
    }

    payload = {
        "event_type": "docker-image-pushed",
        "client_payload": {
            "image": image
        }
    }

    response = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/dispatches",
        headers=headers,
        json=payload
    )

    if response.status_code == 204:
        return jsonify({"message": f"Triggered GitHub Action for {image}"}), 200
    else:
        return jsonify({"error": response.text}), 400

if name == 'main':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)