from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, board, list, card

app = FastAPI(title='Kanban Board API')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(board.router)
app.include_router(list.router)
app.include_router(card.router)