#!/bin/bash

# QR Contact App - Run Script
# Starts both backend and frontend servers

echo "🚀 Starting QR Contact App..."
echo "=============================="

# Activate virtual environment
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found. Run ./setup.sh first"
    exit 1
fi

source venv/bin/activate

# Check if MongoDB is running
echo "Checking MongoDB connection..."
python3 -c "from pymongo import MongoClient; MongoClient('mongodb://localhost:27017', serverSelectionTimeoutMS=2000).server_info()" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "⚠️  Warning: MongoDB doesn't seem to be running locally"
    echo "   Make sure MongoDB is running or update MONGODB_URL in .env"
    echo ""
fi

# Create a temporary directory for logs
LOG_DIR=".logs"
mkdir -p $LOG_DIR

echo ""
echo "Starting services..."
echo "🔵 Backend will run on: http://localhost:8000"
echo "🟢 Frontend will run on: http://localhost:8001"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo "-----------------------------------"
echo ""

# Start backend in background
cd backend
python main.py > "../$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
echo "✓ Backend started (PID: $BACKEND_PID)"

# Start frontend in background
cd ../frontend
python3 -m http.server 8001 > "../$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
echo "✓ Frontend started (PID: $FRONTEND_PID)"

cd ..

# Wait for servers to start
sleep 2

# Check if servers are running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Backend failed to start. Check logs:"
    cat "$LOG_DIR/backend.log"
    exit 1
fi

if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "❌ Frontend failed to start. Check logs:"
    cat "$LOG_DIR/frontend.log"
    exit 1
fi

echo ""
echo "✅ All services started successfully!"
echo ""
echo "Open your browser and go to: http://localhost:8001"
echo ""

# Function to cleanup
cleanup() {
    echo ""
    echo "Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    wait $BACKEND_PID $FRONTEND_PID 2>/dev/null
    echo "✓ Services stopped"
    exit 0
}

# Set up trap to catch Ctrl+C
trap cleanup SIGINT SIGTERM

# Keep script running
wait
