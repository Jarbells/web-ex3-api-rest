from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base

# tabela muitos para muitos entre posts e tags
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tags.id"), primary_key=True),
)

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    
    # relacionamento reverso, nao e necessario mas facilita as queries
    posts = relationship("Post", back_populates="category")

class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    
    posts = relationship("Post", secondary=post_tags, back_populates="tags")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(String, index=True, nullable=False) # o sub do auth0
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # chave estrangeira para categoria
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    
    # relacionamentos
    category = relationship("Category", back_populates="posts")
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")
    likes = relationship("Like", back_populates="post", cascade="all, delete")

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    author_id = Column(String, nullable=False) # o sub do auth0
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    is_hidden = Column(Integer, default=0) # para moderacao - 0=visivel, 1=oculto
    
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=False)
    post = relationship("Post", back_populates="comments")
    likes = relationship("Like", back_populates="comment", cascade="all, delete")

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False) # quem curtiu
    
    # pode ser um like de um post ou de um comentario
    post_id = Column(Integer, ForeignKey("posts.id"), nullable=True)
    comment_id = Column(Integer, ForeignKey("comments.id"), nullable=True)
    
    post = relationship("Post", back_populates="likes")
    comment = relationship("Comment", back_populates="likes")