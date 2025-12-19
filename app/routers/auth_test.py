from fastapi import APIRouter, Depends
from app.core.security import get_current_user

router = APIRouter()

@router.get("/teste-seguro")
def teste_seguro(user: dict = Depends(get_current_user)):
    """
    rota simples para testar se o token jwt esta sendo validado corretamente.
    """
    return {
        "status": "autenticado com sucesso",
        "user_id": user.get("sub"),
        "dados_completos": user
    }