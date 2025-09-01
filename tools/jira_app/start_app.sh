#!/bin/bash
# Startup script for Global Underwriting Jira Integration App
# This ensures we use the correct Python version with Flask installed

echo "🚀 Starting Global Underwriting Jira Integration App..."
echo "================================================================"

# Change to the app directory
cd "$(dirname "$0")"

# Check if Python 3.11 is available (where Flask is installed)
if command -v python3.11 &> /dev/null; then
    echo "✅ Using Python 3.11 (recommended)"
    python3.11 app.py
elif command -v python3 &> /dev/null; then
    echo "⚠️  Using system Python 3 - you may need to install Flask"
    python3 app.py
else
    echo "❌ No Python 3 found! Please install Python 3.11 or later."
    exit 1
fi