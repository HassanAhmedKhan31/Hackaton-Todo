# Task ID: T-017
# Build Script for Hackathon Todo Images

Write-Host "Building Hackathon Todo Images..." -ForegroundColor Cyan

# Build Backend Image
Write-Host "Building Backend Image..." -ForegroundColor Yellow
docker build -t hackathon-backend:latest -f backend/Dockerfile backend/

# Build Frontend Image
Write-Host "Building Frontend Image..." -ForegroundColor Yellow
docker build -t hackathon-frontend:latest -f frontend/Dockerfile frontend/

Write-Host "Images built successfully!" -ForegroundColor Green
