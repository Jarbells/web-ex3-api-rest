from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# schemas basicos
class CategoryBase(BaseModel):
    name: str

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    class Config:
        from_attributes = True

class TagBase(BaseModel):
    name: str

class TagResponse(TagBase):
    id: int
    class Config:
        from_attributes = True

# comentarios
class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    pass

class CommentResponse(CommentBase):
    id: int
    author_id: str
    post_id: int
    created_at: datetime
    likes_count: int = 0
    class Config:
        from_attributes = True

# posts
class PostBase(BaseModel):
    title: str
    content: str
    category_id: int

class PostCreate(PostBase):
    tags: List[str] = [] # recebe a lista de nomes de tags como python ou api

class PostResponse(PostBase):
    id: int
    author_id: str
    created_at: datetime
    category: Optional[CategoryResponse] = None
    tags: List[TagResponse] = []
    likes_count: int = 0
    comments: List[CommentResponse] = [] # opcional - posso tirar se pesar na listagem
    
    class Config:
        from_attributes = True

# schema para atualizar os posts - campos opcionais
class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category_id: Optional[int] = None

# schema para atualizar a categoria
class CategoryUpdate(CategoryBase):
    pass