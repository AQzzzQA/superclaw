import { UserService } from '../src/services/UserService';
import { PermissionService } from '../src/services/PermissionService';

async function initializeDatabase() {
  console.log('🗄️ Initializing database...');
  
  try {
    const userService = new UserService();
    await userService.initializeDatabase();
    console.log('✅ Database initialized successfully!');
  } catch (error) {
    console.error('❌ Database initialization failed:', error);
    process.exit(1);
  }
}

async function createDefaultTemplates() {
  console.log('📋 Creating default permission templates...');
  
  try {
    const permissionService = new PermissionService();
    
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

async function createDefaultAdmin() {
  console.log('👤 Creating default admin user...');
  
  try {
    const userService = new UserService();
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

async function main() {
  console.log('🚀 Starting OpenClaw Permission Manager database initialization...\n');
  
  await initializeDatabase();
  await createDefaultTemplates();
  await createDefaultAdmin();
  
  console.log('\n🎉 Database initialization completed!');
  console.log('\n📋 Created tables:');
  console.log('   - users (用户表)');
  console.log('   - permission_templates (权限模板表)');
  console.log('   - openclaw_config (配置表)');
  console.log('   - audit_logs (审计日志表)');
  console.log('\n📋 Created default templates:');
  console.log('   - 管理员 (admin template)');
  console.log('   - 普通用户 (user template)');
  console.log('   - 只读用户 (readonly template)');
  console.log('\n👤 Created default admin user:');
  console.log('   - QQ: admin');
  console.log('   - Nickname: 系统管理员');
  console.log('   - Role: admin');
  console.log('\n🚀 You can now start the application!');
}

main().catch(console.error);