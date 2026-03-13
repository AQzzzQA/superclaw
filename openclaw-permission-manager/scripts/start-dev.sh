#!/bin/bash

# OpenClaw Permission Manager - Development Startup Script

echo "🚀 Starting OpenClaw Permission Manager in development mode..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18.0 or higher."
    exit 1
fi

# Check npm version
NPM_VERSION=$(npm --version | cut -d. -f1)
if [ "$NPM_VERSION" -lt 8 ]; then
    echo "❌ npm version is too old. Please install npm 8.0 or higher."
    exit 1
fi

# Install dependencies if not already installed
if [ ! -d "backend/node_modules" ]; then
    echo "📦 Installing backend dependencies..."
    cd backend
    npm install
    cd ..
fi

if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend
    npm install
    cd ..
fi

# Create environment files if they don't exist
if [ ! -f "backend/.env" ]; then
    echo "⚙️ Creating backend environment file..."
    cp backend/.env.example backend/.env
    echo "✅ Backend environment file created. Please review and update if necessary."
fi

if [ ! -f "frontend/.env" ]; then
    echo "⚙️ Creating frontend environment file..."
    cp frontend/.env.example frontend/.env
    echo "✅ Frontend environment file created."
fi

# Initialize database if not exists
if [ ! -f "backend/data/permissions.db" ]; then
    echo "🗄️ Initializing database..."
    cd backend
    npm run init-db
    cd ..
fi

# Start backend in background
echo "🔧 Starting backend server..."
cd backend
npm run dev &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend
echo "🎨 Starting frontend development server..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

echo "✅ Development servers started successfully!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:3001"
echo ""
echo "Press Ctrl+C to stop all servers"

# Function to cleanup on exit
cleanup() {
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID $FRONTEND_PID
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for servers to finish
wait