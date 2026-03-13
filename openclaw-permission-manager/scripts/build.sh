#!/bin/bash

# OpenClaw Permission Manager - Build Script

echo "🔨 Building OpenClaw Permission Manager..."

# Check if we're in the project root directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Please run this script from the project root directory."
    exit 1
fi

# Build frontend
echo "🎨 Building frontend..."
cd frontend

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    npm install
fi

# Build frontend
echo "🏗️ Building frontend application..."
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Frontend build failed!"
    exit 1
fi

cd ..

# Build backend
echo "🔧 Building backend..."
cd backend

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "📦 Installing backend dependencies..."
    npm install
fi

# Build backend
echo "🏗️ Building backend application..."
npm run build
if [ $? -ne 0 ]; then
    echo "❌ Backend build failed!"
    exit 1
fi

cd ..

# Create build directory
mkdir -p dist

# Copy built files
echo "📁 Copying built files..."
cp -r frontend/build dist/frontend
cp -r backend/dist dist/backend
cp -r docker-compose.yml dist/
cp -r docs dist/

# Create startup script for production
cat > dist/start.sh << 'EOF'
#!/bin/bash

# OpenClaw Permission Manager - Production Startup Script

echo "🚀 Starting OpenClaw Permission Manager in production mode..."

# Start backend
echo "🔧 Starting backend server..."
cd backend
npm start &
BACKEND_PID=$!

# Start frontend with nginx (if needed)
# For this example, we assume frontend is served separately

echo "✅ Production server started!"
echo "🔧 Backend API: http://localhost:3001"
echo ""
echo "Press Ctrl+C to stop the server"

# Function to cleanup on exit
cleanup() {
    echo "🛑 Stopping server..."
    kill $BACKEND_PID
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for server to finish
wait
EOF

# Make startup script executable
chmod +x dist/start.sh

echo "✅ Build completed successfully!"
echo "📁 Build files are available in the 'dist' directory"
echo "🚀 To start in production mode, run:"
echo "   cd dist && ./start.sh"