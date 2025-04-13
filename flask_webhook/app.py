@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
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
    
    # Print debug info about GitHub API request
    print(f"Sending repository_dispatch to {OWNER}/{REPO} with image: {image}")
    
    response = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/dispatches",
        headers=headers,
        json=payload
    )
    
    print(f"GitHub API response: {response.status_code}")
    if response.status_code != 204:
        print(f"Error response: {response.text}")

    if response.status_code == 204:
        return jsonify({"message": f"Triggered GitHub Action for {image}"}), 200
    else:
        return jsonify({"error": response.text}), 400