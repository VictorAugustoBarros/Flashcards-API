"""Construção da Api FastAPI."""
import os

from ariadne.asgi import GraphQL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.graphql_config.graphql_error import graphql_format_error
from app.graphql_config.schema_importer import graphql_schema
from app.routers.status import status_router
from app.sentry import Sentry


# Frontend
# TODO -> Pensar no design do updater/delete dos Decks/Subdecks (Div da direita)
# TODO -> Popular os graficos da dashboard com valores do banco

# Backend
# TODO -> Finalizar os Updates/Deletes (Mutations)
# TODO -> Arrumar as docstring (mypy)
# TODO -> Aplicar o Nuxt no projeto (estudar)

# Outros
# TODO -> Responsividade
# TODO -> Adicionar pre-commit no projeto https://pre-commit.com/
# TODO -> Validar a segurança nas requests (Jwt, permissões, ...)


class CreateApp:
    """Classe para criação da API FastAPI."""

    def __init__(self):
        """Construtor da classe."""
        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000", "http://localhost:6006"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    def load_routes(self):
        """Carregamento das rotas."""
        self.app.include_router(status_router)

    def load_graphql(self):
        """Instancia do GraphQL e seus Schemas."""
        self.app.mount(
            "/graphql",
            GraphQL(
                schema=graphql_schema,
                error_formatter=graphql_format_error,
                debug=os.getenv("DEBUG", "False") == "True",
            ),
        )

    def start(self):
        """Carregamento das configurações da API."""
        self.load_routes()
        self.load_graphql()
        return self.app


create_app = CreateApp()
app = create_app.start()

Sentry().start()

if __name__ == "__main__":  # type: ignore
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
