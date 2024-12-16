import { Link, useLocation } from 'react-router-dom';

export const Sidebar = () => {
    const location = useLocation();

    const isActive = (path: string) => location.pathname === path;

    return (
        <div className="w-64 bg-gray-800 min-h-screen text-white p-4">
            <div className="space-y-4">
                <Link
                    to="/boards"
                    className={`block px-4 py-2 rounded-lg ${
                        isActive('/boards') ? 'bg-gray-700' : 'hover:bg-gray-700'
                    }`}
                >
                    My Boards
                </Link>
                <button
                    className="w-full px-4 py-2 bg-blue-500 hover:bg-blue-600 rounded-lg text-left"
                >
                    + Create Board
                </button>
            </div>
        </div>
    );
};