export const config = {
  // Server
  port: process.env.PORT || 3001,
  nodeEnv: process.env.NODE_ENV || 'development',
  
  // Frontend URL
  frontendUrl: process.env.FRONTEND_URL || 'http://localhost:3000',
  
  // Security
  jwtSecret: process.env.JWT_SECRET || 'your-secret-key-change-in-production',
  jwtExpiresIn: process.env.JWT_EXPIRES_IN || '7d',
  
  // Database
  dbPath: process.env.DB_PATH || './data/permissions.db',
  
  // File upload
  maxUploadSize: process.env.MAX_UPLOAD_SIZE ? parseInt(process.env.MAX_UPLOAD_SIZE) : 10 * 1024 * 1024, // 10MB
  uploadPath: process.env.UPLOAD_PATH || './uploads',
  
  // QQ Bot integration
  qqBotToken: process.env.QQ_BOT_TOKEN,
  qqBotUrl: process.env.QQ_BOT_URL,
  
  // Default roles and permissions
  defaultRoles: ['admin', 'user', 'readonly'],
  defaultPermissions: {
    admin: ['read', 'write', 'delete', 'manage_users', 'manage_permissions'],
    user: ['read', 'write'],
    readonly: ['read']
  }
};