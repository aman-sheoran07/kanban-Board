from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.card import Card
from app.models.list import List as ListModel
from app.models.board import Board
from app.schemas.card import CardCreate, CardResponse, CardUpdate
from app.utils.auth import get_current_user

router = APIRouter(prefix="/cards", tags=["cards"])

@router.post("/", response_model=CardResponse)
async def create_card(
    card_data: CardCreate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify list exists and user has access
    list_access = db.query(ListModel).join(Board).filter(
        ListModel.id == card_data.list_id,
        Board.owner_id == current_user.id
    ).first()
    if not list_access:
        raise HTTPException(status_code=404, detail="List not found")

    db_card = Card(**card_data.model_dump())
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card

@router.get("/list/{list_id}", response_model=List[CardResponse])
async def get_cards(
    list_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify list access
    list_access = db.query(ListModel).join(Board).filter(
        ListModel.id == list_id,
        Board.owner_id == current_user.id
    ).first()
    if not list_access:
        raise HTTPException(status_code=404, detail="List not found")

    cards = db.query(Card).filter(
        Card.list_id == list_id
    ).order_by(Card.position).all()
    return cards

@router.get("/{card_id}", response_model=CardResponse)
async def get_card(
    card_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    card = db.query(Card).join(ListModel).join(Board).filter(
        Card.id == card_id,
        Board.owner_id == current_user.id
    ).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")
    return card

@router.put("/{card_id}", response_model=CardResponse)
async def update_card(
    card_id: int,
    card_update: CardUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    card = db.query(Card).join(ListModel).join(Board).filter(
        Card.id == card_id,
        Board.owner_id == current_user.id
    ).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    update_data = card_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(card, key, value)

    db.commit()
    db.refresh(card)
    return card

@router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_card(
    card_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    card = db.query(Card).join(ListModel).join(Board).filter(
        Card.id == card_id,
        Board.owner_id == current_user.id
    ).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    db.delete(card)
    db.commit()
    return None

@router.post("/{card_id}/assign/{user_id}", response_model=CardResponse)
async def assign_card(
    card_id: int,
    user_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    card = db.query(Card).join(ListModel).join(Board).filter(
        Card.id == card_id,
        Board.owner_id == current_user.id
    ).first()
    if not card:
        raise HTTPException(status_code=404, detail="Card not found")

    card.assigned_to_id = user_id
    db.commit()
    db.refresh(card)
    return card

from app.schemas.position import CardPositionUpdate
from sqlalchemy import case

# Add this new endpoint to the existing card.py router
@router.put("/reorder", status_code=status.HTTP_200_OK)
async def reorder_cards(
    positions: CardPositionUpdate,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get all card IDs
    card_ids = [pos.id for pos in positions.cards]

    # Verify user has access to all cards
    cards = db.query(Card).join(ListModel).join(Board).filter(
        Card.id.in_(card_ids),
        Board.owner_id == current_user.id
    ).all()

    if len(cards) != len(card_ids):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to one or more cards"
        )

    # Update each card's position and list
    for pos in positions.cards:
        db.query(Card).filter(Card.id == pos.id).update({
            "position": pos.position,
            "list_id": pos.list_id
        }, synchronize_session=False)

    db.commit()
    return {"message": "Cards reordered successfully"}