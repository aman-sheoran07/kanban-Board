import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { LoginForm } from './components/auth/LoginForm';
import { RegisterForm } from './components/auth/RegisterForm';
import { ProtectedRoute } from './components/shared/ProtectedRoute';
import { MainLayout } from './components/layout/MainLayout';
import { BoardsPage } from './pages/BoardsPage';
import { BoardPage } from './pages/BoardPage';
import { NotFoundPage } from './pages/NotFoundPage';

function App() {
    console.log("App is rendering"); // Debug log
    return (
        <Router>
            <Routes>
                {/* Public Routes */}
                <Route path="/login" element={<LoginForm />} />
                <Route path="/register" element={<RegisterForm />} />

                {/* Protected Routes */}
                <Route element={<ProtectedRoute />}>
                    <Route element={<MainLayout />}>
                        <Route path="/boards" element={<BoardsPage />} />
                        <Route path="/boards/:boardId" element={<BoardPage />} />
                    </Route>
                </Route>

                {/* Redirect & 404 */}
                <Route path="/" element={<Navigate to="/boards" replace />} />
                <Route path="*" element={<NotFoundPage />} />
            </Routes>
        </Router>
    );
}

export default App;