#!/bin/bash

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Install test dependencies if not already installed
pip install pytest pytest-django pytest-asyncio

# Run the tests
pytest api/tests/test_integration.py -v
