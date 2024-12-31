import { Navigate, Outlet } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

export const ProtectedRoute = () => {
    const { user, isLoading } = useAuthStore();
    const isAuthenticated = !!user || !!localStorage.getItem('token');

    if (isLoading) {
        return <div>Loading...</div>;
    }

    return isAuthenticated ? <Outlet /> : <Navigate to="/login" replace />;
};