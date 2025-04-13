from flask import Flask, request, jsonify
import requests
import os
import json

# Initialize the Flask application
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get the JSON data sent from DockerHub
        data = request.json
        
        if not data:
            return jsonify({"status": "error", "message": "Invalid payload"}), 400
        
        # Extract repository and tag information from Docker Hub webhook
        repo_name = data.get("repository", {}).get("repo_name")
        tag = data.get("push_data", {}).get("tag")
        
        # Docker Hub webhook payload typically provides repo_name in the format "username/repository"
        # If it doesn't include the username, make sure to add it
        if "/" not in repo_name:
            repo_owner = data.get("repository", {}).get("namespace", "")
            image = f"{repo_owner}/{repo_name}:{tag}"
        else:
            image = f"{repo_name}:{tag}"
        
        # Print for debugging
        print(f"Docker Hub webhook received for image: {image}")
        
        # Get GitHub token from environment variable
        github_token = os.environ.get('GITHUB_TOKEN')
        github_repo = os.environ.get('GITHUB_REPO')  # format: owner/repo
        
        if not github_token or not github_repo:
            return jsonify({"status": "error", "message": "GitHub configuration missing"}), 500
        
        # Trigger GitHub Actions workflow using repository_dispatch event
        github_url = f"https://api.github.com/repos/{github_repo}/dispatches"
        
        headers = {
            "Authorization": f"token {github_token}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        payload = {
            "event_type": "docker-image-pushed",
            "client_payload": {
                "image": image
            }
        }
        
        response = requests.post(github_url, headers=headers, json=payload)
        
        if response.status_code == 204:
            return jsonify({"status": "success", "message": "GitHub Actions workflow triggered"}), 200
        else:
            print(f"GitHub API Error: {response.status_code} - {response.text}")
            return jsonify({"status": "error", "message": f"Failed to trigger workflow: {response.status_code}"}), 500
            
    except Exception as e:
        print(f"Error processing webhook: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Add a health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy"}), 200

# Run the Flask app if executed directly
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)