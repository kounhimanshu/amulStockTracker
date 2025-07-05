#!/bin/bash

set -e  # Exit if any command fails

echo "🧹 Cleaning up old Docker containers..."
docker ps -aq | xargs -r docker rm -f

echo "🧹 Removing old Docker image..."
docker rmi -f amul-checker || echo "No previous image found."

echo "🔨 Building Docker image..."
docker build -t amul-checker .

echo "🚀 Running Docker container..."
docker run --rm -v "$(pwd)":/app amul-checker
