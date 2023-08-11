"""Construção da Api FastAPI."""

from fastapi import FastAPI
from app.models.cards.cards_importer import graphql_cards_schema
from app.routers.status import status_router
from app.sentry import Sentry

from starlette_graphene3 import GraphQLApp, make_graphiql_handler


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
        self.app.mount("/", GraphQLApp(graphql_cards_schema, on_get=make_graphiql_handler()))  # Graphiql IDE

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
