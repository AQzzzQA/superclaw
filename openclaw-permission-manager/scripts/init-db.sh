#!/bin/bash

# OpenClaw Permission Manager - Database Initialization Script

echo "🗄️ Initializing OpenClaw Permission Manager database..."

# Check if we're in the backend directory
if [ ! -f "package.json" ] || [ ! -d "src" ]; then
    echo "❌ Please run this script from the backend directory."
    exit 1
fi

# Install dependencies if not already installed
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

# Create data directory if it doesn't exist
mkdir -p data
mkdir -p uploads

# Initialize database
echo "🔄 Creating database tables..."
node -e "
const { UserService } = require('./src/services/UserService');
const userService = new UserService();

async function init() {
  try {
    await userService.initializeDatabase();
    console.log('✅ Database initialized successfully!');
  } catch (error) {
    console.error('❌ Database initialization failed:', error);
    process.exit(1);
  }
}

init();
"

# Create default permission templates
echo "📋 Creating default permission templates..."
node -e "
const { PermissionService } = require('./src/services/PermissionService');
const permissionService = new PermissionService();

async function createDefaultTemplates() {
  try {
    // Admin template
    await permissionService.createTemplate({
      name: '管理员',
      description: '拥有所有权限的管理员模板',
      permissions: ['read', 'write', 'delete', 'manage_users', 'manage_permissions', 'system_config'],
      is_system: true
    });
    
    // User template
    await permissionService.createTemplate({
      name: '普通用户',
      description: '普通用户基础权限模板',
      permissions: ['read', 'write', 'message_send', 'message_view'],
      is_system: true
    });
    
    // Readonly template
    await permissionService.createTemplate({
      name: '只读用户',
      description: '只读用户权限模板',
      permissions: ['read', 'message_view'],
      is_system: true
    });
    
    console.log('✅ Default permission templates created successfully!');
  } catch (error) {
    console.log('⚠️ Default templates may already exist:', error.message);
  }
}

createDefaultTemplates();
"

# Create default admin user
echo "👤 Creating default admin user..."
node -e "
const { UserService } = require('./src/services/UserService');
const userService = new UserService();

async function createDefaultAdmin() {
  try {
    const admin = await userService.getUserByQQNumber('admin');
    
    if (!admin) {
      await userService.createUser({
        qq_number: 'admin',
        nickname: '系统管理员',
        role: 'admin',
        permissions: ['read', 'write', 'delete', 'manage_users', 'manage_permissions', 'system_config']
      });
      console.log('✅ Default admin user created successfully!');
    } else {
      console.log('✅ Admin user already exists.');
    }
  } catch (error) {
    console.error('❌ Failed to create admin user:', error);
    process.exit(1);
  }
}

createDefaultAdmin();
"

echo "🎉 Database initialization completed!"
echo ""
echo "📋 Created tables:"
echo "   - users (用户表)"
echo "   - permission_templates (权限模板表)"
echo "   - openclaw_config (配置表)"
echo "   - audit_logs (审计日志表)"
echo ""
echo "📋 Created default templates:"
echo "   - 管理员 (admin template)"
echo "   - 普通用户 (user template)"
echo "   - 只读用户 (readonly template)"
echo ""
echo "👤 Created default admin user:"
echo "   - QQ: admin"
echo "   - Nickname: 系统管理员"
echo "   - Role: admin"
echo ""
echo "🚀 You can now start the application!"