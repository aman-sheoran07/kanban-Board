import { Draggable, Droppable } from '@hello-pangea/dnd';
import { Card } from './Card';

interface ListProps {
    list: {
        id: number;
        title: string;
        cards: any[];
    };
    index: number;
}

export const List = ({ list, index }: ListProps) => {
    return (
        <Draggable draggableId={`list-${list.id}`} index={index}>
            {(provided) => (
                <div
                    ref={provided.innerRef}
                    {...provided.draggableProps}
                    className="bg-gray-200 rounded-lg p-4 w-72 flex-shrink-0"
                >
                    <div
                        {...provided.dragHandleProps}
                        className="flex items-center justify-between mb-4"
                    >
                        <h3 className="font-semibold">{list.title}</h3>
                        <button className="text-gray-500 hover:text-gray-700">•••</button>
                    </div>

                    <Droppable droppableId={`list-${list.id}`} type="card">
                        {(provided) => (
                            <div
                                ref={provided.innerRef}
                                {...provided.droppableProps}
                                className="space-y-2"
                            >
                                {list.cards.map((card, index) => (
                                    <Card key={card.id} card={card} index={index} />
                                ))}
                                {provided.placeholder}
                            </div>
                        )}
                    </Droppable>

                    <button className="mt-4 text-gray-600 hover:text-gray-800 w-full text-left">
                        + Add a card
                    </button>
                </div>
            )}
        </Draggable>
    );
};