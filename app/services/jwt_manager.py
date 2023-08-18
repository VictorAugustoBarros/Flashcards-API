import jwt
from fastapi.responses import JSONResponse
from datetime import datetime, timedelta
from fastapi import HTTPException


class JwtManager:
    def __init__(self):
        self.secret_key = "vamosverseissofunciona"

    def create_token(self, payload: dict):
        payload.update({"exp": datetime.utcnow() + timedelta(days=7)})
        return jwt.encode(payload, self.secret_key, algorithm="HS256")

    def verify_token(self, token: str):
        try:
            return jwt.decode(token, self.secret_key, algorithms=["HS256"])

        except jwt.exceptions.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token Expirado!")

        except jwt.exceptions.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Token Inválido!")

        except Exception:
            raise HTTPException(
                status_code=401, detail="Falha na autenticação do Token!"
            )
