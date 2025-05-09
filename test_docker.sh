#!/bin/bash

set -e

echo "Testing Docker setup for Pest Management Chatbot..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

echo "Building Docker images..."
docker-compose build

echo "Starting containers..."
docker-compose up -d

echo "Waiting for services to start..."
sleep 10

echo "Setting up user groups and permissions..."
docker-compose exec -T web python manage.py create_groups

echo "Checking web service..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:80 | grep -q "200"; then
    echo "Web service is running."
else
    echo "Web service is not running properly."
    echo "Checking logs..."
    docker-compose logs web
    exit 1
fi

echo "All tests passed! The containerized application is running correctly."
echo "To stop the containers, run: docker-compose down" 