#!/bin/bash

set -e  # Exit if any command fails

echo "🧹 Cleaning up old Docker containers..."
docker ps -aq | xargs -r docker rm -f

echo "🧹 Removing old Docker image..."
docker rmi -f amul-stock-tracker || echo "No previous image found."

echo "🔨 Building Docker image..."
docker buildx build --network=host -t amul-stock-tracker .

echo "🚀 Running Docker container..."
docker run --rm --network=host --env-file .env amul-stock-tracker 
