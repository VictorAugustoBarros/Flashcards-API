from app.jwt_manager import JwtManager


def validate_token(func):
    def wrapper(*args, **kwargs):
        token = dict(args[1].context["request"].headers).get("authorization")
        if not token:
            kwargs.update({"token": {"valid": False, "error": "Token não informado"}})
            return func(*args, **kwargs)

        try:
            jwt_manager = JwtManager()
            user_info = jwt_manager.verify_token(token=token)
            kwargs.update({"token": {"valid": True, "user_info": user_info}})

        except Exception as error:
            kwargs.update({"token": {"valid": False, "error": str(error)}})

        return func(*args, **kwargs)

    return wrapper


class MiddlewareValidation:
    @staticmethod
    async def validate_token(resolver, obj, info, **args):
        BYPASS = "login"

        if info.operation.name.value in BYPASS:
            return resolver(obj, info, **args)

        token = dict(info.context["request"].headers).get("authorization")
        if not token:
            raise Exception("Token não informado")

        try:
            jwt_manager = JwtManager()

            jwt_manager.verify_token(token=token)

            value = resolver(obj, info, **args)
            return value

        except Exception as error:
            raise ValueError("Unauthorized")
