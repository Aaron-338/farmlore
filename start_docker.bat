@echo off
echo Testing Docker setup for Pest Management Chatbot...

REM Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Docker is not installed. Please install Docker first.
    exit /b 1
)

REM Check if Docker Compose is installed
where docker-compose >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo Docker Compose is not installed. Please install Docker Compose first.
    exit /b 1
)

echo Building Docker images...
docker-compose build

echo Starting containers...
docker-compose up -d

echo Waiting for services to start...
timeout /t 10 /nobreak

echo Setting up user groups and permissions...
docker-compose exec web python manage.py create_groups

echo All done! The containerized application should be running.
echo To check if it's running, open http://localhost in your browser.
echo To stop the containers, run: docker-compose down 