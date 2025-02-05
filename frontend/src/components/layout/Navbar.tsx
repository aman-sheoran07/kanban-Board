// src/components/layout/Navbar.tsx
import { useState } from 'react';
import { Link } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

export const Navbar = () => {
    const [isProfileOpen, setIsProfileOpen] = useState(false);
    const { user, logout } = useAuthStore();

    return (
        <nav className="bg-gray-800 text-white shadow">
            <div className="max-w-7xl mx-auto px-4">
                <div className="flex justify-between h-16">
                    <div className="flex">
                        <Link to="/boards" className="flex items-center">
                            <span className="text-xl font-bold text-white">Kanban Board</span>
                        </Link>
                    </div>

                    <div className="flex items-center">
                        <div className="relative">
                            <button
                                onClick={() => setIsProfileOpen(!isProfileOpen)}
                                className="flex items-center space-x-2 hover:bg-gray-700 px-3 py-2 rounded-md"
                            >
                                <span className="text-white">{user?.username}</span>
                                <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center text-white">
                                    {user?.username?.[0].toUpperCase()}
                                </div>
                            </button>

                            {isProfileOpen && (
                                <div className="absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1">
                                    <button
                                        onClick={logout}
                                        className="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 w-full text-left"
                                    >
                                        Sign out
                                    </button>
                                </div>
                            )}
                        </div>
                    </div>
                </div>
            </div>
        </nav>
    );
};