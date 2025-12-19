from fastapi import FastAPI
from app.core.config import settings
from app.db.session import engine
from app.models import models

# importar as rotas
from app.routers import auth_test, categories, posts, comments

# cria as tabelas quando inicia
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

# registra os roteadores
app.include_router(auth_test.router, prefix=settings.API_V1_STR + "/auth", tags=["Auth Test"])
app.include_router(categories.router, prefix=settings.API_V1_STR + "/categories", tags=["Categories"])
app.include_router(posts.router, prefix=settings.API_V1_STR + "/posts", tags=["Posts"])
app.include_router(comments.router, prefix=settings.API_V1_STR + "/comments", tags=["Comments"])

@app.get("/")
def root():
    return {"message": "api plataforma comunidade - rodando", "docs": "/docs"}