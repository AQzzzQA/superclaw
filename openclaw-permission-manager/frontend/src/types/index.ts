// User types
export interface User {
  id: string;
  qq_number: string;
  nickname: string;
  avatar_url?: string;
  role: 'admin' | 'user' | 'readonly';
  permissions: string[];
  created_at: string;
  updated_at: string;
}

// Permission types
export interface PermissionTemplate {
  id: string;
  name: string;
  description?: string;
  permissions: string[];
  is_system: boolean;
  created_by?: string;
  created_at: string;
  updated_at: string;
}

// Config types
export interface OpenClawConfig {
  id: string;
  config_name: string;
  config_data: any;
  version: number;
  created_by?: string;
  created_at: string;
  updated_at: string;
}

// API response types
export interface ApiResponse<T> {
  success: boolean;
  data: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T> {
  success: boolean;
  data: T[];
  count: number;
  page: number;
  limit: number;
}

// Auth types
export interface AuthUser {
  id: string;
  qq_number: string;
  nickname: string;
  role: string;
  permissions: string[];
}

// Form types
export interface UserForm {
  qq_number: string;
  nickname: string;
  avatar_url?: string;
  role: 'admin' | 'user' | 'readonly';
  permissions: string[];
}

export interface PermissionTemplateForm {
  name: string;
  description?: string;
  permissions: string[];
  is_system?: boolean;
  created_by?: string;
}

export interface ConfigForm {
  config_name: string;
  config_data: any;
  created_by?: string;
}

// Role types
export type UserRole = 'admin' | 'user' | 'readonly';

// Permission types
export type PermissionType = 
  | 'read'
  | 'write'
  | 'delete'
  | 'manage_users'
  | 'manage_permissions'
  | 'system_config'
  | 'message_send'
  | 'message_view';

// Status types
export type StatusType = 'success' | 'error' | 'warning' | 'info';