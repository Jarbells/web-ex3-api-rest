from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func, desc

from app.db.session import get_db
from app.models.models import Post, Tag, Like, Comment, Category
from app.schemas.schemas import PostCreate, PostResponse, CommentCreate, CommentResponse
from app.core.security import get_current_user
from app.schemas.schemas import PostUpdate

router = APIRouter()

# crud postagens
@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate, 
    db: Session = Depends(get_db), 
    current_user: dict = Depends(get_current_user)
):
    # Verifica categoria
    category = db.query(Category).filter(Category.id == post.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="categoria nao encontrada")

    # processa tags
    tags_objects = []
    for tag_name in post.tags:
        # busca tag existente ou cria nova
        tag = db.query(Tag).filter(Tag.name == tag_name).first()
        if not tag:
            tag = Tag(name=tag_name)
            db.add(tag)
        tags_objects.append(tag)
    
    new_post = Post(
        title=post.title,
        content=post.content,
        author_id=current_user["sub"], # pega o id do auth0
        category_id=post.category_id,
        tags=tags_objects
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    
    # calcula likes comecando do zero
    new_post.likes_count = 0 
    return new_post

@router.get("/", response_model=List[PostResponse])
def list_posts(
    db: Session = Depends(get_db),
    limit: int = 10,
    offset: int = 0,
    q: Optional[str] = None,           # busca de texto
    category_id: Optional[int] = None, # filtro categoria
    author_id: Optional[str] = None,   # filtro autor
    tag: Optional[str] = None,         # filtro tag
    sort_by: str = "date"              # ordenacao - date ou likes
):
    query = db.query(Post)

    # filtros
    if category_id:
        query = query.filter(Post.category_id == category_id)
    if author_id:
        query = query.filter(Post.author_id == author_id)
    if tag:
        query = query.join(Post.tags).filter(Tag.name == tag)
    
    # busca por texto
    if q:
        query = query.filter(
            (Post.title.contains(q)) | (Post.content.contains(q))
        )

    # ordenar
    if sort_by == "likes":
        # join para contar likes e ordenar
        query = query.outerjoin(Like, (Like.post_id == Post.id)).group_by(Post.id).order_by(desc(func.count(Like.id)))
    else:
        query = query.order_by(desc(Post.created_at))

    # paginar
    posts = query.offset(offset).limit(limit).all()

    # preencher contagem de likes manualmente para o response
    for post in posts:
        post.likes_count = db.query(Like).filter(Like.post_id == post.id).count()
    
    return posts

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post nao encontrado")
    
    # so o dono ou admin pode deletar
    if post.author_id != current_user["sub"]: 
        raise HTTPException(status_code=403, detail="permissao negada")

    db.delete(post)
    db.commit()
    return None

# comentarios em posts
@router.post("/{post_id}/comments", response_model=CommentResponse)
def create_comment(
    post_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="post nao encontrado")

    new_comment = Comment(
        content=comment.content,
        author_id=current_user["sub"],
        post_id=post_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    new_comment.likes_count = 0
    return new_comment

# curtidas
@router.post("/{post_id}/like")
def like_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # ve se ja curtiu
    existing_like = db.query(Like).filter(
        Like.user_id == current_user["sub"],
        Like.post_id == post_id
    ).first()

    if existing_like:
        raise HTTPException(status_code=400, detail="voce ja curtiu este post")

    new_like = Like(user_id=current_user["sub"], post_id=post_id)
    db.add(new_like)
    db.commit()
    return {"message": "post curtido com sucesso"}

@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int,
    post_update: PostUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # busca o post
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if not db_post:
        raise HTTPException(status_code=404, detail="post nao encontrado")

    # verifica permissao - so o dono pode editar
    if db_post.author_id != current_user["sub"]:
        raise HTTPException(status_code=403, detail="voce so pode editar seus proprios posts")

    # atualiza apenas os campos enviados
    if post_update.title:
        db_post.title = post_update.title
    if post_update.content:
        db_post.content = post_update.content
    if post_update.category_id:
        # verifica se a nova categoria existe
        category = db.query(Category).filter(Category.id == post_update.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="categoria invalida")
        db_post.category_id = post_update.category_id

    db.commit()
    db.refresh(db_post)
    
    # recalcula likes para a resposta
    db_post.likes_count = db.query(Like).filter(Like.post_id == db_post.id).count()
    return db_post