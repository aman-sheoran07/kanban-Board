import api from '../utils/axios';

export const authService = {
  async register(data: any) {
    return await api.post('/auth/register', data);
  },

  async login(credentials: any) {
    const formData = new URLSearchParams();
    formData.append('username', credentials.username);
    formData.append('password', credentials.password);

    const { data } = await api.post('/auth/token', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    return data;  // Return just the data
  }
};