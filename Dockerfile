# Use Python 3.9 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the script
COPY main.py .

# Create a configuration directory for GitHub token
RUN mkdir -p /config

# Environment variable for GitHub token
ENV GITHUB_TOKEN=""

# Create volume for output
VOLUME ["/app/output"]

# Set entrypoint
ENTRYPOINT ["python3", "main.py"]