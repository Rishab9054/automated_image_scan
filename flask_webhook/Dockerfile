# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
# Use --no-cache-dir to reduce image size
# Use --trusted-host pypi.python.org if needed behind certain proxies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container at /app
COPY . .

# Make port 5000 available to the world outside this container
# This matches the port your Flask app runs on
EXPOSE 5000

# Define environment variables (optional, can be set at runtime)
# You'll need to provide these when running the container,
# for example using 'docker run -e GITHUB_TOKEN=your_token ...'
# ENV GITHUB_TOKEN=your_token_here
# ENV GITHUB_REPO=your_repo_here
# ENV GITHUB_OWNER=your_owner_here
# ENV PORT=5000

# Run app.py when the container launches
CMD ["python", "app.py"]