import api from './api';

export interface LoginResponse {
  token: string;
  user: {
    id: string;
    qq_number: string;
    nickname: string;
    role: string;
    permissions: string[];
  };
  message: string;
}

export const authService = {
  async login(qq_number: string): Promise<{ data: LoginResponse }> {
    const response = await api.post('/auth/login', { qq_number });
    return response;
  },

  async getCurrentUser(): Promise<any> {
    const response = await api.get('/auth/me');
    return response;
  },

  async updateProfile(data: any): Promise<any> {
    const response = await api.put('/auth/profile', data);
    return response;
  },

  logout(): void {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem('token');
  },

  getCurrentUser(): any {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
  },
};