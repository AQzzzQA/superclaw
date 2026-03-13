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

export interface PermissionTemplateCreate {
  name: string;
  description?: string;
  permissions: string[];
  is_system?: boolean;
  created_by?: string;
}

export interface PermissionTemplateUpdate {
  name?: string;
  description?: string;
  permissions?: string[];
  is_system?: boolean;
  created_by?: string;
}

export interface OpenClawConfig {
  id: string;
  config_name: string;
  config_data: string;
  version: number;
  created_by?: string;
  created_at: string;
  updated_at: string;
}

export interface OpenClawConfigCreate {
  config_name: string;
  config_data: string;
  created_by?: string;
}

export interface OpenClawConfigUpdate {
  config_name?: string;
  config_data?: string;
  created_by?: string;
}

export interface AuditLog {
  id: string;
  action: string;
  target_type: string;
  target_id?: string;
  user_id?: string;
  changes?: string;
  ip_address?: string;
  user_agent?: string;
  created_at: string;
}