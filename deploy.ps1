# Deployment script for StaySense AI
# Make sure to install Git first from https://git-scm.com/download/win

Write-Host "=== StaySense AI Deployment Script ===" -ForegroundColor Green
Write-Host ""
Write-Host "Before proceeding, ensure:" -ForegroundColor Yellow
Write-Host "1. Git is installed (https://git-scm.com/download/win)"
Write-Host "2. You have Heroku CLI installed (https://devcenter.heroku.com/articles/heroku-cli)"
Write-Host "3. Your repository is initialized with git"
Write-Host ""

# Get git installation path
$gitPath = "C:\Program Files\Git\bin\git.exe"
if (-not (Test-Path $gitPath)) {
    Write-Host "ERROR: Git not found at $gitPath" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Change to project directory
cd "c:\Users\Sanvie Singh\OneDrive\Desktop\app.py"

Write-Host "Step 1: Configuring Git..." -ForegroundColor Cyan
& $gitPath config user.email "your-email@example.com"
& $gitPath config user.name "Your Name"

Write-Host "Step 2: Adding files..." -ForegroundColor Cyan
& $gitPath add -A

Write-Host "Step 3: Committing changes..." -ForegroundColor Cyan
& $gitPath commit -m "Add CORS support and fix production backend URLs"

Write-Host "Step 4: Pushing to repository..." -ForegroundColor Cyan
& $gitPath push origin main

Write-Host ""
Write-Host "Step 5: Deploy to Heroku (backend)..." -ForegroundColor Cyan
& $gitPath push heroku main

Write-Host ""
Write-Host "✅ Deployment Complete!" -ForegroundColor Green
Write-Host "Frontend: https://your-app.vercel.app" -ForegroundColor Green
Write-Host "Backend: https://your-app-backend.herokuapp.com" -ForegroundColor Green
