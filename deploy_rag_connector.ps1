# PowerShell script to deploy RAG Connector

Write-Host "Deploying RAG Connector for FarmLore" -ForegroundColor Green
Write-Host "===================================" -ForegroundColor Green

# Check if Docker is running
try {
    $null = docker info
} catch {
    Write-Host "Docker is not running. Please start Docker and try again." -ForegroundColor Red
    exit 1
}

# Copy the RAG chat template to the Django templates directory
Write-Host "Copying RAG chat template to Django templates directory..." -ForegroundColor Yellow
$templateDir = "pest-management-chatbot/farmlore-project/chatbot/templates/chatbot/"
if (-not (Test-Path $templateDir)) {
    New-Item -Path $templateDir -ItemType Directory -Force | Out-Null
}
Copy-Item -Path "rag_chat.html" -Destination $templateDir -Force

# Make sure files are available
if (-not ((Test-Path "standalone_rag.py") -and (Test-Path "rag_web_connector.py"))) {
    Write-Host "Required files missing. Please make sure standalone_rag.py and rag_web_connector.py exist." -ForegroundColor Red
    exit 1
}

# Build and start the services
Write-Host "Building and starting services..." -ForegroundColor Yellow
docker-compose build
docker-compose up -d

Write-Host ""
Write-Host "RAG Connector Deployment Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host ""
Write-Host "Access the RAG-enhanced chat at: http://localhost/chatbot/rag-chat/" -ForegroundColor Cyan
Write-Host ""
Write-Host "To verify the RAG connector is working:" -ForegroundColor Cyan
Write-Host "  - Try asking questions about agricultural pests like:" -ForegroundColor Cyan
Write-Host "    - How do I control aphids on my tomato plants?" -ForegroundColor Cyan
Write-Host "    - What pests affect cucumber plants?" -ForegroundColor Cyan
Write-Host "    - How to deal with spider mites in my garden?" -ForegroundColor Cyan
Write-Host ""
Write-Host "To check logs:" -ForegroundColor Cyan
Write-Host "  - docker-compose logs -f rag_connector" -ForegroundColor Cyan
Write-Host "" 