import { PermissionTemplate, PermissionTemplateCreate, PermissionTemplateUpdate, OpenClawConfig, OpenClawConfigCreate, OpenClawConfigUpdate } from '../models/Permission';
import { UserService } from './UserService';
import { v4 as uuidv4 } from 'uuid';
import sqlite3 from 'sqlite3';
import path from 'path';

export class PermissionService {
  private db: sqlite3.Database;
  private userService: UserService;

  constructor() {
    this.db = new sqlite3.Database(path.join(__dirname, '../../data/permissions.db'));
    this.userService = new UserService();
  }

  // Permission Templates
  async getAllTemplates(): Promise<PermissionTemplate[]> {
    return new Promise((resolve, reject) => {
      this.db.all('SELECT * FROM permission_templates ORDER BY created_at DESC', (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows);
        }
      });
    });
  }

  async getTemplateById(id: string): Promise<PermissionTemplate | null> {
    return new Promise((resolve, reject) => {
      this.db.get('SELECT * FROM permission_templates WHERE id = ?', [id], (err, row) => {
        if (err) {
          reject(err);
        } else {
          resolve(row || null);
        }
      });
    });
  }

  async createTemplate(templateData: PermissionTemplateCreate): Promise<PermissionTemplate> {
    return new Promise((resolve, reject) => {
      const id = uuidv4();
      const createdAt = new Date().toISOString();
      const updatedAt = createdAt;
      
      const sql = `
        INSERT INTO permission_templates (id, name, description, permissions, is_system, created_by, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
      `;
      
      const params = [
        id,
        templateData.name,
        templateData.description || null,
        JSON.stringify(templateData.permissions),
        templateData.is_system ? 1 : 0,
        templateData.created_by || null,
        createdAt,
        updatedAt
      ];
      
      this.db.run(sql, params, function(err) {
        if (err) {
          reject(err);
        } else {
          resolve({
            id,
            name: templateData.name,
            description: templateData.description,
            permissions: templateData.permissions,
            is_system: templateData.is_system || false,
            created_by: templateData.created_by,
            created_at: createdAt,
            updated_at: updatedAt
          });
        }
      });
    });
  }

  async updateTemplate(id: string, updateData: PermissionTemplateUpdate): Promise<PermissionTemplate | null> {
    return new Promise((resolve, reject) => {
      const fields = [];
      const values = [];
      const updatedAt = new Date().toISOString();
      
      if (updateData.name !== undefined) {
        fields.push('name = ?');
        values.push(updateData.name);
      }
      if (updateData.description !== undefined) {
        fields.push('description = ?');
        values.push(updateData.description);
      }
      if (updateData.permissions !== undefined) {
        fields.push('permissions = ?');
        values.push(JSON.stringify(updateData.permissions));
      }
      if (updateData.is_system !== undefined) {
        fields.push('is_system = ?');
        values.push(updateData.is_system ? 1 : 0);
      }
      if (updateData.created_by !== undefined) {
        fields.push('created_by = ?');
        values.push(updateData.created_by);
      }
      
      if (fields.length === 0) {
        resolve(this.getTemplateById(id));
        return;
      }
      
      fields.push('updated_at = ?');
      values.push(updatedAt);
      values.push(id);
      
      const sql = `UPDATE permission_templates SET ${fields.join(', ')} WHERE id = ?`;
      
      this.db.run(sql, values, function(err) {
        if (err) {
          reject(err);
        } else {
          if (this.changes === 0) {
            resolve(null);
          } else {
            resolve(this.getTemplateById(id));
          }
        }
      });
    });
  }

  async deleteTemplate(id: string): Promise<boolean> {
    return new Promise((resolve, reject) => {
      this.db.run('DELETE FROM permission_templates WHERE id = ?', [id], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve(this.changes > 0);
        }
      });
    });
  }

  // OpenClaw Config
  async getAllConfigs(): Promise<OpenClawConfig[]> {
    return new Promise((resolve, reject) => {
      this.db.all('SELECT * FROM openclaw_config ORDER BY created_at DESC', (err, rows) => {
        if (err) {
          reject(err);
        } else {
          resolve(rows);
        }
      });
    });
  }

  async getConfigById(id: string): Promise<OpenClawConfig | null> {
    return new Promise((resolve, reject) => {
      this.db.get('SELECT * FROM openclaw_config WHERE id = ?', [id], (err, row) => {
        if (err) {
          reject(err);
        } else {
          resolve(row || null);
        }
      });
    });
  }

  async createConfig(configData: OpenClawConfigCreate): Promise<OpenClawConfig> {
    return new Promise((resolve, reject) => {
      const id = uuidv4();
      const createdAt = new Date().toISOString();
      const updatedAt = createdAt;
      
      const sql = `
        INSERT INTO openclaw_config (id, config_name, config_data, version, created_by, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
      `;
      
      const params = [
        id,
        configData.config_name,
        JSON.stringify(configData.config_data),
        1,
        configData.created_by || null,
        createdAt,
        updatedAt
      ];
      
      this.db.run(sql, params, function(err) {
        if (err) {
          reject(err);
        } else {
          resolve({
            id,
            config_name: configData.config_name,
            config_data: configData.config_data,
            version: 1,
            created_by: configData.created_by,
            created_at: createdAt,
            updated_at: updatedAt
          });
        }
      });
    });
  }

  async updateConfig(id: string, updateData: OpenClawConfigUpdate): Promise<OpenClawConfig | null> {
    return new Promise((resolve, reject) => {
      const fields = [];
      const values = [];
      const updatedAt = new Date().toISOString();
      
      if (updateData.config_name !== undefined) {
        fields.push('config_name = ?');
        values.push(updateData.config_name);
      }
      if (updateData.config_data !== undefined) {
        fields.push('config_data = ?');
        values.push(JSON.stringify(updateData.config_data));
      }
      if (updateData.created_by !== undefined) {
        fields.push('created_by = ?');
        values.push(updateData.created_by);
      }
      
      if (fields.length === 0) {
        resolve(this.getConfigById(id));
        return;
      }
      
      fields.push('updated_at = ?');
      values.push(updatedAt);
      values.push(id);
      
      const sql = `UPDATE openclaw_config SET ${fields.join(', ')} WHERE id = ?`;
      
      this.db.run(sql, values, function(err) {
        if (err) {
          reject(err);
        } else {
          if (this.changes === 0) {
            resolve(null);
          } else {
            resolve(this.getConfigById(id));
          }
        }
      });
    });
  }

  async deleteConfig(id: string): Promise<boolean> {
    return new Promise((resolve, reject) => {
      this.db.run('DELETE FROM openclaw_config WHERE id = ?', [id], function(err) {
        if (err) {
          reject(err);
        } else {
          resolve(this.changes > 0);
        }
      });
    });
  }

  async generateOpenClawConfig(userId: string): Promise<any> {
    try {
      const user = await this.userService.getUserById(userId);
      if (!user) {
        throw new Error('User not found');
      }

      const permissions = JSON.parse(user.permissions);
      const template = await this.getTemplateById(user.role);

      const config = {
        version: "1.0.0",
        generated_at: new Date().toISOString(),
        user: {
          id: user.id,
          qq_number: user.qq_number,
          nickname: user.nickname,
          role: user.role
        },
        permissions: permissions,
        template: template ? {
          name: template.name,
          permissions: template.permissions
        } : null,
        features: {
          allowed: this.getEnabledFeatures(permissions),
          denied: this.getDisabledFeatures(permissions)
        }
      };

      return config;
    } catch (error) {
      throw new Error(`Failed to generate OpenClaw config: ${error}`);
    }
  }

  private getEnabledFeatures(permissions: string[]): string[] {
    const featureMapping: Record<string, string[]> = {
      admin: ['all_commands', 'user_management', 'permission_management', 'system_config'],
      user: ['basic_commands', 'user_profile', 'message_send'],
      readonly: ['read_only', 'message_view']
    };

    const features: string[] = [];
    permissions.forEach(permission => {
      if (featureMapping[permission]) {
        features.push(...featureMapping[permission]);
      }
    });

    return Array.from(new Set(features));
  }

  private getDisabledFeatures(permissions: string[]): string[] {
    const allFeatures = ['all_commands', 'user_management', 'permission_management', 'system_config', 'basic_commands', 'user_profile', 'message_send', 'read_only', 'message_view'];
    const enabledFeatures = this.getEnabledFeatures(permissions);
    
    return allFeatures.filter(feature => !enabledFeatures.includes(feature));
  }
}