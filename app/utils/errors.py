from sentry_sdk import capture_exception


class DatabaseInsertFailed(Exception):
    """Exceção para falhas de inserção no banco de dados."""

    def __init__(self, _):
        capture_exception(self)

class DatabaseUpdateFailed(Exception):
    """Exceção para falhas de atualização no banco de dados."""

    def __init__(self, _):
        capture_exception(self)

class DatabaseDeleteFailed(Exception):
    """Exceção para falhas de deleção no banco de dados."""

    def __init__(self, _):
        capture_exception(self)


class DatabaseQueryFailed(Exception):
    """Exceção para falhas na busca das informações no banco de dados."""

    def __init__(self, _):
        capture_exception(self)


class TokenError(Exception):
    pass


class InvalidToken(Exception):
    def __str__(self):
        return "Token Inválido!"


class ExpiredToken(Exception):
    def __str__(self):
        return "Token Expirado!"
