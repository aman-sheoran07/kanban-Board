from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.board import Board
from app.schemas.board import BoardCreate, BoardResponse, BoardUpdate
from app.utils.auth import get_current_user

router = APIRouter(prefix="/boards", tags=["boards"])

@router.post("/", response_model=BoardResponse)
async def create_board(
    board: BoardCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_board = Board(**board.model_dump(), owner_id=current_user.id)
    db.add(db_board)
    db.commit()
    db.refresh(db_board)
    return db_board

@router.get("/", response_model=List[BoardResponse])
async def get_user_boards(
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Board).filter(Board.owner_id == current_user.id).all()

@router.get("/{board_id}", response_model=BoardResponse)
async def get_board(
    board_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    board = db.query(Board).filter(
        Board.id == board_id,
        Board.owner_id == current_user.id
    ).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")
    return board

@router.put("/{board_id}", response_model=BoardResponse)
async def update_board(
    board_id: int,
    board_update: BoardUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    board = db.query(Board).filter(
        Board.id == board_id,
        Board.owner_id == current_user.id
    ).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    for key, value in board_update.model_dump().items():
        setattr(board, key, value)

    db.commit()
    db.refresh(board)
    return board

@router.delete("/{board_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_board(
    board_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    board = db.query(Board).filter(
        Board.id == board_id,
        Board.owner_id == current_user.id
    ).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    db.delete(board)
    db.commit()
    return None