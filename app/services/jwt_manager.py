import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from app.utils.credencials import jwt_secret_key


class JwtManager:

    @staticmethod
    def create_token(user_data: dict):
        """Criando um Token JWT"""
        user_data.update({"exp": datetime.utcnow() + timedelta(hours=1)})
        return jwt.encode(user_data, jwt_secret_key, algorithm="HS256")

    @staticmethod
    def verify_token(token: str):
        try:
            return jwt.decode(token, jwt_secret_key, algorithms=["HS256"])

        except ExpiredSignatureError as error:
            raise error

        except InvalidTokenError as error:
            raise error

        except Exception as error:
            raise error
