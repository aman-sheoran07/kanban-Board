from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.list import List as ListModel
from app.models.board import Board
from app.schemas.list import ListCreate, ListResponse, ListUpdate
from app.utils.auth import get_current_user

router = APIRouter(prefix="/lists", tags=["lists"])

@router.post("/", response_model=ListResponse)
async def create_list(
    list_data: ListCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify board exists and user has access
    board = db.query(Board).filter(
        Board.id == list_data.board_id,
        Board.owner_id == current_user.id
    ).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    db_list = ListModel(**list_data.model_dump())
    db.add(db_list)
    db.commit()
    db.refresh(db_list)
    return db_list

@router.get("/board/{board_id}", response_model=List[ListResponse])
async def get_lists(
    board_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify board access
    board = db.query(Board).filter(
        Board.id == board_id,
        Board.owner_id == current_user.id
    ).first()
    if not board:
        raise HTTPException(status_code=404, detail="Board not found")

    lists = db.query(ListModel).filter(
        ListModel.board_id == board_id
    ).order_by(ListModel.position).all()
    return lists

@router.put("/{list_id}", response_model=ListResponse)
async def update_list(
    list_id: int,
    list_update: ListUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get list and verify access
    db_list = db.query(ListModel).join(Board).filter(
        ListModel.id == list_id,
        Board.owner_id == current_user.id
    ).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")

    # Update list
    for key, value in list_update.model_dump(exclude_unset=True).items():
        setattr(db_list, key, value)

    db.commit()
    db.refresh(db_list)
    return db_list

@router.delete("/{list_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_list(
    list_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get list and verify access
    db_list = db.query(ListModel).join(Board).filter(
        ListModel.id == list_id,
        Board.owner_id == current_user.id
    ).first()
    if not db_list:
        raise HTTPException(status_code=404, detail="List not found")

    db.delete(db_list)
    db.commit()
    return None