# Task ID: T-017
# Build Automation Script for Local Kubernetes
# This script builds the Docker images and makes them available to Minikube.

Write-Host "Building Backend Image..."
docker build -t hackathon-backend:latest ./backend

Write-Host "Building Frontend Image..."
docker build -t hackathon-frontend:latest ./frontend

Write-Host "Images built successfully."
Write-Host "NOTE: To use these in Minikube, run 'minikube image load hackathon-backend:latest' and 'minikube image load hackathon-frontend:latest'"