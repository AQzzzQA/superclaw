import api from './api';

export interface User {
  id: string;
  qq_number: string;
  nickname: string;
  avatar_url?: string;
  role: string;
  permissions: string[];
  created_at: string;
  updated_at: string;
}

export const userService = {
  async getAllUsers(): Promise<{ data: User[] }> {
    const response = await api.get('/users');
    return response;
  },

  async getUserById(id: string): Promise<any> {
    const response = await api.get(`/users/${id}`);
    return response;
  },

  async getUserByQQNumber(qq_number: string): Promise<any> {
    const response = await api.get(`/users/qq/${qq_number}`);
    return response;
  },

  async createUser(data: any): Promise<any> {
    const response = await api.post('/users', data);
    return response;
  },

  async updateUser(id: string, data: any): Promise<any> {
    const response = await api.put(`/users/${id}`, data);
    return response;
  },

  async deleteUser(id: string): Promise<any> {
    const response = await api.delete(`/users/${id}`);
    return response;
  },

  async searchUsers(query: string): Promise<any> {
    const response = await api.get(`/users/search?q=${encodeURIComponent(query)}`);
    return response;
  },
};