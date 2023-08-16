"""Construção da Api FastAPI."""
import os

from ariadne.asgi import GraphQL
from fastapi import FastAPI

from app.gql_config.graphql_error import graphql_format_error
from app.models.schema_importer import graphql_schema
from app.routers.status import status_router
from app.services.sentry import Sentry


# TODO -> Continuar os testes unitários

# TODO -> Finalizar os Update / Delete de todas as querys / mutations
# TODO -> Arrumar as docstring (mypy)


class CreateApp:
    """Classe para criação da API FastAPI."""

    def __init__(self):
        """Construtor da classe."""
        self.app = FastAPI()

    def load_routes(self):
        """Carregamento das rotas."""
        self.app.include_router(status_router)

    def load_graphql(self):
        """Instancia do GraphQL e seus Schemas."""
        self.app.mount(
            "/graphql",
            GraphQL(
                graphql_schema,
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
