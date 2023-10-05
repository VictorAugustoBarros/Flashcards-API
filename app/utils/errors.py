class DatabaseInsertFailed(Exception):
    """Exceção para falhas de inserção no banco de dados."""


class DatabaseUpdateFailed(Exception):
    """Exceção para falhas de atualização no banco de dados."""


class DatabaseDeleteFailed(Exception):
    """Exceção para falhas de deleção no banco de dados."""


class DatabaseQueryFailed(Exception):
    """Exceção para falhas na busca das informações no banco de dados."""

    def __init__(self, query: str):
        self.query = query


class TokenError(Exception):
    pass


class InvalidToken(Exception):
    def __str__(self):
        return "Token Inválido!"


class ExpiredToken(Exception):
    def __str__(self):
        return "Token Expirado!"


class UsernameAlreadyTaken(Exception):
    def __str__(self):
        return "Username já existe!"


class EmailAlreadyTaken(Exception):
    def __str__(self):
        return "Email já existe!"
