import api from './api';

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

export const permissionService = {
  async getAllTemplates(): Promise<{ data: PermissionTemplate[] }> {
    const response = await api.get('/permissions/templates');
    return response;
  },

  async getTemplateById(id: string): Promise<any> {
    const response = await api.get(`/permissions/templates/${id}`);
    return response;
  },

  async createTemplate(data: any): Promise<any> {
    const response = await api.post('/permissions/templates', data);
    return response;
  },

  async updateTemplate(id: string, data: any): Promise<any> {
    const response = await api.put(`/permissions/templates/${id}`, data);
    return response;
  },

  async deleteTemplate(id: string): Promise<any> {
    const response = await api.delete(`/permissions/templates/${id}`);
    return response;
  },

  async getAllConfigs(): Promise<any> {
    const response = await api.get('/permissions/configs');
    return response;
  },

  async getConfigById(id: string): Promise<any> {
    const response = await api.get(`/permissions/configs/${id}`);
    return response;
  },

  async createConfig(data: any): Promise<any> {
    const response = await api.post('/permissions/configs', data);
    return response;
  },

  async updateConfig(id: string, data: any): Promise<any> {
    const response = await api.put(`/permissions/configs/${id}`, data);
    return response;
  },

  async deleteConfig(id: string): Promise<any> {
    const response = await api.delete(`/permissions/configs/${id}`);
    return response;
  },

  async generateOpenClawConfig(userId: string): Promise<any> {
    const response = await api.get(`/permissions/generate/${userId}`);
    return response;
  },
};