#!/bin/bash

# OpenClaw Permission Manager - Project Validation Script

echo "🔍 Validating OpenClaw Permission Manager project structure..."

# Check if we're in the project root directory
if [ ! -d "backend" ] || [ ! -d "frontend" ]; then
    echo "❌ Please run this script from the project root directory."
    exit 1
fi

# Check backend structure
echo "📁 Checking backend structure..."
cd backend

REQUIRED_BACKEND_FILES=(
    "package.json"
    "tsconfig.json"
    "src/index.ts"
    "src/config/database.ts"
    "src/config/env.ts"
    "src/models/User.ts"
    "src/models/Permission.ts"
    "src/models/Auth.ts"
    "src/controllers/UserController.ts"
    "src/controllers/PermissionController.ts"
    "src/controllers/AuthController.ts"
    "src/services/UserService.ts"
    "src/services/PermissionService.ts"
    "src/routes/auth.ts"
    "src/routes/users.ts"
    "src/routes/permissions.ts"
    "src/routes/templates.ts"
    "src/routes/config.ts"
    "src/middleware/auth.ts"
    "src/middleware/role.ts"
    "src/middleware/validation.ts"
    "src/utils/Logger.ts"
    "src/utils/ResponseHelper.ts"
    ".env.example"
    "Dockerfile"
    "README.md"
)

for file in "${REQUIRED_BACKEND_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing backend file: $file"
        exit 1
    fi
done

echo "✅ Backend structure is valid"
cd ..

# Check frontend structure
echo "📁 Checking frontend structure..."
cd frontend

REQUIRED_FRONTEND_FILES=(
    "package.json"
    "tsconfig.json"
    "src/index.tsx"
    "src/App.tsx"
    "src/pages/LoginPage.tsx"
    "src/pages/Dashboard.tsx"
    "src/pages/UserManagement.tsx"
    "src/pages/PermissionTemplates.tsx"
    "src/pages/ConfigManagement.tsx"
    "src/components/Header.tsx"
    "src/services/api.ts"
    "src/services/authService.ts"
    "src/services/userService.ts"
    "src/services/permissionService.ts"
    "src/services/configService.ts"
    "src/types/index.ts"
    "public/index.html"
    "Dockerfile"
    "nginx.conf"
    "README.md"
)

for file in "${REQUIRED_FRONTEND_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing frontend file: $file"
        exit 1
    fi
done

echo "✅ Frontend structure is valid"
cd ..

# Check documentation
echo "📁 Checking documentation..."
REQUIRED_DOCS=(
    "docs/api/README.md"
    "docs/installation/README.md"
    "docs/usage/README.md"
    "README.md"
)

for file in "${REQUIRED_DOCS[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing documentation: $file"
        exit 1
    fi
done

echo "✅ Documentation is complete"

# Check scripts
echo "📁 Checking scripts..."
cd scripts

REQUIRED_SCRIPTS=(
    "start-dev.sh"
    "init-db.sh"
    "build.sh"
    "validate-project.sh"
)

for file in "${REQUIRED_SCRIPTS[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing script: $file"
        exit 1
    fi
done

echo "✅ Scripts are complete"
cd ..

# Check Docker configuration
echo "📁 Checking Docker configuration..."
if [ ! -f "docker-compose.yml" ]; then
    echo "❌ Missing docker-compose.yml"
    exit 1
fi

echo "✅ Docker configuration is complete"

# Check environment configuration
echo "📁 Checking environment configuration..."
if [ ! -f "backend/.env.example" ]; then
    echo "❌ Missing backend environment example"
    exit 1
fi

if [ ! -f "frontend/.env.example" ]; then
    echo "❌ Missing frontend environment example"
    exit 1
fi

echo "✅ Environment configuration is complete"

# Count total files and directories
TOTAL_FILES=$(find . -type f -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.json" -o -name "*.md" | wc -l)
TOTAL_DIRS=$(find . -type d | wc -l)

echo ""
echo "🎉 Project validation completed successfully!"
echo "📊 Statistics:"
echo "   - Total files: $TOTAL_FILES"
echo "   - Total directories: $TOTAL_DIRS"
echo ""
echo "📁 Project structure:"
echo "   - Backend: ✅ Complete"
echo "   - Frontend: ✅ Complete"
echo "   - Documentation: ✅ Complete"
echo "   - Scripts: ✅ Complete"
echo "   - Docker: ✅ Complete"
echo ""
echo "🚀 OpenClaw Permission Manager is ready to use!"
echo ""
echo "Quick start:"
echo "   ./scripts/start-dev.sh"