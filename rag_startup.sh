#!/bin/bash
# RAG Startup Script for Docker container
# This script should be added to the container startup process

# Set up logging
LOG_FILE="/app/logs/rag_startup.log"
mkdir -p /app/logs

echo "$(date) - Starting RAG integration..." > $LOG_FILE

# Wait for the web service to fully initialize
echo "$(date) - Waiting for web service to initialize (30 seconds)..." >> $LOG_FILE
sleep 30

# Run the RAG injector
echo "$(date) - Running RAG injector..." >> $LOG_FILE
python /app/api_rag_injector.py >> $LOG_FILE 2>&1

# Check if the injector was successful
if [ $? -eq 0 ]; then
    echo "$(date) - RAG integration successful!" >> $LOG_FILE
else
    echo "$(date) - RAG integration failed. Check logs for details." >> $LOG_FILE
fi

# Keep the script running in the background
echo "$(date) - RAG startup script completed" >> $LOG_FILE 