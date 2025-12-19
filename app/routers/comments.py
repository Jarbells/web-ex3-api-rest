from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.models import Comment, Like
from app.core.security import get_current_user

router = APIRouter()

@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(status_code=404, detail="comentario nao encontrado")
    
    # dono do comentario
    if comment.author_id != current_user["sub"]:
        raise HTTPException(status_code=403, detail="nao autorizado")

    db.delete(comment)
    db.commit()
    return None

@router.post("/{comment_id}/like")
def like_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    existing_like = db.query(Like).filter(
        Like.user_id == current_user["sub"],
        Like.comment_id == comment_id
    ).first()

    if existing_like:
        raise HTTPException(status_code=400, detail="voce ja curtiu este comentario")

    new_like = Like(user_id=current_user["sub"], comment_id=comment_id)
    db.add(new_like)
    db.commit()
    return {"message": "comentario curtido"}