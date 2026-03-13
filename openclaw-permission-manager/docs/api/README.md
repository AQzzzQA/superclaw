# API 文档

## 概述

OpenClaw 权限管理系统提供了完整的 RESTful API，用于管理用户、权限模板和配置文件。

## 认证

所有需要认证的 API 都需要在请求头中包含 JWT token：

```
Authorization: Bearer <your-token>
```

## 基础 URL

开发环境：`http://localhost:3001/api`

生产环境：根据部署配置而定

## API 端点

### 1. 认证接口

#### POST /api/auth/login
用户登录（QQ号自动注册）

**请求体：**
```json
{
  "qq_number": "123456789"
}
```

**响应：**
```json
{
  "success": true,
  "message": "Login successful",
  "data": {
    "token": "jwt-token-here",
    "user": {
      "id": "user-id",
      "qq_number": "123456789",
      "nickname": "用户昵称",
      "role": "user",
      "permissions": ["read"]
    }
  }
}
```

#### GET /api/auth/me
获取当前用户信息

**响应：**
```json
{
  "success": true,
  "data": {
    "id": "user-id",
    "qq_number": "123456789",
    "nickname": "用户昵称",
    "role": "user",
    "permissions": ["read"],
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z"
  }
}
```

#### PUT /api/auth/profile
更新用户资料

**请求体：**
```json
{
  "nickname": "新昵称",
  "role": "user",
  "permissions": ["read", "write"]
}
```

### 2. 用户管理接口

#### GET /api/users
获取用户列表

**响应：**
```json
{
  "success": true,
  "data": [
    {
      "id": "user-id",
      "qq_number": "123456789",
      "nickname": "用户昵称",
      "role": "user",
      "permissions": ["read"],
      "created_at": "2024-01-01T00:00:00Z",
      "updated_at": "2024-01-01T00:00:00Z"
    }
  ],
  "count": 1
}
```

#### POST /api/users
创建用户

**请求体：**
```json
{
  "qq_number": "123456789",
  "nickname": "用户昵称",
  "role": "user",
  "permissions": ["read"]
}
```

#### GET /api/users/:id
获取用户详情

#### PUT /api/users/:id
更新用户

**请求体：**
```json
{
  "nickname": "新昵称",
  "role": "admin",
  "permissions": ["read", "write", "delete"]
}
```

#### DELETE /api/users/:id
删除用户

#### GET /api/users/qq/:qq_number
根据QQ号获取用户

### 3. 权限模板接口

#### GET /api/permissions/templates
获取权限模板列表

#### POST /api/permissions/templates
创建权限模板（需要管理员权限）

**请求体：**
```json
{
  "name": "管理员模板",
  "description": "管理员默认权限",
  "permissions": ["read", "write", "delete", "manage_users", "manage_permissions"],
  "is_system": false
}
```

#### GET /api/permissions/templates/:id
获取模板详情

#### PUT /api/permissions/templates/:id
更新模板（需要管理员权限）

#### DELETE /api/permissions/templates/:id
删除模板（需要管理员权限）

### 4. 配置管理接口

#### GET /api/permissions/configs
获取配置列表

#### POST /api/permissions/configs
创建配置（需要管理员权限）

**请求体：**
```json
{
  "config_name": "默认配置",
  "config_data": {
    "version": "1.0.0",
    "features": {
      "allowed": ["read", "write"],
      "denied": ["delete"]
    }
  }
}
```

#### GET /api/permissions/configs/:id
获取配置详情

#### PUT /api/permissions/configs/:id
更新配置（需要管理员权限）

#### DELETE /api/permissions/configs/:id
删除配置（需要管理员权限）

#### GET /api/permissions/generate/:userId
生成用户配置

**响应：**
```json
{
  "success": true,
  "data": {
    "version": "1.0.0",
    "generated_at": "2024-01-01T00:00:00Z",
    "user": {
      "id": "user-id",
      "qq_number": "123456789",
      "nickname": "用户昵称",
      "role": "user"
    },
    "permissions": ["read", "write"],
    "features": {
      "allowed": ["basic_commands", "user_profile"],
      "denied": ["all_commands", "user_management"]
    }
  }
}
```

## 权限系统

### 角色定义

- **admin**: 管理员，拥有所有权限
- **user**: 普通用户，基础权限
- **readonly**: 只读用户，只能查看

### 权限列表

- `read`: 读取权限
- `write`: 写入权限
- `delete`: 删除权限
- `manage_users`: 管理用户
- `manage_permissions`: 管理权限
- `system_config`: 系统配置
- `message_send`: 发送消息
- `message_view`: 查看消息

## 错误响应

所有错误响应都遵循以下格式：

```json
{
  "success": false,
  "error": "错误描述",
  "details": "详细信息（可选）"
}
```

### 常见错误码

- `400`: 请求参数错误
- `401`: 未认证
- `403`: 权限不足
- `404`: 资源不存在
- `500`: 服务器内部错误

## 数据格式

### 用户数据格式

```typescript
interface User {
  id: string;
  qq_number: string;
  nickname: string;
  avatar_url?: string;
  role: 'admin' | 'user' | 'readonly';
  permissions: string[];
  created_at: string;
  updated_at: string;
}
```

### 权限模板格式

```typescript
interface PermissionTemplate {
  id: string;
  name: string;
  description?: string;
  permissions: string[];
  is_system: boolean;
  created_by?: string;
  created_at: string;
  updated_at: string;
}
```

### 配置数据格式

```typescript
interface OpenClawConfig {
  id: string;
  config_name: string;
  config_data: any;
  version: number;
  created_by?: string;
  created_at: string;
  updated_at: string;
}
```