import { useEffect, useState } from 'react';
import { DragDropContext, Droppable } from '@hello-pangea/dnd';
import { List } from './List';
import { useParams } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

interface BoardData {
    id: number;
    title: string;
    lists: ListData[];
}

interface ListData {
    id: number;
    title: string;
    position: number;
    cards: CardData[];
}

interface CardData {
    id: number;
    title: string;
    description?: string;
    position: number;
}

export const Board = () => {
    const [board, setBoard] = useState<BoardData | null>(null);
    const [loading, setLoading] = useState(true);
    const { boardId } = useParams();
    const { user } = useAuthStore();

    useEffect(() => {
        // TODO: Fetch board data
        setLoading(false);
    }, [boardId]);

    const handleDragEnd = (result: any) => {
        // TODO: Implement drag and drop logic
    };

    if (loading) return <div>Loading board...</div>;
    if (!board) return <div>Board not found</div>;

    return (
        <DragDropContext onDragEnd={handleDragEnd}>
            <div className="min-h-screen bg-gray-100 p-4">
                <div className="flex items-center justify-between mb-6">
                    <h1 className="text-2xl font-bold">{board.title}</h1>
                    <button className="bg-blue-500 text-white px-4 py-2 rounded">
                        Add List
                    </button>
                </div>
                <Droppable droppableId="lists" direction="horizontal" type="list">
                    {(provided) => (
                        <div
                            {...provided.droppableProps}
                            ref={provided.innerRef}
                            className="flex space-x-4 overflow-x-auto pb-4"
                        >
                            {board.lists.map((list, index) => (
                                <List key={list.id} list={list} index={index} />
                            ))}
                            {provided.placeholder}
                        </div>
                    )}
                </Droppable>
            </div>
        </DragDropContext>
    );
};