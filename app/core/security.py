import json
from urllib.request import urlopen
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

# bearer token cobrado no trabalho
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    valida o token jwt do auth0 e retorna o payload que sao os dados do usuario
    """
    token = credentials.credentials
    
    # uso essa url para obter as chaves publicas do meu dominio auth0
    jwks_url = f"https://{settings.AUTH0_DOMAIN}/.well-known/jwks.json"
    
    try:
        # pego as chaves publicas
        with urlopen(jwks_url) as response:
            jwks = json.loads(response.read())
        
        # le o cabecalho do token para saber qual chave foi usada
        unverified_header = jwt.get_unverified_header(token)
        
        rsa_key = {}
        # encontra a chave correta no conjunto de chaves - jwks
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"]
                }
        
        if rsa_key:
            # decodifica e valida o token audiencia, emissor e validade
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=[settings.AUTH0_ALGORITHM],
                audience=settings.AUTH0_API_AUDIENCE,
                issuer=settings.AUTH0_ISSUER,
            )
            return payload # retorna o dicionario com os dados do usuario
            
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token expirou",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="nao foi possivel validar as credenciais",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="erro na autenticacao",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="nao foi possivel encontrar a chave de assinatura apropriada",
        headers={"WWW-Authenticate": "Bearer"},
    )