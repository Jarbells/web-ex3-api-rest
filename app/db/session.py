from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# conexao com o sqlite
# check_same_thread=False - necessario apenas para sqlite
engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URI, 
    connect_args={"check_same_thread": False}
)

# cria a fabrica de sessoes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# dependencia para injetar o banco de dados nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()