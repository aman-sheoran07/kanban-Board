import { Link } from 'react-router-dom';

export const NotFoundPage = () => {
    return (
        <div className="min-h-screen flex items-center justify-center">
            <div className="text-center">
                <h1 className="text-4xl font-bold mb-4">404 - Page Not Found</h1>
                <p className="mb-4">The page you're looking for doesn't exist.</p>
                <Link to="/" className="text-blue-600 hover:text-blue-800">
                    Go Home
                </Link>
            </div>
        </div>
    );
};