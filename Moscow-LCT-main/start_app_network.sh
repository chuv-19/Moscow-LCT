#!/bin/bash
# Launch Tree Detection Web App with Network Access

echo "===================================="
echo "   Tree Detection System"
echo "   Network Access Enabled"
echo "===================================="
echo ""

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
elif [ -d ".venv" ]; then
    echo "Activating virtual environment..."
    source .venv/bin/activate
else
    echo "⚠️  Virtual environment not found. Using system Python."
fi

echo ""
echo "Starting web application..."
echo ""
echo "Access from:"
echo "  - This computer: http://localhost:8501"
echo "  - Your phone: Check the Network URL below"
echo ""
echo "Make sure your phone is on the same WiFi network!"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

streamlit run app.py --server.address=0.0.0.0 --server.port=8501
