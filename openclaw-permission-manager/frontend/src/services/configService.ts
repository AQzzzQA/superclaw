import api from './api';

export interface OpenClawConfig {
  id: string;
  config_name: string;
  config_data: any;
  version: number;
  created_by?: string;
  created_at: string;
  updated_at: string;
}

export const configService = {
  async getAllConfigs(): Promise<{ data: OpenClawConfig[] }> {
    const response = await api.get('/configs');
    return response;
  },

  async getConfigById(id: string): Promise<any> {
    const response = await api.get(`/configs/${id}`);
    return response;
  },

  async createConfig(data: any): Promise<any> {
    const response = await api.post('/configs', data);
    return response;
  },

  async updateConfig(id: string, data: any): Promise<any> {
    const response = await api.put(`/configs/${id}`, data);
    return response;
  },

  async deleteConfig(id: string): Promise<any> {
    const response = await api.delete(`/configs/${id}`);
    return response;
  },

  async generateOpenClawConfig(userId: string): Promise<any> {
    const response = await api.get(`/config/generate/${userId}`);
    return response;
  },
};