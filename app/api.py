"""Construção da Api FastAPI."""
import os

from ariadne.asgi import GraphQL
from fastapi import FastAPI

from app.gql_config.graphql_error import graphql_format_error
from app.models.schema_importer import graphql_schema
from app.routers.status import status_router
from app.services.sentry import Sentry

# Frontend
# TODO -> Pensar no web design da aplicação
# TODO -> Criar o básico do cadastro e visualização dos Decks/Subdecks/Cards


# Backend
# TODO -> Finalizar os Updates (Mutations)
# TODO -> Arrumar as docstring (mypy)

# TODO -> Criar servidor da Amazon (Terraform)
# TODO -> Estudar o Jenkins (Deploy automatizado)
# TODO -> Fazer teste de carga em prod (Locust)


from fastapi.middleware.cors import CORSMiddleware


class CreateApp:
    """Classe para criação da API FastAPI."""

    def __init__(self):
        """Construtor da classe."""
        self.app = FastAPI()
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["http://localhost:3000"],
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
