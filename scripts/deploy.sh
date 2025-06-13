#!/bin/bash

# Aurora Nowcast NZ - Deployment Script
# This script helps with local testing and manual deployment

set -e # Exit on any error

echo "🌌 Aurora Nowcast NZ - Deployment Script"
echo "========================================"

# Check if we're in the project root
if [ ! -f "backend/requirements.txt" ]; then
    echo "❌ Please run this script from the project root directory"
    exit 1
fi

# Function to check command availability
check_command() {
    if ! command -v $1 &>/dev/null; then
        echo "❌ $1 is not installed. Please install it first."
        exit 1
    fi
}

# Check dependencies
echo "🔍 Checking dependencies..."
check_command python3
check_command pip

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "🐍 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install/update dependencies
echo "📦 Installing Python dependencies..."
pip install -r backend/requirements.txt

# Test the system
echo "🧪 Running tests..."
cd backend
python test_geonet.py

# Check test results
if [ $? -eq 0 ]; then
    echo "✅ Tests passed! Generating status data..."

    # Generate status data
    python geonet_data.py

    if [ -f "../docs/status.json" ]; then
        echo "✅ Status data generated successfully!"
        echo "📊 Status file size: $(du -h ../docs/status.json | cut -f1)"

        # Show preview of the data
        echo "📋 Data preview:"
        head -20 ../docs/status.json

        echo ""
        echo "🚀 Ready for deployment!"
        echo ""
        echo "Next steps:"
        echo "1. Commit and push to trigger GitHub Actions"
        echo "2. Visit GitHub Pages site to see live app"
        echo "3. Or serve locally with: python -m http.server 8000 (from docs/ directory)"

    else
        echo "❌ Failed to generate status.json"
        exit 1
    fi
else
    echo "❌ Tests failed. Please check the output above."
    exit 1
fi

cd ..

echo ""
echo "🎉 Deployment preparation complete!"
