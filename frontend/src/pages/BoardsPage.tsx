// src/pages/BoardsPage.tsx
const BoardsPage = () => {
    return (
        <div className="flex-1 p-6 bg-gray-100">
            <div className="mb-6">
                <h1 className="text-2xl font-bold text-gray-800">My Boards</h1>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                {/* Board cards will be mapped here */}
            </div>
        </div>
    );
};

export { BoardsPage };