import { create } from 'zustand';
import { authService } from '../services/auth.service';
import { User, LoginCredentials, RegisterData, AuthResponse } from '../types/auth.types';

interface AuthState {
    user: User | null;
    isLoading: boolean;
    error: string | null;
    login: (username: string, password: string) => Promise<void>;
    logout: () => void;
    register: (data: RegisterData) => Promise<void>;
    setUser: (user: User | null) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
    user: null,
    isLoading: false,
    error: null,

    setUser: (user) => set({ user }),

    login: async (username: string, password: string) => {
        set({ isLoading: true, error: null });
        try {
            const { data } = await authService.login({ username, password });
            localStorage.setItem('token', data.access_token);
            set({ user: { username, id: 0, email: '' } });
        } catch (error: any) {
            set({ error: error.response?.data?.detail || 'Login failed' });
            throw error;
        } finally {
            set({ isLoading: false });
        }
    },

    logout: () => {
        localStorage.removeItem('token');
        set({ user: null });
    },

    register: async (data: RegisterData) => {
        set({ isLoading: true, error: null });
        try {
            const response = await authService.register(data);
            set({ user: response.data });
        } catch (error: any) {
            set({ error: error.response?.data?.detail || 'Registration failed' });
            throw error;
        } finally {
            set({ isLoading: false });
        }
    }
}));