import { useParams } from 'react-router-dom';

const BoardPage = () => {
    const { boardId } = useParams();

    return (
        <div>
            <h1>Board {boardId}</h1>
            <div>Board details coming soon...</div>
        </div>
    );
};

// Add this export statement
export { BoardPage };